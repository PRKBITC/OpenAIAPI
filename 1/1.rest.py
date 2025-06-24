import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("OPENAI_BASE_URL") + '/chat/completions';
api_key = os.getenv("OPENAI_API_KEY")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    }
data = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": """
            Create a short quiz with 5 questions and 4 options for each question. 
            The quiz should be about the Telangana festivals. Each question should have a correct answer marked with an asterisk (*) at the end of the option.
            The options should be in the format: 1. Option A, 2. Option B, 3. Option C, 4. Option D.
            """
        }
    ]
}
response = requests.post(url, headers=headers, data=json.dumps(data))
# Print only the content of the response
response_content = response.json()
print(response_content['choices'][0]['message']['content'])
