/*
  # Create Projects Tables

  1. New Tables
    - `projects` - Main project container
    - `project_memberships` - Team membership
    - `sprints` - Agile sprints
    - `epics` - Large bodies of work
    - `stories` - User stories
    - `tasks` - Sub-tasks
    - `comments` - Story comments

  2. Security
    - Enable RLS
    - Add appropriate policies
*/

CREATE TABLE IF NOT EXISTS projects (
  id bigserial PRIMARY KEY,
  key varchar(10) NOT NULL UNIQUE,
  name varchar(255) NOT NULL,
  description text,
  owner_id bigint REFERENCES users(id) ON DELETE SET NULL,
  is_active boolean NOT NULL DEFAULT true,
  settings jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS projects_key_idx ON projects(key);
CREATE INDEX IF NOT EXISTS projects_is_active_idx ON projects(is_active);

CREATE TABLE IF NOT EXISTS project_memberships (
  id bigserial PRIMARY KEY,
  project_id bigint NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  user_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role varchar(50) NOT NULL DEFAULT 'DEVELOPER',
  joined_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE(project_id, user_id)
);

CREATE TABLE IF NOT EXISTS sprints (
  id bigserial PRIMARY KEY,
  project_id bigint NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  name varchar(255) NOT NULL,
  goal text,
  start_date date NOT NULL,
  end_date date NOT NULL,
  status varchar(20) NOT NULL DEFAULT 'PLANNING',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS sprints_project_id_idx ON sprints(project_id);
CREATE INDEX IF NOT EXISTS sprints_status_idx ON sprints(status);

CREATE TABLE IF NOT EXISTS epics (
  id bigserial PRIMARY KEY,
  project_id bigint NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  key varchar(20) NOT NULL UNIQUE,
  title varchar(255) NOT NULL,
  description text NOT NULL,
  owner_id bigint REFERENCES users(id) ON DELETE SET NULL,
  status varchar(20) NOT NULL DEFAULT 'TODO',
  priority varchar(20) NOT NULL DEFAULT 'MEDIUM',
  generated_by_ai boolean NOT NULL DEFAULT false,
  ai_confidence decimal(3, 2),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS epics_project_id_idx ON epics(project_id);
CREATE INDEX IF NOT EXISTS epics_status_idx ON epics(status);
CREATE INDEX IF NOT EXISTS epics_key_idx ON epics(key);

CREATE TABLE IF NOT EXISTS stories (
  id bigserial PRIMARY KEY,
  project_id bigint NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  epic_id bigint REFERENCES epics(id) ON DELETE SET NULL,
  sprint_id bigint REFERENCES sprints(id) ON DELETE SET NULL,
  key varchar(20) NOT NULL UNIQUE,
  title varchar(255) NOT NULL,
  description text NOT NULL,
  acceptance_criteria jsonb NOT NULL DEFAULT '[]',
  story_points integer,
  assignee_id bigint REFERENCES users(id) ON DELETE SET NULL,
  assigned_to_ai boolean NOT NULL DEFAULT false,
  status varchar(20) NOT NULL DEFAULT 'BACKLOG',
  priority varchar(20) NOT NULL DEFAULT 'MEDIUM',
  generated_by_ai boolean NOT NULL DEFAULT false,
  ai_confidence decimal(3, 2),
  technical_notes text,
  created_by_id bigint REFERENCES users(id) ON DELETE SET NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS stories_project_id_idx ON stories(project_id);
CREATE INDEX IF NOT EXISTS stories_epic_id_idx ON stories(epic_id);
CREATE INDEX IF NOT EXISTS stories_sprint_id_idx ON stories(sprint_id);
CREATE INDEX IF NOT EXISTS stories_status_idx ON stories(status);
CREATE INDEX IF NOT EXISTS stories_key_idx ON stories(key);

CREATE TABLE IF NOT EXISTS tasks (
  id bigserial PRIMARY KEY,
  story_id bigint NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
  title varchar(255) NOT NULL,
  description text,
  assignee_id bigint REFERENCES users(id) ON DELETE SET NULL,
  assigned_to_ai boolean NOT NULL DEFAULT false,
  status varchar(20) NOT NULL DEFAULT 'TODO',
  estimated_hours decimal(5, 2),
  actual_hours decimal(5, 2),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS tasks_story_id_idx ON tasks(story_id);
CREATE INDEX IF NOT EXISTS tasks_status_idx ON tasks(status);

CREATE TABLE IF NOT EXISTS comments (
  id bigserial PRIMARY KEY,
  story_id bigint NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
  author_id bigint REFERENCES users(id) ON DELETE SET NULL,
  content text NOT NULL,
  is_ai_generated boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS comments_story_id_idx ON comments(story_id);
CREATE INDEX IF NOT EXISTS comments_created_at_idx ON comments(created_at);

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE sprints ENABLE ROW LEVEL SECURITY;
ALTER TABLE epics ENABLE ROW LEVEL SECURITY;
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read projects"
  ON projects FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can create projects"
  ON projects FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Users can read stories"
  ON stories FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can create stories"
  ON stories FOR INSERT
  TO authenticated
  WITH CHECK (true);
