CREATE TABLE pgtask.consumer (
    id serial PRIMARY KEY,
    name text NOT NULL UNIQUE,

    last_started timestamp with time zone
);

CREATE FUNCTION pgtask.register_consumer(name text) RETURNS integer AS $$
    if 'select_plan' not in SD:
        SD['select_plan'] = plpy.prepare(
            "SELECT id FROM pgtask.consumer WHERE name=$1", ['text'])

    ids = plpy.execute(SD['select_plan'], [name])
    if len(ids) == 1:
        return ids[0]['id']


    if 'insert_plan' not in SD:
        SD['insert_plan'] = plpy.prepare(
            "INSERT INTO pgtask.consumer (name) VALUES ($1) RETURNING id",
            ['text'])

    return plpy.execute(SD['insert_plan'], [name])[0]['id']
$$ LANGUAGE plpython3u;

CREATE FUNCTION pgtask.start_consumer(consumer_id integer) RETURNS void AS $$
    # Attempt to avoid duplicate instances of same consumer
    consumer_started_notification_channel = (
        "pgtask:consumer_{}_started".format(consumer_id))
    plpy.execute("LISTEN \"{}\"".format(consumer_started_notification_channel))
    plpy.execute("NOTIFY \"{}\"".format(consumer_started_notification_channel))

    # Listen for notification of new pending tasks
    consumer_task_notification_channel = (
        "pgtask:consumer_{}_task".format(consumer_id))
    plpy.execute("LISTEN \"{}\"".format(consumer_task_notification_channel))

    if 'update_plan' not in SD:
        SD['update_plan'] = plpy.prepare(
            "UPDATE pgtask.consumer SET last_started=transaction_timestamp() "
            "WHERE id=$1", ['integer'])

    plpy.execute(SD['update_plan'], [consumer_id])

    # Tasks that were being processed by a (presumed-dead) instance are failed
    if 'fail_tasks_plan' not in SD:
        SD['fail_tasks_plan'] = plpy.prepare(
            "UPDATE pgtask.task SET status='failed' WHERE consumer_id=$1 AND "
            "status='processing' RETURNING id", ['integer'])

    if 'log_task_failure_plan' not in SD:
        SD['log_task_failure_plan'] = plpy.prepare(
            "INSERT INTO pgtask.task_log (task_id, level, message) VALUES "
            "($1, 'ERROR', 'Task was found ''processing'' during consumer "
            "startup - marking as ''failed''')", ['integer'])

    tasks = plpy.execute(SD['fail_tasks_plan'], [consumer_id])
    task_ids = [task['id'] for task in tasks]

    for task_id in task_ids:
        plpy.execute(SD['log_task_failure_plan'], [task_id])
$$ LANGUAGE plpython3u;
