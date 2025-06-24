from openai import OpenAI
import os
import numpy as np

client = OpenAI()

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

embeddings=get_embeddings(["the sun is shaining brightly over the ocean", "A black hole consumes all light and energy in silence"])


#print(response.data[0].embedding)
# print(response.data[1].embedding)

# Calculate Cosine Similariy
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
  
  
def euclidean_distance(embedding1, embedding2):
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    
    if embedding1.shape != embedding2.shape:
      raise ValueError("Embeddings must have the same shape")
    return np.linalg.norm(embedding1 - embedding2) 
  
  

print("Cosine Similarity:", cosine_similarity(embeddings[0], embeddings[1]))
print("Cosine Similarity:", cosine_similarity([0,1], [0,-1]))#To get the negative value of cosine similarity    
print("Cosine Similarity:", cosine_similarity([2,4], [4,8]))#To get the close to 1 value of cosine similarity
print("Euclidean Distance:", euclidean_distance(embeddings[0], embeddings[1]))
