/*
  # Create Agents Tables

  1. New Tables
    - `ai_providers` - AI provider configurations
    - `prompts` - Agent system prompts
    - `agent_tasks` - Agent tasks
    - `agent_executions` - Task execution history

  2. Security
    - Enable RLS on all tables
    - Add appropriate policies
*/

CREATE TABLE IF NOT EXISTS ai_providers (
  id bigserial PRIMARY KEY,
  name varchar(50) NOT NULL UNIQUE,
  provider_type varchar(20) NOT NULL,
  api_key varchar(500),
  api_url varchar(200),
  model_name varchar(100) NOT NULL,
  is_active boolean NOT NULL DEFAULT true,
  max_tokens integer NOT NULL DEFAULT 4096,
  temperature decimal(3, 2) NOT NULL DEFAULT 0.7,
  config jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS prompts (
  id bigserial PRIMARY KEY,
  agent_type varchar(50) NOT NULL,
  name varchar(100) NOT NULL,
  system_prompt text NOT NULL,
  version varchar(20) NOT NULL DEFAULT '1.0',
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE(agent_type, name, version)
);

CREATE TABLE IF NOT EXISTS agent_tasks (
  id bigserial PRIMARY KEY,
  agent_type varchar(50) NOT NULL,
  title varchar(255) NOT NULL,
  description text NOT NULL,
  input_data jsonb NOT NULL DEFAULT '{}',
  output_data jsonb NOT NULL DEFAULT '{}',
  status varchar(20) NOT NULL DEFAULT 'PENDING',
  priority integer NOT NULL DEFAULT 5,
  created_by_id bigint REFERENCES users(id) ON DELETE SET NULL,
  assigned_to_id bigint REFERENCES users(id) ON DELETE SET NULL,
  parent_task_id bigint REFERENCES agent_tasks(id) ON DELETE CASCADE,
  tokens_used integer NOT NULL DEFAULT 0,
  execution_time_seconds decimal(10, 2) NOT NULL DEFAULT 0.0,
  error_message text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  started_at timestamptz,
  completed_at timestamptz
);

CREATE INDEX IF NOT EXISTS agent_tasks_agent_type_status_idx ON agent_tasks(agent_type, status);
CREATE INDEX IF NOT EXISTS agent_tasks_created_by_status_idx ON agent_tasks(created_by_id, status);
CREATE INDEX IF NOT EXISTS agent_tasks_priority_created_at_idx ON agent_tasks(priority, created_at);

CREATE TABLE IF NOT EXISTS agent_executions (
  id bigserial PRIMARY KEY,
  task_id bigint NOT NULL REFERENCES agent_tasks(id) ON DELETE CASCADE,
  agent_type varchar(50) NOT NULL,
  provider_id bigint REFERENCES ai_providers(id) ON DELETE SET NULL,
  prompt_used_id bigint REFERENCES prompts(id) ON DELETE SET NULL,
  input_tokens integer NOT NULL DEFAULT 0,
  output_tokens integer NOT NULL DEFAULT 0,
  total_tokens integer NOT NULL DEFAULT 0,
  execution_time_seconds decimal(10, 2) NOT NULL DEFAULT 0.0,
  success boolean NOT NULL DEFAULT false,
  error_message text,
  raw_request jsonb NOT NULL DEFAULT '{}',
  raw_response jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS agent_executions_task_id_idx ON agent_executions(task_id);
CREATE INDEX IF NOT EXISTS agent_executions_agent_type_idx ON agent_executions(agent_type);
CREATE INDEX IF NOT EXISTS agent_executions_created_at_idx ON agent_executions(created_at);

ALTER TABLE ai_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE prompts ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_executions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can read providers"
  ON ai_providers FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can read prompts"
  ON prompts FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can read own tasks"
  ON agent_tasks FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can create tasks"
  ON agent_tasks FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Users can read executions"
  ON agent_executions FOR SELECT
  TO authenticated
  USING (true);
