from middleware import mw_tracker, MWOptions
# mw_tracker(
#     MWOptions(
#         access_token="whkvkobudfitutobptgonaezuxpjjypnejbb",
#         target="https://myapp.middleware.io:443",
#         service_name="MyPythonApp",
#     )
# )

from flask import Flask

import logging
import sys
from test import sample_function, another_function
logging.getLogger().setLevel(logging.INFO)
logging.info("Application initiated successfully.", extra={'Tester': 'Alex'})

app = Flask(__name__)

@app.route('/')
def hello_world():
    logging.error("error log sample", extra={'CalledFunc': 'hello_world'})
    logging.warning("warning log sample")
    logging.info("info log sample")
    return 'Hello World!'

@app.route('/exception-new')
def generate_exception():
    print("Exception generated ......")
    sample_function()

if __name__ == '__main__':
    app.run('0.0.0.0', 8010)