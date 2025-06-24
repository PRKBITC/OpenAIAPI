from openai import OpenAI
import os
from dotenv import load_dotenv
import json
load_dotenv()
client = OpenAI()
# Define the JSON Schema for the response
review_schema = {
    "type": "object",
    "properties": {
        "product_summary": {
            "type": "string",
            "description": "A brief summary of the product being reviewed.",
        },
        "rating": {
            "type": "number",
            "description": "The rating given to the product, usually on a scale from 1 to 5.",
        },
        "review_text": {
            "type": "string",
            "description": "The detailed review text provided by the reviewer.",
        },
        "reviewer": {
            "type": "string",
            "description": "The name or identifier of the reviewer.",
        },
        "IsReview" : {
            "type": "boolean",
            "description": "True if the content is a review, False otherwise.",
        },
        "review_quality": {
            "type": "string",
            "description": "The quality of the review, which can be either 'worst', 'bad', 'good', or 'best'.",
            "enum": ["worst", "bad", "good", "best"],
        },
    },
    "required": ["product_summary", "rating", "review_text", "reviewer", "IsReview", "review_quality"],
    "additionalProperties": False,
}
# Use OpenAI's chat completion API with the JSON Schema
completion = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.5,
    messages=[
        {"role": "system", "content": "Extract the review details. Use NA for missing values."},
        {
            "role": "user",
            "content": "John had awful experience with the mouse",
        },
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "product_review",
            "strict": True,
            "schema": review_schema,
        },
    },
)

# Extract the structured review information
rating = completion.choices[0].message.content
# Display the parsed review information
rating_json = json.loads(rating)
print(rating_json)
