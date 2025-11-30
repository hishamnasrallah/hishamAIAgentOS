/*
  # Create Workflows Tables

  1. New Tables
    - `workflows` - Main workflow orchestration
    - `workflow_steps` - Individual workflow steps
    - `workflow_templates` - Reusable templates
    - `workflow_steps_depends_on` - Step dependencies

  2. Security
    - Enable RLS
    - Add appropriate policies
*/

CREATE TABLE IF NOT EXISTS workflows (
  id bigserial PRIMARY KEY,
  name varchar(255) NOT NULL,
  description text NOT NULL,
  workflow_type varchar(50) NOT NULL,
  status varchar(20) NOT NULL DEFAULT 'PENDING',
  config jsonb NOT NULL DEFAULT '{}',
  input_data jsonb NOT NULL DEFAULT '{}',
  output_data jsonb NOT NULL DEFAULT '{}',
  created_by_id bigint REFERENCES users(id) ON DELETE SET NULL,
  current_step integer NOT NULL DEFAULT 0,
  total_steps integer NOT NULL DEFAULT 0,
  priority integer NOT NULL DEFAULT 5,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  started_at timestamptz,
  completed_at timestamptz
);

CREATE INDEX IF NOT EXISTS workflows_type_status_idx ON workflows(workflow_type, status);
CREATE INDEX IF NOT EXISTS workflows_created_by_status_idx ON workflows(created_by_id, status);

CREATE TABLE IF NOT EXISTS workflow_steps (
  id bigserial PRIMARY KEY,
  workflow_id bigint NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
  step_order integer NOT NULL,
  name varchar(255) NOT NULL,
  description text,
  step_type varchar(50) NOT NULL DEFAULT 'AGENT_TASK',
  status varchar(20) NOT NULL DEFAULT 'PENDING',
  config jsonb NOT NULL DEFAULT '{}',
  input_data jsonb NOT NULL DEFAULT '{}',
  output_data jsonb NOT NULL DEFAULT '{}',
  agent_task_id bigint REFERENCES agent_tasks(id) ON DELETE SET NULL,
  retry_count integer NOT NULL DEFAULT 0,
  max_retries integer NOT NULL DEFAULT 3,
  error_message text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  started_at timestamptz,
  completed_at timestamptz,
  UNIQUE(workflow_id, step_order)
);

CREATE INDEX IF NOT EXISTS workflow_steps_workflow_id_idx ON workflow_steps(workflow_id);
CREATE INDEX IF NOT EXISTS workflow_steps_status_idx ON workflow_steps(status);

CREATE TABLE IF NOT EXISTS workflow_steps_depends_on (
  id bigserial PRIMARY KEY,
  from_workflowstep_id bigint NOT NULL REFERENCES workflow_steps(id) ON DELETE CASCADE,
  to_workflowstep_id bigint NOT NULL REFERENCES workflow_steps(id) ON DELETE CASCADE,
  UNIQUE(from_workflowstep_id, to_workflowstep_id)
);

CREATE TABLE IF NOT EXISTS workflow_templates (
  id bigserial PRIMARY KEY,
  name varchar(255) NOT NULL UNIQUE,
  description text NOT NULL,
  workflow_type varchar(50) NOT NULL,
  template_config jsonb NOT NULL,
  is_active boolean NOT NULL DEFAULT true,
  created_by_id bigint REFERENCES users(id) ON DELETE SET NULL,
  usage_count integer NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflow_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflow_templates ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own workflows"
  ON workflows FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can create workflows"
  ON workflows FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Users can read workflow steps"
  ON workflow_steps FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can read templates"
  ON workflow_templates FOR SELECT
  TO authenticated
  USING (true);
