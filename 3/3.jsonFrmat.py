from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
messages = [
    {"role": "system", "content": "You are a helpful assistant. Your response should be in JSON format."},
    {
        "role": "user",
        "content": "What are the features of GenAI?"
    }
]
client = OpenAI()
response = client.chat.completions.create(  
    model="gpt-4o",
    messages=messages,
    response_format={"type": "json_object"}
)
print(response.choices[0].message.content)
