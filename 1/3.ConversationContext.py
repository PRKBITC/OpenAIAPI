from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
# Define the messages
messages = [
    {"role": "developer", "content": "You are an expert in AI and ML Subject. You can answer any question about AI and ML at an entry level learners.You must regret to answer questions not relates to AI and ML" },
    {"role": "user", "content": "What is Gen AI?" }
]
completion = client.chat.completions.create(  
    model="gpt-4o-mini",
    messages=messages,
    
)
# Print the response
print(completion.choices[0].message.content)
print("*********What are the features?**********************" )
messages.append({"role": "assistant", "content": completion.choices[0].message.content })
messages.append({"role": "user", "content": "What are the features?" })
completion = client.chat.completions.create(  
    model="gpt-4o-mini",
    messages=messages,    
)
# Print the response
print(completion.choices[0].message.content)
print("********General day today usecases*******************" )
messages.append({"role": "assistant", "content": completion.choices[0].message.content })
messages.append({"role": "user", "content": "General day today usecases" })
completion = client.chat.completions.create(  
    model="gpt-4o-mini",
    messages=messages,    
)
# Print the response
print(completion.choices[0].message.content)
print("****************************************************************" )
