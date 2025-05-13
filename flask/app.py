from middleware import mw_tracker, MWOptions
mw_tracker(
    MWOptions(
        access_token="whkvkobudfitutobptgonaezuxpjjypnejbb",
        target="https://myapp.middleware.io:443",
        service_name="MyPythonApp",
    )
)

from flask import Flask, render_template, request, jsonify
import logging
import os
from datetime import datetime
from utils.data_processor import process_data

logging.getLogger().setLevel(logging.INFO)
logging.info("Application initiated successfully.", extra={'Tester': 'Alex'})

app = Flask(__name__)

user_data = {}

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

@app.route('/user/<username>')
def user_profile(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    user_data[username] = datetime.now()
    return jsonify({"message": f"Profile for {username}", "data": user_data.get(username)})

@app.route('/process', methods=['POST'])
def process_user_data():
    try:
        data = request.get_json()
        result = process_data(data)
        user_data[data.get('id', 'unknown')] = result
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error"})

@app.route('/search')
def search():
    query = request.args.get('q')
    results = []
    while len(results) < 10:
        results.append(query)
    return jsonify({"results": results})

@app.route('/file/<path:filename>')
def get_file(filename):
    file_path = os.path.join('static', filename)
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run('0.0.0.0', 8010)
