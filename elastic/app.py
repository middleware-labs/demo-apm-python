
# app.py

from middleware import MwTracker
MwTracker()

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from search import Search
import os

import logging
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)

# Initialize the Search class with Cloud ID and Password
es = Search()

# Sample data to index
documents = [
    {"content": "Elasticsearch is a distributed, RESTful search and analytics engine."},
    {"content": "Python is a programming language that lets you work quickly."},
    {"content": "Flask is a micro web framework for Python."},
    {"content": "Data science is an interdisciplinary field that uses scientific methods."},
]

# Index sample documents on startup
index_name = "sample_index"
es.index_documents(index_name, documents)

@app.route('/myroute', methods=['GET', 'POST'])
def index():
    account_key = os.getenv('RUM_ACCOUNT_KEY', '')
    target = os.getenv('RUM_TARGET', '')
    logging.info("Inside Index Func.", extra={'myroute': 'index'})
    results = []
    if request.method == 'POST':
        query = request.form.get('query', '')
        results = es.search(index_name, query)
        return render_template('index.html', query=query, results=results)
    return render_template('index.html', query='', results=[],account_key=account_key,target=target)

@app.route("/health", methods=["GET"])
def health_check():
    logging.info("Health Check Initiated")
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    logging.info("APP Run.")
    CORS(app) 
    app.run(port=4000)