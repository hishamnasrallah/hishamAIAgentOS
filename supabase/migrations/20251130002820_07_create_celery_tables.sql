/*
  # Create Celery Tables

  1. New Tables
    - `django_celery_beat_*` - Celery Beat tables for scheduled tasks
    - `django_celery_results_*` - Celery result backend tables
*/

CREATE TABLE IF NOT EXISTS django_celery_beat_periodictask (
  id serial PRIMARY KEY,
  name varchar(200) NOT NULL UNIQUE,
  task varchar(200) NOT NULL,
  interval_id integer,
  crontab_id integer,
  solar_id integer,
  clocked_id integer,
  args text NOT NULL DEFAULT '[]',
  kwargs text NOT NULL DEFAULT '{}',
  queue varchar(200),
  exchange varchar(200),
  routing_key varchar(200),
  expires timestamptz,
  enabled boolean NOT NULL DEFAULT true,
  last_run_at timestamptz,
  total_run_count integer NOT NULL DEFAULT 0,
  date_changed timestamptz NOT NULL DEFAULT now(),
  description text NOT NULL DEFAULT '',
  one_off boolean NOT NULL DEFAULT false,
  start_time timestamptz,
  priority integer,
  headers text NOT NULL DEFAULT '{}',
  expire_seconds integer
);

CREATE TABLE IF NOT EXISTS django_celery_beat_intervalschedule (
  id serial PRIMARY KEY,
  every integer NOT NULL,
  period varchar(24) NOT NULL
);

CREATE TABLE IF NOT EXISTS django_celery_beat_crontabschedule (
  id serial PRIMARY KEY,
  minute varchar(240) NOT NULL DEFAULT '*',
  hour varchar(96) NOT NULL DEFAULT '*',
  day_of_week varchar(64) NOT NULL DEFAULT '*',
  day_of_month varchar(124) NOT NULL DEFAULT '*',
  month_of_year varchar(64) NOT NULL DEFAULT '*',
  timezone varchar(63) NOT NULL DEFAULT 'UTC'
);

CREATE TABLE IF NOT EXISTS django_celery_beat_solarschedule (
  id serial PRIMARY KEY,
  event varchar(24) NOT NULL,
  latitude numeric(9, 6) NOT NULL,
  longitude numeric(9, 6) NOT NULL
);

CREATE TABLE IF NOT EXISTS django_celery_beat_clockedschedule (
  id serial PRIMARY KEY,
  clocked_time timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS django_celery_beat_periodictasks (
  ident smallint PRIMARY KEY DEFAULT 1,
  last_update timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS django_celery_results_taskresult (
  id serial PRIMARY KEY,
  task_id varchar(255) NOT NULL UNIQUE,
  status varchar(50) NOT NULL,
  content_type varchar(128) NOT NULL,
  content_encoding varchar(64) NOT NULL,
  result text,
  date_done timestamptz NOT NULL DEFAULT now(),
  traceback text,
  meta text,
  task_args text,
  task_kwargs text,
  task_name varchar(255),
  worker varchar(100),
  date_created timestamptz NOT NULL DEFAULT now(),
  periodic_task_name varchar(255)
);

CREATE INDEX IF NOT EXISTS django_celery_results_taskresult_task_id_idx ON django_celery_results_taskresult(task_id);
CREATE INDEX IF NOT EXISTS django_celery_results_taskresult_date_done_idx ON django_celery_results_taskresult(date_done);
CREATE INDEX IF NOT EXISTS django_celery_results_taskresult_status_idx ON django_celery_results_taskresult(status);

CREATE TABLE IF NOT EXISTS django_celery_results_chordcounter (
  id serial PRIMARY KEY,
  group_id varchar(255) NOT NULL UNIQUE,
  sub_tasks text NOT NULL,
  count integer NOT NULL
);
