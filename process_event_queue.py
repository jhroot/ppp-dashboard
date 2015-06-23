"""
Process SQS message from event and property queue and populate monitoring database
"""
import settings as settings_lib
from optparse import OptionParser
import log
import boto.sqs
from multiprocessing import Pool
from functools import partial
import json

settings = {}
logger = {}

def main():
    parser = OptionParser()
    parser.add_option("-e", "--env", default="dev", action="store", type="string", dest="env",
                      help="set the environment to run, either dev or live")
    (options, args) = parser.parse_args()
    if options.env:
        env = options.env

    global settings
    settings = settings_lib.get_settings(env)

    log_file = "process_event_queue.log"
    global logger
    logger = log.logger(log_file, settings.log_level)

    # Simple connect
    conn = boto.sqs.connect_to_region(settings.sqs_region,
                                      aws_access_key_id=settings.aws_access_key_id,
                                      aws_secret_access_key=settings.aws_secret_access_key)
    queue = conn.get_queue(settings.event_monitor_queue)

    pool = Pool(settings.event_queue_pool_size)

    while True:
        messages = queue.get_messages(num_messages=settings.event_queue_message_count, visibility_timeout=60,
                                      wait_time_seconds=20)
        if messages is not None:
            logger.info(str(len(messages)) + " message received")
            pool.map(process_message, messages)
        else:
            logger.info("No messages received")


def process_message(message):
    message_payload = json.loads(message.get_body())
    message_type = message_payload.get('message-type')
    if message_type is not None:
        if message_type in dispatch:
            dispatch[message_type](message_payload)
        else:
            logger.error('Unknown message type ' + message_type)

def process_event_message(message):
    print message['item-identifier']

def process_property_message(message):
    pass

dispatch = {'event': process_event_message, 'property': process_property_message}


if __name__ == "__main__":
    main()
