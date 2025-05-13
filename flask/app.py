from middleware import mw_tracker, MWOptions
mw_tracker(
    MWOptions(
        access_token="mgqjtlgshkyhlykoaermkzbjpmgprkrzmbsb",
        target="https://sbncr.stage.env.middleware.io",
        service_name="flask-app",
    )
)

from flask import Flask

import logging
logging.getLogger().setLevel(logging.INFO)
logging.info("Application initiated successfully.", extra={'Tester': 'Alex'})

app = Flask(__name__)

@app.route('/')
def hello_world():
    logging.error("error log sample", extra={'CalledFunc': 'hello_world'})
    logging.warning("warning log sample")
    logging.info("info log sample")
    return 'Hello World!'

@app.route('/exception')
def generate_exception():
    randomList = ['a', 0, 2]

    for entry in randomList:
        try:
            print("The entry is", entry)
            r = 1/int(entry)
            break
        except Exception as e:
            tracker.record_error(e)
    print("The reciprocal of", entry, "is", r)
    return 'Exception Generated!'

@app.route('/greeting')
def greeting():
    greeting_message = "Hello User, Your request id is" + str(5000)
    return greeting_message

if __name__ == '__main__':
    app.run('0.0.0.0', 8010)