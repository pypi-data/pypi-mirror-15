CREATE TABLE pgtask.subscription (
    id serial PRIMARY KEY,
    consumer_id integer NOT NULL REFERENCES pgtask.consumer ON DELETE CASCADE,
    event text NOT NULL,

    UNIQUE (consumer_id, event)
);

CREATE FUNCTION pgtask.update_subscriptions(consumer_id integer, events text[]) RETURNS void AS $$
    if 'select_plan' not in SD:
        SD['select_plan'] = plpy.prepare(
            "SELECT event FROM pgtask.subscription WHERE consumer_id=$1",
            ['integer'])

    if 'delete_plan' not in SD:
        SD['delete_plan'] = plpy.prepare(
            "DELETE FROM pgtask.subscription WHERE consumer_id=$1 AND "
            "event=$2", ['integer', 'text'])

    if 'insert_plan' not in SD:
        SD['insert_plan'] = plpy.prepare(
            "INSERT INTO pgtask.subscription (consumer_id, event) VALUES "
            "($1, $2)", ['integer', 'text'])

    wanted_events = set(events)

    subscriptions = plpy.execute(SD['select_plan'], [consumer_id])
    subscribed_events = {x['event'] for x in subscriptions}

    for unwanted_event in subscribed_events - wanted_events:
        plpy.execute(SD['delete_plan'], [consumer_id, unwanted_event])
        
    for wanted_event in wanted_events - subscribed_events:
        plpy.execute(SD['insert_plan'], [consumer_id, wanted_event])
$$ LANGUAGE plpython3u;
