/*
  # Create Django Auth Support Tables

  1. New Tables
    - `user_permissions` - User-specific permissions
    - `django_content_type` - Content types
    - `auth_permission` - Permissions
    - `auth_group` - Groups
    - `auth_group_permissions` - Group permissions
    - `users_groups` - User-group relationships
    - `users_user_permissions` - User-permission relationships
*/

CREATE TABLE IF NOT EXISTS django_content_type (
  id serial PRIMARY KEY,
  app_label varchar(100) NOT NULL,
  model varchar(100) NOT NULL,
  UNIQUE(app_label, model)
);

CREATE TABLE IF NOT EXISTS auth_permission (
  id serial PRIMARY KEY,
  name varchar(255) NOT NULL,
  content_type_id integer NOT NULL REFERENCES django_content_type(id),
  codename varchar(100) NOT NULL,
  UNIQUE(content_type_id, codename)
);

CREATE TABLE IF NOT EXISTS auth_group (
  id serial PRIMARY KEY,
  name varchar(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS auth_group_permissions (
  id bigserial PRIMARY KEY,
  group_id integer NOT NULL REFERENCES auth_group(id),
  permission_id integer NOT NULL REFERENCES auth_permission(id),
  UNIQUE(group_id, permission_id)
);

CREATE TABLE IF NOT EXISTS users_groups (
  id bigserial PRIMARY KEY,
  hishamosuser_id bigint NOT NULL REFERENCES users(id),
  group_id integer NOT NULL REFERENCES auth_group(id),
  UNIQUE(hishamosuser_id, group_id)
);

CREATE TABLE IF NOT EXISTS users_user_permissions (
  id bigserial PRIMARY KEY,
  hishamosuser_id bigint NOT NULL REFERENCES users(id),
  permission_id integer NOT NULL REFERENCES auth_permission(id),
  UNIQUE(hishamosuser_id, permission_id)
);

CREATE TABLE IF NOT EXISTS user_permissions (
  id bigserial PRIMARY KEY,
  user_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  permission_name varchar(100) NOT NULL,
  resource_type varchar(50) NOT NULL,
  resource_id varchar(100),
  granted_at timestamptz NOT NULL DEFAULT now(),
  granted_by_id bigint REFERENCES users(id) ON DELETE SET NULL,
  UNIQUE(user_id, permission_name, resource_type, resource_id)
);

ALTER TABLE user_permissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own permissions"
  ON user_permissions FOR SELECT
  TO authenticated
  USING (true);
