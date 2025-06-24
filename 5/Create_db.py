#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API
#RAG related code to create a database with OpenSearch and OpenAI Embedding API

import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from openai import OpenAI
openai_client = OpenAI()
load_dotenv()
host = os.environ.get('OPENSEARCH_HOST')
port = os.environ.get('OPENSEARCH_PORT')
username = os.environ.get('OPENSEARCH_USERNAME')
password = os.environ.get('OPENSEARCH_PASSWORD')

# OpenSearch configuration dictionary
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

#funfacts(content,name,fact_embedding)
# Mock documents array with fun facts
# knowledge_base = [
#     {"content": "A group of flamingos is called a 'flamboyance'.", "name": "Fun Fact 1"},
#     {"content": "Octopuses have five hearts.", "name": "Fun Fact 2"},
#     {"content": "Butterflies taste with their feet.", "name": "Fun Fact 3"},
#     {"content": "A snail can sleep for Five years.", "name": "Fun Fact 4"},
#     {"content": "Elephants are the only animals that can't jump.", "name": "Fun Fact 5"},
#     {"content": "A rhinoceros' horn is made of hair.", "name": "Fun Fact 6"},
#     {"content": "Slugs have four noses.", "name": "Fun Fact 7"},
#     {"content": "A cow gives nearly 200,000 glasses of milk in a lifetime.", "name": "Fun Fact 8"},
#     {"content": "Bats are the only mammals that can fly.", "name": "Fun Fact 9"},
#     {"content": "Koalas sleep up to 21 hours a day.", "name": "Fun Fact 10"}
# ]

# knowledge_base = [ 
#     {"content": "The human brain has about 86 billion neurons.", "name": "Human Fact 1"},
#     {"content": "Your nose can detect over 1 trillion different scents.", "name": "Human Fact 2"},
#     {"content": "Humans share approximately 60 of their DNA with bananas.", "name": "Human Fact 3"},
#     {"content": "The average person walks the equivalent of five times around the world in their lifetime.", "name": "Human Fact 4"},
#     {"content": "Your body has more bacterial cells than human cells.", "name": "Human Fact 5"},
#     {"content": "The strongest muscle in the human body relative to size is the masseter (jaw muscle).", "name": "Human Fact 6"},
#     {"content": "Humans are the only species known to blush.", "name": "Human Fact 7"},
#     {"content": "Human bones are about five times stronger than steel of the same density.", "name": "Human Fact 8"},
#     {"content": "The average human heart beats around 100,000 times per day.", "name": "Human Fact 9"},
#     {"content": "Your skin renews itself approximately every 28 days.", "name": "Human Fact 10"}
# ]

knowledge_base = [
    {"content": "Laughter strengthens social bonds and increases group cooperation.", "name": "Friend Fact 1"},
    {"content": "People with strong friendships are generally happier and live longer.", "name": "Friend Fact 2"},
    {"content": "The average person has about 3 to 5 close friends in their lifetime.", "name": "Friend Fact 3"},
    {"content": "Oxytocin, the 'love hormone', is released when we spend time with friends.", "name": "Friend Fact 4"},
    {"content": "True friends can influence your habits more than family.", "name": "Friend Fact 5"},
    {"content": "Sharing secrets and experiences builds deeper friendships.", "name": "Friend Fact 6"},
    {"content": "Friendship boosts mental health and reduces stress.", "name": "Friend Fact 7"},
    {"content": "Childhood friendships help shape social behavior later in life.", "name": "Friend Fact 8"},
    {"content": "Even brief positive interactions with strangers can uplift your mood.", "name": "Friend Fact 9"},
    {"content": "Friends often subconsciously mimic each other's speech and gestures.", "name": "Friend Fact 10"},
    {"content": "Long-distance friendships can be as strong as in-person ones with regular communication.", "name": "Friend Fact 11"},
    {"content": "Spending time with friends can increase dopamine, the feel-good chemical.", "name": "Friend Fact 12"},
    {"content": "Loyalty is rated as the most important trait in a friend across cultures.", "name": "Friend Fact 13"},
    {"content": "Friendships formed during tough times tend to be stronger.", "name": "Friend Fact 14"},
    {"content": "Friends can help boost your self-confidence and motivation.", "name": "Friend Fact 15"},
    {"content": "Pets are often considered best friends by their owners due to emotional bonds.", "name": "Friend Fact 16"},
    {"content": "Friends can help you live healthier by encouraging good habits.", "name": "Friend Fact 17"},
    {"content": "Social rejection activates the same brain areas as physical pain.", "name": "Friend Fact 18"},
    {"content": "Friendships often form faster when people laugh together.", "name": "Friend Fact 19"},
    {"content": "Celebrating small wins with friends strengthens relationships.", "name": "Friend Fact 20"}
]


