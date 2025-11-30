/*
  # Create Users Table

  1. New Tables
    - `users` (extends Django's auth)
      - `id` (bigserial, primary key)
      - `password` (varchar)
      - `last_login` (timestamptz, nullable)
      - `is_superuser` (boolean)
      - `username` (varchar, unique)
      - `first_name` (varchar)
      - `last_name` (varchar)
      - `email` (varchar, unique)
      - `is_staff` (boolean)
      - `is_active` (boolean)
      - `date_joined` (timestamptz)
      - `role` (varchar)
      - `avatar` (varchar, nullable)
      - `preferences` (jsonb)
      - `ai_token_limit` (integer)
      - `ai_tokens_used` (integer)
      - `last_token_reset` (timestamptz)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)

  2. Security
    - Enable RLS on `users` table
    - Add policy for users to read their own data
*/

CREATE TABLE IF NOT EXISTS users (
  id bigserial PRIMARY KEY,
  password varchar(128) NOT NULL,
  last_login timestamptz,
  is_superuser boolean NOT NULL DEFAULT false,
  username varchar(150) NOT NULL UNIQUE,
  first_name varchar(150) NOT NULL DEFAULT '',
  last_name varchar(150) NOT NULL DEFAULT '',
  email varchar(254) NOT NULL UNIQUE,
  is_staff boolean NOT NULL DEFAULT false,
  is_active boolean NOT NULL DEFAULT true,
  date_joined timestamptz NOT NULL DEFAULT now(),
  role varchar(20) NOT NULL DEFAULT 'DEVELOPER',
  avatar varchar(500),
  preferences jsonb NOT NULL DEFAULT '{}',
  ai_token_limit integer NOT NULL DEFAULT 100000,
  ai_tokens_used integer NOT NULL DEFAULT 0,
  last_token_reset timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS users_username_idx ON users(username);
CREATE INDEX IF NOT EXISTS users_email_idx ON users(email);
CREATE INDEX IF NOT EXISTS users_created_at_idx ON users(created_at);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own data"
  ON users FOR SELECT
  TO authenticated
  USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own data"
  ON users FOR UPDATE
  TO authenticated
  USING (auth.uid()::text = id::text)
  WITH CHECK (auth.uid()::text = id::text);
