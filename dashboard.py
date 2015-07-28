from flask import Flask, render_template
import dashboard_data_access

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

if __name__ == '__main__':
    app.run()
