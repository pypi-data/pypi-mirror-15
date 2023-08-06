CREATE FUNCTION pgtask.fire_row_change_events(target_table regclass) RETURNS void AS $$
    BEGIN
        EXECUTE 'CREATE TRIGGER ' ||
            quote_ident('pgtask_row_change:insert:' || target_table::text) || 
            ' AFTER INSERT ON ' || quote_ident(target_table::text) ||
            ' FOR EACH ROW EXECUTE PROCEDURE pgtask.fire_row_changed_event()';

        EXECUTE 'CREATE TRIGGER ' ||
            quote_ident('pgtask_row_change:update:' || target_table::text) || 
            ' AFTER UPDATE ON ' || quote_ident(target_table::text) ||
            ' FOR EACH ROW WHEN (OLD IS DISTINCT FROM NEW)' ||
            ' EXECUTE PROCEDURE pgtask.fire_row_changed_event()';

        EXECUTE 'CREATE TRIGGER ' ||
            quote_ident('pgtask_row_change:delete:' || target_table::text) || 
            ' AFTER DELETE ON ' || quote_ident(target_table::text) ||
            ' FOR EACH ROW EXECUTE PROCEDURE pgtask.fire_row_changed_event()';
    END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION pgtask.fire_row_changed_event() RETURNS trigger AS $$
    import json
    if 'select_plan' not in SD:
        SD['select_plan'] = plpy.prepare(
            "SELECT pgtask.publish_event($1, $2)", ['text', 'json'])

    event_name = "pgtask_row_changed in table {}.{}".format(
        TD['table_schema'], TD['table_name'])

    event_data = {'old_row': TD['old'], 'new_row': TD['new']}

    plpy.execute(SD['select_plan'], [event_name, json.dumps(event_data)])
$$ LANGUAGE plpython3u;
