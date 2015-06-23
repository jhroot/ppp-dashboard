import datetime
import boto.sqs
from boto.sqs.message import Message
import settings as settings_lib
import json


def send_event_message(message, settings):
    conn = boto.sqs.connect_to_region(settings.sqs_region,
                                      aws_access_key_id=settings.aws_access_key_id,
                                      aws_secret_access_key=settings.aws_secret_access_key)
    queue = conn.get_queue(settings.event_monitor_queue)

    m = Message()
    m.set_body(json.dumps(message))
    queue.write(m)


def build_event_message(item_identifier, version, run, event_type, timestamp, status, message):
    message = {
        'message-type': 'event',
        'item-identifier': item_identifier,
        'version': version,
        'run': run,
        'event-type': event_type,
        'timestamp': timestamp.isoformat(),
        'status': status, message: message
    }
    return message


def main():
    env = 'exp'
    settings = settings_lib.get_settings(env)
    message = build_event_message("00001", "1", "1", "Image resizing", datetime.datetime.now(), "start", "")
    send_event_message(message, settings)


if __name__ == "__main__":
    main()
