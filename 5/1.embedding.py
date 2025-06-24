from openai import OpenAI
import os
import numpy as np

client = OpenAI()

response = client.embeddings.create(
  input="I am White and I am Black", #,"I do programmnig and I am a developer"],#I do programming and I am programmer
  model="text-embedding-3-small",
  dimensions=6 #1536 as default
)
print(response.data[0].embedding)
# print(response.data[1].embedding)

# Calculate Cosine Similariy
# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# print("Cosine Similarity:", cosine_similarity(response.data[0].embedding, response.data[1].embedding))