# Function to return embedding array for the parameter arrayOfStrings using OpenAI Embedding API
def generate_embeddings(arrayOfStrings):
    # Generate embeddings for the given list of texts using OpenAI API.
    response = openai_client.embeddings.create(input=arrayOfStrings, dimensions=1024, model="text-embedding-3-small")    
    arrayOfEmbeddings = [item.embedding for item in response.data]
    return arrayOfEmbeddings

# Function to create OpenSearch index with knn_vector mapping
#funfacts(id,content,name,fact_embedding)
def create_opensearch_index(opensearch_client):
    index_body = {
        "settings": {
                "index": {
                    "knn": True  # Enable k-NN
                },
        },
        "mappings": {
            "properties": {
                "id": {"type": "long"},  # ID field (similar to serial)
                "name": {"type": "text"}, # Text field for the document name
                "content": {"type": "text"}, # Text field for the document content
                "fact_embedding": {
                    "type": "knn_vector", # k-NN vector field for embeddings
                    "dimension": 1024, # Dimension of the embedding vector
                    "method": { # Method for indexing the embeddings
                        "name": "hnsw", # Hierarchical Navigable Small World Graph used for indexing
                        "space_type": "cosinesimil", # Cosine similarity used for distance calculation (L2 for Euclidean Distance)
    # If you're working with text embeddings (like OpenSearch k-NN search), cosine similarity is usually the best choice.
                        "engine": "nmslib" # NMSLIB library used for indexing 
                        }
                }
            }
        }
    }
    # Create the index (Table) if it does not exist
    if not opensearch_client.indices.exists(INDEX_NAME):
        opensearch_client.indices.create(index=INDEX_NAME, body=index_body)
        print(f"Index '{INDEX_NAME}' created.")

# Function to insert documents into OpenSearch
def insert_documents(opensearch_client, knowledge_base, fact_embeddings):
    actions = []
    for i, doc in enumerate(knowledge_base):
        action = {
            "_index": INDEX_NAME,
            "_id": i,
            "_source": {
                "name": doc["name"],
                "content": doc["content"],
                "fact_embedding": fact_embeddings[i]
            }
        }
        actions.append(action)
    success, _ = bulk(opensearch_client, actions)
    print(f"Successfully inserted {success} documents into OpenSearch.")

# Main function to generate embeddings and insert documents
def main():
    # Extract contents from the documents
    arrayOfStrings = []
    for doc in knowledge_base:
        arrayOfStrings.append(doc["content"])

    # Generate embeddings for the content
    arrayOfEmbeddings = generate_embeddings(arrayOfStrings)

    # Connect to OpenSearch
    opensearch_client = OpenSearch(**OPENSEARCH_CONFIG)

    # Create the OpenSearch index
    create_opensearch_index(opensearch_client)

    # Insert documents with embeddings
    insert_documents(opensearch_client, knowledge_base, arrayOfEmbeddings)

# Entry point of the script
if __name__ == "__main__":
    main()
