from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

messages = [
    {
        "role": "developer",
        "content": """
                You are a poet.                
                You can write poems with variable number of  lines in each stanza. 
                Please use the below json format for output
                {
                    "stanza":  [           
                            {               
                            "lines: [
                                    "Line 1"                        
                            ],
                            "lines_count": 3
                            }            
                    ]
                }
                """,
    },
    {
        "role": "user",
        "content": "Write a poem on Weather"
    },
]
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.3,
    top_p=0.3,
    response_format={"type": "json_object"},
)

# Print the response
print(completion.choices[0].message.content)
