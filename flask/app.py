from middleware import mw_tracker, MWOptions
mw_tracker(
    MWOptions(
        access_token="whkvkobudfitutobptgonaezuxpjjypnejbb",
        target="https://myapp.middleware.io:443",
        service_name="MyPythonApp",
    )
)

from flask import Flask, jsonify

import logging
logging.getLogger().setLevel(logging.INFO)
logging.info("Application initiated successfully.", extra={'Tester': 'Alex'})

app = Flask(__name__)

# Define sample user data dictionary
user_data = {
    "admin": {"name": "Administrator", "role": "admin", "email": "admin@example.com"},
    "user1": {"name": "Test User", "role": "user", "email": "user1@example.com"},
    "demo": {"name": "Demo Account", "role": "guest", "email": "demo@example.com"}
}

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
    print(f"User profile requested for {username}")
    if username not in user_data:
        return jsonify({"error": f"User '{username}' not found"}), 404
    
    user_info = user_data[username]
    if not user_info:
        return jsonify({"error": "User data is empty"}), 400
        
    return jsonify({"message": f"Profile for {username}", "data": user_info})


if __name__ == '__main__':
    app.run('0.0.0.0', 8010)