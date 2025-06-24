from openai import OpenAI
import os
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

class Grade(str, Enum):
    Excellent = "excellent"
    Good = "good"
    Bad = "bad"
    Worst = "worst"

class ProductReview(BaseModel):
    product_names:  list[str] = Field(..., description="A brief summary of the product being reviewed.")
    rating: float = Field(..., description="The rating of the product")
    review_text: str = Field(..., description="The opinion of reviewer of product")
    reviewer: str = Field(..., description="The name of reviewer")
    isReview: bool = Field(..., description="True if review else False.")
    grade: Optional[Grade] = Field(...,description="Describe the product as worst, bad, good or excellent")
    
class ReviewsList(BaseModel):
    reviews: list[ProductReview] = Field(..., description="List of product reviews")


# Use OpenAI's chat completion API with the JSON Schema
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    temperature=0.5,
    messages=[
        {"role": "system", "content": "Extract the review details. Please provide seperate reviews for each object"},#Extract the review details. Please provide separate object for each product review
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
    response_format=ProductReview
)

# Extract the structured review information
review = completion.choices[0].message.parsed

# Display the parsed review information

if(review.isReview):    
    print(f"Product Names: {review.product_names}")
    print(f"Rating: {review.rating}")
    print(f"Review: {review.review_text}")
    print(f"Reviewer: {review.reviewer}")
else:
    print("This is not a review.")
