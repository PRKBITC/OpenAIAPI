from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
# Define the messages
messages = [
    {"role": "developer", "content": """You are an expert in Finance and Maori Subject. 
                                    You can answer any question about Finance and Maori at an entry level learners.
                                    You must regret to answer questions not relates to Finance and Maori""" }    
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
    print("Request Token count: ",completion.usage.prompt_tokens)
    print("Response Token Count: ",completion.usage.completion_tokens)
    print("Total Token Count: ",completion.usage.total_tokens)
    print("*******************************************************************************" )
    messages.append({"role": "assistant", "content": completion.choices[0].message.content })

