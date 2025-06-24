from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
# Define the messages
messages = [
    {"role": "developer", "content": "You are an expert in AI and ML Subject. You can answer any question about AI and ML at an entry level learners.You must regret to answer questions not relates to AI and ML" }    
]
while True:
    # Get user input
    user_input = input("Praveen Enter your Question: ")
    if user_input.lower() == "exit":
        break
    messages.append({"role": "user", "content": user_input })
    completion = client.chat.completions.create(  
        model="gpt-4o-mini",
        messages=messages,    
    )
    # Print the response
    print(completion.choices[0].message.content)
    print("*******************************************************************************" )
    messages.append({"role": "assistant", "content": completion.choices[0].message.content })

