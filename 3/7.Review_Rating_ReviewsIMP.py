from openai import OpenAI
import os
from dotenv import load_dotenv
import json
load_dotenv()
client = OpenAI()

#Define the JSON Schema for the response
review_schema = {
    "type": "object",
    "properties": {
        "product_summary": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "A brief summary of the product being reviewed.",
            }
        },
        "rating": {
            "type": "number",
            "description": "The rating given to the product, usually on a scale from 1 to 5.",
            "min": 1,
            "max": 5,
        },
         "rating_text": {
            "type": "string",
            "description": "The text representation of the rating",
            "enum": ["Excellent", "Good", "Average", "not good", "good"],
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
        # Add more properties as needed
    },
    # Specify required fields and additional properties
    "required": ["product_summary", "rating","rating_text", "review_text", "reviewer", "IsReview"],
    "additionalProperties": False,
}
#Use OpenAI's chat completion API with the JSON Schema
reviews_schema={
    "type": "object",
    "properties": {
        "reviews": {
            "type": "array",
            "items":review_schema,
            },            
        },
    "required": ["reviews"],
    "additionalProperties": False,
    }

   
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.5,
    messages=[
        {"role": "system", "content": "Extract the review details. Use NA for missing values.Please provide seprate object for each product review"},
        {
            "role": "user",
            "content": """
                John rated Dell Laptop as excellent but also mentioned that dell Mouse is average and Dell keyborad as worst
                Praveen said Nokia mobile is good and Samsung mobile is not good
                Sandeep has rated mobile as very good and also mentioned that Samsung mobile is not good
            """,
        },
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "product_review",
            "strict": True,
            "schema": reviews_schema,
        },
    },
)
# Extract the sturctured review information
rating = completion.choices[0].message.content
#Display the parsed review information
ratings_json = json.loads(rating)
print(ratings_json)
for review in ratings_json["reviews"]:
    print(f"Product Summary: {review['product_summary']}")    
    print(f"Rating: {review['rating']}")
    print(f"Rating Text: {review['rating_text']}")
    print(f"Review Text: {review['review_text']}")    
    print(f"Reviewer: {review['reviewer']}")
    print(f"Is Review: {review['IsReview']}")
    print("-" * 20)