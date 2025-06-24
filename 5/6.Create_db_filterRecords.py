#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API

import os
import numpy as np
from opensearchpy import OpenSearch
from Create_db import generate_embeddings # Python file of Step-1
from openai import OpenAI
from dotenv import load_dotenv

openai_client = OpenAI()
load_dotenv()
host = os.environ.get('OPENSEARCH_HOST')
port = os.environ.get('OPENSEARCH_PORT')
username = os.environ.get('OPENSEARCH_USERNAME')
password = os.environ.get('OPENSEARCH_PASSWORD')

# OpenSearch configuration
OPENSEARCH_CONFIG = {
    "hosts": [{"host": host, "port": port}],
    "http_auth": (username, password),
    "http_compress": True,
    "use_ssl": True,
    "verify_certs": False,
    "ssl_assert_hostname": False,
    "ssl_show_warn": False
}

INDEX_NAME = "funfacts"

# Function to retrieve documents from OpenSearch based on cosine similarity
def retrieve_matching_documents(opensearch_client, user_query, limit=3):
    # Generate the embedding for the query
    user_query_embedding = generate_embeddings(user_query)[0]
    # Perform the OpenSearch search to get all documents   
    search_body = {        
        "_source": ["content"],  # Only retrieve necessary fields
        "query": {
            "knn": {
                "fact_embedding":{
                    "vector": user_query_embedding,
                    "k": limit,
                }
            }
        }
    }    
    response = opensearch_client.search(index=INDEX_NAME, body=search_body)    
    # Extract documents and their embeddings
    documents_string = ''
    # # match_all query returns all documents, so we need to filter based on cosine similarity
    for hit in response["hits"]["hits"]:
        doc = hit["_source"]
        documents_string += doc['content']
    return documents_string

# Main function for testing
def main():
    # User query for information
    #user_query = "I want to learn about animal sleep patterns"
    #user_query = "I want to learn about Human anotomy"
    user_query = "Friendship and Love are same or different?"

    # Connect to OpenSearch
    opensearch_client = OpenSearch(**OPENSEARCH_CONFIG)

    # Retrieve documents based on the user query
    retrieved_maching_string = retrieve_matching_documents(opensearch_client, user_query, limit=4)
 
    print('---------------------------------- Retrieved Documents ----------------------------------')
    for ele in retrieved_maching_string.split('.'):
        print(ele, sep='\n')
    print('---------------------------------------------------------------------------------------------------')

if __name__ == "__main__":
    main()
