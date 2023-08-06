CREATE TYPE pgtask.task_log_level AS ENUM (
    'ERROR', 'WARNING', 'INFO', 'DEBUG');


CREATE TABLE pgtask.task_log (
    id serial PRIMARY KEY,

    task_id integer NOT NULL REFERENCES pgtask.task ON DELETE CASCADE,
    timestamp timestamp with time zone NOT NULL
        DEFAULT statement_timestamp(),
    level pgtask.task_log_level NOT NULL,
    message text NOT NULL
);


CREATE FUNCTION pgtask.task_log_task_insert() RETURNS trigger AS $$
    if 'insert_plan' not in SD:
        SD['insert_plan'] = plpy.prepare(
            "INSERT INTO pgtask.task_log (task_id, level, message) VALUES "
            "($1, 'INFO', $2)", ['integer', 'text'])

    msg = (
        "New '{status}' task created with progress '{progress}', "
        "embargoed until '{embargo}'")
    msg = msg.format(
        status=TD['new']['status'], progress=TD['new']['progress'],
        embargo=TD['new']['embargo'])

    plpy.execute(SD['insert_plan'], [TD['new']['id'], msg])
$$ LANGUAGE plpython3u;

CREATE TRIGGER task_log_task_insert
    AFTER INSERT ON pgtask.task
    FOR EACH ROW
    EXECUTE PROCEDURE pgtask.task_log_task_insert();


CREATE FUNCTION pgtask.task_log_task_status_change() RETURNS trigger AS $$
    if 'insert_plan' not in SD:
        SD['insert_plan'] = plpy.prepare(
            "INSERT INTO pgtask.task_log (task_id, level, message) VALUES "
            "($1, 'INFO', $2)", ['integer', 'text'])

    msg = "Status changed from '{old}' to '{new}'"
    msg = msg.format(old=TD['old']['status'], new=TD['new']['status'])

    plpy.execute(SD['insert_plan'], [TD['new']['id'], msg])
$$ LANGUAGE plpython3u;

CREATE TRIGGER task_log_task_status_change
    AFTER UPDATE ON pgtask.task
    FOR EACH ROW WHEN (NEW.status IS DISTINCT FROM OLD.status)
    EXECUTE PROCEDURE pgtask.task_log_task_status_change();


CREATE FUNCTION pgtask.task_log_task_progress_change() RETURNS trigger AS $$
    if 'insert_plan' not in SD:
        SD['insert_plan'] = plpy.prepare(
            "INSERT INTO pgtask.task_log (task_id, level, message) VALUES "
            "($1, 'INFO', $2)", ['integer', 'text'])

    msg = "Progress changed from '{old}' to '{new}'"
    msg = msg.format(old=TD['old']['progress'], new=TD['new']['progress'])

    plpy.execute(SD['insert_plan'], [TD['new']['id'], msg])
$$ LANGUAGE plpython3u;

CREATE TRIGGER task_log_task_progress_change
    AFTER UPDATE ON pgtask.task
    FOR EACH ROW WHEN (NEW.progress IS DISTINCT FROM OLD.progress)
    EXECUTE PROCEDURE pgtask.task_log_task_progress_change();


CREATE FUNCTION pgtask.task_log_task_embargo_change() RETURNS trigger AS $$
    if 'insert_plan' not in SD:
        SD['insert_plan'] = plpy.prepare(
            "INSERT INTO pgtask.task_log (task_id, level, message) VALUES "
            "($1, 'INFO', $2)", ['integer', 'text'])

    msg = "Embargo changed from '{old}' to '{new}'"
    msg = msg.format(old=TD['old']['embargo'], new=TD['new']['embargo'])

    plpy.execute(SD['insert_plan'], [TD['new']['id'], msg])
$$ LANGUAGE plpython3u;

CREATE TRIGGER task_log_task_embargo_change
    AFTER UPDATE ON pgtask.task
    FOR EACH ROW WHEN (NEW.embargo IS DISTINCT FROM OLD.embargo)
    EXECUTE PROCEDURE pgtask.task_log_task_embargo_change();
