CREATE TYPE pgtask.task_status AS ENUM (
    'pending', 'processing', 'completed', 'failed');

CREATE TABLE pgtask.task (
    id serial PRIMARY KEY,

    created timestamp with time zone NOT NULL
        DEFAULT statement_timestamp(),
    embargo timestamp with time zone NOT NULL
        DEFAULT statement_timestamp(),

    consumer_id integer NOT NULL REFERENCES pgtask.consumer ON DELETE CASCADE,
    event text NOT NULL,

    event_data json,

    status pgtask.task_status NOT NULL,
    progress integer CHECK (progress BETWEEN 0 AND 100)
);


CREATE FUNCTION pgtask.consumer_task() RETURNS trigger AS $$
    consumer_task_notification_channel = (
        "pgtask:consumer_{}_task".format(TD['new']['consumer_id']))
    plpy.execute("NOTIFY \"{}\", '{}'".format(
        consumer_task_notification_channel, TD['new']['id']))
$$ LANGUAGE plpython3u;

CREATE TRIGGER consumer_task
    AFTER INSERT OR UPDATE ON pgtask.task
    FOR EACH ROW WHEN (NEW.status = 'pending')
    EXECUTE PROCEDURE pgtask.consumer_task();


CREATE FUNCTION pgtask.publish_event(event text, event_data json DEFAULT null, embargo timestamp with time zone DEFAULT statement_timestamp()) RETURNS void AS $$
    if 'select_plan' not in SD:
        SD['select_plan'] = plpy.prepare(
            "SELECT consumer_id FROM pgtask.subscription WHERE event=$1",
            ['text'])

    if 'insert_plan' not in SD:
        SD['insert_plan'] = plpy.prepare(
            "INSERT INTO pgtask.task (embargo, consumer_id, event, "
            "event_data, status) VALUES ($1, $2, $3, $4, 'pending')",
            ['timestamp with time zone', 'integer', 'text', 'json'])

    consumers = plpy.execute(SD['select_plan'], [event])
    consumer_ids = [consumer['consumer_id'] for consumer in consumers]

    for consumer_id in consumer_ids:
        plpy.execute(
            SD['insert_plan'], [embargo, consumer_id, event, event_data])
$$ LANGUAGE plpython3u;


CREATE FUNCTION pgtask.publish_task(consumer_id integer, event text, event_data json DEFAULT null, embargo timestamp with time zone DEFAULT statement_timestamp()) RETURNS void AS $$
    if 'insert_plan' not in SD:
        SD['insert_plan'] = plpy.prepare(
            "INSERT INTO pgtask.task (embargo, consumer_id, event, "
            "event_data, status) VALUES ($1, $2, $3, $4, 'pending')",
            ['timestamp with time zone', 'integer', 'text', 'json'])

    plpy.execute(SD['insert_plan'], [embargo, consumer_id, event, event_data])
$$ LANGUAGE plpython3u;
