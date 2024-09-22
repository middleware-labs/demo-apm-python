
# search.py

from elasticsearch import Elasticsearch
import logging
logging.getLogger().setLevel(logging.INFO)


class Search:
    def __init__(self):
        logging.info("ES Connect.", extra={'es': 'connect'})

        # Connect to Elasticsearch Cloud
        self.es = Elasticsearch(
            "https://e54bffae04f54f3cbe8fff59514134b6.us-central1.gcp.cloud.es.io:443",
            api_key="MlM2RUQ1SUJCeW15emhfOVplQUs6d3BrSllVOThRLVNfTGVlZ0Fld3pvQQ"
        )
        if not self.es.ping():
            logging.info("Ping fail.")
            raise ValueError("Connection failed")
        print("Connected to Elasticsearch!")

    def index_documents(self, index_name, documents):
        logging.info("Indexing Documents.")
        # Create the index if it doesn't exist
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name)

        # Index sample documents
        for i, doc in enumerate(documents):
            self.es.index(index=index_name, id=i + 1, body=doc)

    def search(self, index_name, query):
        # Perform a search query
        logging.info("Query Search")

        response = self.es.search(index=index_name, body={
            "query": {
                "match": {
                    "content": query
                }
            }
        })
        return response['hits']['hits']    