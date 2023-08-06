\set ON_ERROR_STOP on

BEGIN;

CREATE SCHEMA pgtask;

CREATE EXTENSION plpython3u;

\i consumer.sql
\i subscription.sql

\i task.sql
\i task_log.sql

\i row_change_helper.sql

\i permissions.sql


COMMIT;
