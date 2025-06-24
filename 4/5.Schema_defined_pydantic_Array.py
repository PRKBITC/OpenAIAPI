from openai import OpenAI
import os
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional,List
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

class Grade(str, Enum):
    Excellent = "excellent"
    Good = "good"
    Bad = "bad"
    Worst = "worst"

class ProductReview(BaseModel):
    product_names:  List[str] = Field(..., description="A brief summary of the product being reviewed.")
    rating: float = Field(..., description="The rating of the product")
    review_text: str = Field(..., description="The opinion of reviewer of product")
    reviewer: str = Field(..., description="The name of reviewer")
    isReview: bool = Field(..., description="True if review else False.")
    grade: Optional[Grade] = Field(...,description="Describe the product as worst, bad, good or excellent")
    
class Reviews(BaseModel):
     reviews: List[ProductReview] = Field(..., description="List of product reviews")   

# Use OpenAI's chat completion API with the JSON Schema
completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    temperature=0.5,
    messages=[
        {"role": "system", "content": "Extract the review details. Please provide separate objects for each product review"},
        {
            "role": "user",
            "content": """
                John rated Mouse 5 of 5 and felt good to have it.
                Praveen rated Nokia as excellent .
                Adi rated Samsung as worst.
                Aru rated dell mouse as bad.
            """,
        },
    ],
    response_format=Reviews
)

# Extract the structured review information
reviews = completion.choices[0].message.parsed


# Print the structured review information

print("--------------------------------------------------") 
print("Product Reviews:")
for review in reviews.reviews:
    print(f"Product Name: {review.product_names}")
    print(f"Rating: {review.rating}")
    print(f"Review Text: {review.review_text}")
    print(f"Reviewer: {review.reviewer}")
    print(f"Is Review: {review.isReview}")
    print(f"Grade: {review.grade}")
    print("--------------------------------------------------")