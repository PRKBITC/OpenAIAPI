from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client=OpenAI()

file=client.files.create(
    file=open("C:/Users/prave/Phython/BITC_Class_AI/Personal/AI_MS_RoadMap.pdf", "rb"),
    purpose="user_data"
)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user", 
         "content": [
             {
             "type":"file",
                "file":{
                    "file_id":file.id,
             }
        },
        {
            "type":"text",
            "text":"Healthcare AI readiness summary",
            },
         ] 
        }
    ]
    
)
# Print the response
print(completion.choices[0].message.content)
print("Token count: ",completion.usage.prompt_tokens)