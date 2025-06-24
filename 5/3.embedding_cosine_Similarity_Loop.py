import openai
import numpy as np
from openai import OpenAI
import os
client = OpenAI()

# Sentences to be embedded
sentences = [
    "This is a Sample Code of OpenAI",
    "OpenAI Sample Code:",
    "Today is a holiday"
]
# Function to get embeddings from OpenAI
def get_embeddings(arrayOfStrings):
    response = client.embeddings.create(
        input=arrayOfStrings,     
        dimensions=256,
        model="text-embedding-3-small"
    )
    #print(response.data)    
    arrayofEmbeddings = []
    for data in response.data:
        arrayofEmbeddings.append(data.embedding)
        print(len(data.embedding))
    return arrayofEmbeddings

# Calculate Cosine Similariy
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Get embeddings
embeddings = get_embeddings(sentences)
# Print cosine similarities between all texts in sentences array
print("Cosine Similarities:")
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        similarity = cosine_similarity(embeddings[i], embeddings[j])
        print(f"Similarity between '{sentences[i]}' and '{sentences[j]}': {similarity}")

print(cosine_similarity(embeddings[0], embeddings[1]))
