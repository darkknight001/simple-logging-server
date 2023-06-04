CREATE DATABASE ActivityLog;

\c ActivityLog;

CREATE TABLE logs (
  id INTEGER,
  unix_ts INTEGER,
  user_id INTEGER,
  event_name VARCHAR(255)
);