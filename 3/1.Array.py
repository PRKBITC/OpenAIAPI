from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
import json

# Get OpenAI Client from Util.
# header_name = os.getenv("GATEWAY_HEADER_NAME")
# header_value = os.getenv("GATEWAY_HEADER_VALUE")
#headers = {header_name: header_value}
#client = OpenAI(default_headers=headers)
client = OpenAI()

# Define the JSON Schema for the response
review_schema = {
                "type": "object",
                "properties": {
                    "product_summary": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
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
                    "IsReview": {
                        "type": "boolean",
                        "description": "A boolean value indicating whether the input is a review or not.",
                    },
                    "rating_text": {
                        "type": "string",
                        "description": "The text representation of the rating",
                        "enum": ["worst", "bad", "nice", "best"],
                    }
                },
                "required": ["product_summary", "rating", "review_text", "reviewer", "IsReview", "rating_text"],
                "additionalProperties": False,
            }

reviews_schema = {
            "name": "product_review",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "reviews": {
                        "type": "array",
                        "items": review_schema
                    }
                },
                "required": ["reviews"],
                "additionalProperties": False,
            }
        }
# Use OpenAI's chat completion API with the JSON Schema
completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    temperature=0.2,
    messages=[
        {"role": "system", "content": "Extract the review details. Use NA for all missing properties"},
        {
            "role": "user",
            "content": """
            John said computer, mouse and mobile phone are awesome
            Sandeep has rated mobile as very good
            Andres has expressed happiness in buying a camera
            """,
        },
    ],
    response_format={
        "type": "json_schema",
        "json_schema": reviews_schema
    },
)

# Extract the structured review information
ratings = completion.choices[0].message.content
# Display the parsed review information
ratings_json = json.loads(ratings)
for review in ratings_json["reviews"]:
    print(f"Reviewer: {review['reviewer']}")
    print(f"Rating: {review['rating']}")
    print(f"Rating Text: {review['rating_text']}")
    print(f"Review Text: {review['review_text']}")
    print(f"Product Summary: {review['product_summary']}")
    print(f"Is Review: {review['IsReview']}")
    print()
