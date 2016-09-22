from flask import Flask
import logging

# set the logging mechanism
logging.basicConfig(filename="/var/log/event_log",
                   level = logging.DEBUG)

app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World!"
@app.route("/start_kodi")
def start_kodi():
    logging.info("Kodi started successfully!")
    return "All OK"

def read_and_format_log():
    with open("/var/log/event_log") as f:
        return  f.read().replace('\n', '<br>')

@app.route("/retrieve_log")
def retrieve_log():
    return read_and_format_log()

if __name__ == '__main__':
    app.run(port=5001)


