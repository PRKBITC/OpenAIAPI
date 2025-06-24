from openai import OpenAI
import os
import numpy as np

client = OpenAI()

response = client.embeddings.create(
  #input=["I do programming and I am programmer", "I do programmnig and I am a developer"],
  #input=["I do programming and I am programmer", "Today is Holiday"],
  input=["Today Is working", "Today is Holiday"],#0.37
  #input=["I Love you", "I hate YOu"],#.61
  #input=["the sun is shaining brightly over the ocean", "A black hole consumes all light and energy in silence"],
  #input=["The cat sat on the mat and looked around.", "A cat sat on the mat and glanced around."],#.89
  #input=["I love playing football on weekends with my friends.", "I enjoy playing football on weekends with my friends."],#.89
  #input=["I love working on weekends.", "I hate working on weekends."],#.58
  model="text-embedding-3-small",
  dimensions=6 #1536 as default
)
#print(response.data[0].embedding)
# print(response.data[1].embedding)

# Calculate Cosine Similariy
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("Cosine Similarity:", cosine_similarity(response.data[0].embedding, response.data[1].embedding))


