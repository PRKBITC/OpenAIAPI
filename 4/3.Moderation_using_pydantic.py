from enum import Enum
from typing import Optional
from pydantic import BaseModel

from openai import OpenAI
import os


class Category(str, Enum):
    violence = "violence"
    sexual = "sexual"
    self_harm = "self_harm"
    hate = "hate"
    harassment = "harassment"
    spam = "spam"
    misinformation = "misinformation"
    child_exploitation = "child_exploitation"
    adult_content = "adult_content"
    self_injury = "self_injury"
    

class ContentCompliance(BaseModel):
    is_violating: bool
    category: Optional[Category]
    explanation_if_violating: Optional[str]

client = OpenAI()
completion = client.beta.chat.completions.parse(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": "Determine if the user input violates specific guidelines and explain if they do."},
        {"role": "user", "content": "I want to cut my hand with knife"},
    ],
    response_format=ContentCompliance,
)
print(completion.choices[0].message.parsed)
