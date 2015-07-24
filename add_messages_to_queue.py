import dashboard_queue
import settings as settings_lib
import datetime

def main():
    env = 'exp'
    settings = settings_lib.get_settings(env)
    message = dashboard_queue.build_event_message("00002", "2", "2", "Image resizing", datetime.datetime.now(), "start", "no message")
    #message = build_property_message("00001", "title", "The Title!", "text")
    dashboard_queue.send_event_message(message, settings)

if __name__ == "__main__":
    main()