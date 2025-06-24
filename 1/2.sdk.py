from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
# Define the messages
messages = [
    {"role": "user", "content": "Name 5 best countries to visit ad why ? in a tabular format." }
]
completion = client.chat.completions.create(  
    model="gpt-4o-mini",
    messages=messages,
    n=10
)
# Print the response
print(completion.choices[0].message.content)
print("=" * 50)
print(completion.choices[1].message.content)
