/*
  # Create Django System Tables

  1. New Tables
    - `django_migrations` - Track migrations
    - `django_session` - Session storage
    - `django_admin_log` - Admin action logs
*/

CREATE TABLE IF NOT EXISTS django_migrations (
  id bigserial PRIMARY KEY,
  app varchar(255) NOT NULL,
  name varchar(255) NOT NULL,
  applied timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS django_session (
  session_key varchar(40) PRIMARY KEY,
  session_data text NOT NULL,
  expire_date timestamptz NOT NULL
);

CREATE INDEX IF NOT EXISTS django_session_expire_date_idx ON django_session(expire_date);

CREATE TABLE IF NOT EXISTS django_admin_log (
  id serial PRIMARY KEY,
  action_time timestamptz NOT NULL DEFAULT now(),
  object_id text,
  object_repr varchar(200) NOT NULL,
  action_flag smallint NOT NULL,
  change_message text NOT NULL,
  content_type_id integer REFERENCES django_content_type(id),
  user_id bigint NOT NULL REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS django_admin_log_user_id_idx ON django_admin_log(user_id);
CREATE INDEX IF NOT EXISTS django_admin_log_content_type_id_idx ON django_admin_log(content_type_id);
