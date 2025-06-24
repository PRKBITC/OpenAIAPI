from openai import OpenAI
from dotenv import load_dotenv

format = "JSON"
load_dotenv()
messages = [
    {
        "role": "system",
        "content": f"""
                You are suppose to provide features of any keyword. Please provide your response in {format} format.
                The {format} format should be like this:
                {{
                    "features": [
                        {{
                            "name": "Text Generation",
                            "description": "Ability to generate human-like text based on a prompt.",
                            "examples": [
                                "Generate a blog introduction about AI trends.",
                                "Write an email apology to a customer.",
                                "Create a short story about a space adventure."
                            ]
                        }}
                    ]
                }}
             """,
    },
    {"role": "user", "content": "GenAI?"},
]
client = OpenAI()
response = client.chat.completions.create(
    messages=messages, model="gpt-4o-mini", response_format={"type": "json_object"}
)
print(response.choices[0].message.content)
