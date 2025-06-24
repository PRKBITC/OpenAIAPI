from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
# Define the messages

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Create a poem about the beauty of nature" }
        ],
    #Stream is a generator that yields chunks of data as they become available.
    #This is useful for long responses or when you want to display the response as it is being generated.
    #Rather than waiting for the entire response to be generated, you can process each chunk as it arrives.
    #This can be useful for creating a more interactive user experience.
    stream=True
)
for chunk in stream:
    print(chunk.choices[0].delta.content, end='', flush=True)
    #print(chunk.choices[0].delta)
    #print("******************************************")