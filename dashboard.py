from flask import Flask, render_template, jsonify
from boto.sqs.message import Message
import dashboard_data_access
import boto.sqs
import json
from optparse import OptionParser
import settings as settings_lib

global ENV
global settings

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    articles = None
    try:
        articles = dashboard_data_access.get_items()
    except Exception as e:
        print e
    if articles is not None:
        return render_template('index.html', articles=articles)
    # TODO handle errors


@app.route('/event/<string:item_identifier>')
def item_events(item_identifier):
    # TODO validate item_identifier against regexp to prevent possible attack vector
    events = None
    try:
        events = dashboard_data_access.get_events_for_item(item_identifier)
    except Exception as e:
        print e
    if events is not None:
        return render_template('events.html', events=events, item_identifier=item_identifier)
    # TODO: handle errors


@app.route('/publish/<string:version_id>', methods=['POST', 'GET'])
def publish_item(version_id):
    if version_id is not None:
        try:
            message = {'workflow_name': 'ApproveArticlePublication',
                       'workflow_data': {'article_version_id': version_id}}
            message_string = json.dumps(message)
            conn = boto.sqs.connect_to_region(settings.sqs_region,
                                      aws_access_key_id=settings.aws_access_key_id,
                                      aws_secret_access_key=settings.aws_secret_access_key)
            queue = conn.get_queue(settings.workflow_starter_queue)

            m = Message()
            m.set_body(message_string)
            queue.write(m)
        except Exception as e:
            print e
    return jsonify({'message': 'publication request submitted'})


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-e", "--env", default="dev", action="store", type="string", dest="env", help="set the environment to run, either dev or live")
    (options, args) = parser.parse_args()
    if options.env:
        ENV = options.env
    settings = settings_lib.get_settings(ENV)
    app.run()
