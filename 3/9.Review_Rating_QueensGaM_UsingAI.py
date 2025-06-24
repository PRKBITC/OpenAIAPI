from openai import OpenAI
import googlemaps
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Initialize Google Maps client
API_KEY = "AIzaSyAO4uGpMzqO0fLkS93cbpACmck-k5aeAD4"  # Replace with your Google API key
gmaps = googlemaps.Client(key=API_KEY)

# Function to fetch reviews from Google Places API
def fetch_google_reviews(place_name):
    """Fetch reviews for a given place using Google Places API."""
    try:
        # Search for the place
        places_result = gmaps.places(query=place_name)

        if not places_result.get("results"):
            print("No results found for the given place.")
            return []

        # Get the place ID of the first result
        place_id = places_result["results"][0]["place_id"]

        # Get detailed information about the place, including reviews
        place_details = gmaps.place(place_id=place_id, fields=["name", "rating", "reviews"])

        # Extract reviews
        reviews = place_details.get("result", {}).get("reviews", [])
        extracted_reviews = []
        for review in reviews:
            extracted_reviews.append({
                "product_summary": [place_name],
                "rating": review.get("rating", "NA"),
                "rating_text": "NA",  # Google reviews don't provide a text rating, so we use "NA"
                "review_text": review.get("text", "NA"),
                "reviewer": review.get("author_name", "NA"),
                "IsReview": True
            })
        return extracted_reviews

    except Exception as e:
        print(f"An error occurred while fetching reviews: {e}")
        return []

# Function to interact with the GPT model
def ask_question(messages):
    """Send a conversational query to the GPT-4o-mini model."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.5,
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Main function to handle fetching reviews and conversational queries
def main():
    # Prompt the user to enter a place name
    place_name = input("Enter the name of the place you want to fetch reviews for: ")

    # Fetch reviews for the entered place
    reviews = fetch_google_reviews(place_name)

    if not reviews:
        print("No reviews found.")
        return

    # Prepare the initial context for the GPT model
    messages = [
        {"role": "system", "content": "You are an AI assistant that analyzes reviews. Use NA for missing values."},
        {
            "role": "user",
            "content": f"The following are reviews for {place_name}: {json.dumps(reviews)}",
        },
    ]

    # Start a conversational loop
    print("Reviews fetched successfully. You can now ask questions about the reviews.")
    while True:
        user_input = input("Ask a question about the reviews (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add user input to the conversation
        messages.append({"role": "user", "content": user_input})

        # Get the model's response
        response = ask_question(messages)
        if response:
            print("AI Response:")
            print(response)
            # Add the assistant's response to the conversation
            messages.append({"role": "assistant", "content": response})
        else:
            print("Failed to get a response. Please try again.")

if __name__ == "__main__":
    main()