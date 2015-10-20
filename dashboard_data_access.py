import psycopg2
import datetime

store_event_sql = 'insert into event (version, run, type, timestamp, status, message, item_id, message_id) ' \
                  'select %s, %s, %s, %s, %s, %s, %s, %s where not exists ' \
                  '(select * from event where message_id = %s)'


store_property_sql = 'insert into property (property_type, name, int_value, date_value, text_value, item_id, message_id, ' \
                     ' version) select %s, %s, %s, %s, %s, %s, %s, %s where not exists ' \
                     '(select * from event where message_id = %s)'

update_property_sql = 'update property set property_type=%s, int_value=%s, date_value=%s, text_value = %s, message_id = ' \
                      '%s, version=%s where property_id = %s'

property_id_sql = 'select property_id  from property where name=%s and item_id=%s and version=%s '

get_item_sql = 'select item_id from item where item_identifier = %s'

insert_item_sql = 'insert into item (item_identifier) values (%s) returning item_id'

get_items_sql = 'SELECT item_id, item_identifier FROM item'

get_item_properties_sql = 'select property_id, name, int_value, text_value, date_value, property_type, version from property ' \
                          'where item_id = %s'

get_events_for_item_sql = 'select event_id, version, run, type, timestamp, status, message from event ' \
                          'where item_id = %s'


def get_items(with_properties=True):
    items = []
    conn, cur = get_connection()
    cur.execute(get_items_sql)
    rows = cur.fetchall()
    if rows is not None:
        for row in rows:
            items.append(get_item_from_row(row))
    if with_properties:
        items = add_properties(items)
    return items


def get_item_from_row(row):
    item = {'item_id': row[0], 'item_identifier': row[1]}
    return item


def add_properties(items):
    # TODO this data could be retrieved in a single query
    conn, cur = get_connection()
    for item in items:
        item_properties = {}
        cur.execute(get_item_properties_sql, (item.get('item_id'),))
        properties = cur.fetchall()
        for prop in properties:
            value = None
            property_type = prop[5]
            if property_type == 'int':
                value = prop[2]
            elif property_type == 'text':
                value = prop[3]
            elif property_type == 'date':
                value = prop[4]
            name = prop[1]
            property_id = prop[0]
            property_version = prop[6]
            if name is not None and value is not None:
                version_properties = item_properties.get(property_version)
                if version_properties is None:
                    version_properties = {}
                    item_properties[property_version] = version_properties
                version_properties[name] = ({'id': property_id, 'value': value})
        item['properties'] = item_properties
    return items


def get_events_for_item(item_identifier):
    raw_events = []
    item_id = get_item_id(item_identifier)
    if item_id is not None:
        conn, cur = get_connection()
        cur.execute(get_events_for_item_sql, (item_id,))
        rows = cur.fetchall()
        if rows is not None:
            for row in rows:
                raw_events.append(get_event_from_row(row))
    events = {}
    for event in raw_events:
        version = str(event.get('version'))
        run = str(event.get('run'))
        if version is not None and run is not None:
            if version not in events:
                events[version] = {}
            if run not in events[version]:
                events[version][run] = []
            events[version][run].append(event)
    else:
        pass  # TODO: handle
    return events


def get_event_from_row(row):
    event = {'event_id': row[0], 'version': row[1], 'run': row[2], 'event_type': row[3], 'timestamp': row[4],
             'status': row[5], 'message': row[6]}
    return event


def get_item_id(item_identifier, add=False):
    conn, cur = get_connection()

    cur.execute(get_item_sql, (item_identifier,))
    result = cur.fetchone()
    if result is None:
        if (add):
            cur.execute(insert_item_sql, (item_identifier,))
            item_id = cur.fetchone()[0]
        else:
            item_id = None
    else:
        item_id = result[0]
    conn.commit()
    cur.close()
    conn.close()
    return item_id


def store_event(version, run, event_type, timestamp, status, message, item_identifier, message_id):
    conn, cur = get_connection()

    item_id = get_item_id(item_identifier, add=True)
    cur.execute(store_event_sql,
                (version, run, event_type, timestamp, status, message, item_id, message_id, message_id))
    conn.commit()
    cur.close()
    conn.close()


def store_property(property_type, name, value, item_identifier, version, message_id):
    conn, cur = get_connection()
    if version is None:
        version = 0
    item_id = get_item_id(item_identifier, add=True)
    int_value = None
    date_value = None
    text_value = None
    if property_type == 'text':
        text_value = value
    elif property_type == 'date':
        text_value = datetime.datetime(value)
    elif property_type == 'int':
        int_value = int(value)
    else:
        # TODO: log error
        return

    cur.execute(property_id_sql, (name, item_id , version))
    conn.commit()
    row = cur.fetchone()
    if row is None:
        cur.execute(store_property_sql,
                    (property_type, name, int_value, date_value, text_value, item_id, message_id, version, message_id))
    else:
        property_id = row[0]
        cur.execute(update_property_sql, (property_type, int_value, date_value, text_value, message_id, version,
                                          property_id))
    conn.commit()
    cur.close()
    conn.close()


def get_connection():
    conn = psycopg2.connect(database='elifemonitoring',
                            user='elifemonitor',
                            host='elifemonitor.cts3ortehubv.eu-west-1.rds.amazonaws.com',
                            password='elifemonitor6')
    cur = conn.cursor()
    return conn, cur


def main():
    e = get_events_for_item('00001')
    print len(e)

if __name__ == "__main__":
    main()
