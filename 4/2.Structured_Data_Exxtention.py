from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


# Define the MovieDetails model
class MovieDetails(BaseModel):
    title: str
    director: str
    cast: list[str]
    genre: list[str]
    synopsis: str

client = OpenAI()
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",  # Specify the model
    messages=[
        {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text describing a movie and should extract the details into the given structure."},
        {"role": "user", "content": "The movie Inception is directed by Christopher Nolan. It features Leonardo DiCaprio, Joseph Gordon-Levitt, and Ellen Page in lead roles. It’s a science fiction thriller that explores dreams within dreams. The genre includes science fiction, thriller, and mystery."}
    ],
    response_format=MovieDetails,  # Parse response into MovieDetails
)

# Extract the structured movie details
movie_details = completion.choices[0].message.parsed

# Display the parsed movie details
print(movie_details)
