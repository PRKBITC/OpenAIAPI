import googlemaps

# Initialize the Google Maps client
API_KEY = "AIzaSyAO4uGpMzqO0fLkS93cbpACmck-k5aeAD4"  # Replace with your API key
gmaps = googlemaps.Client(key=API_KEY)

def get_place_reviews(place_name):
    """Fetch reviews for a given place using Google Places API."""
    try:
        # Search for the place
        places_result = gmaps.places(query=place_name)

        if not places_result.get("results"):
            print("No results found for the given place.")
            return

        # Get the place ID of the first result
        place_id = places_result["results"][0]["place_id"]

        # Get detailed information about the place, including reviews
        place_details = gmaps.place(place_id=place_id, fields=["name", "rating", "reviews"])

        # Extract reviews
        reviews = place_details.get("result", {}).get("reviews", [])
        for i, review in enumerate(reviews, start=1):
            print(f"Review {i}:")
            print(f"Author: {review['author_name']}")
            print(f"Rating: {review['rating']}")
            print(f"Text: {review['text']}")
            print(f"Time: {review['relative_time_description']}")
            print("-" * 20)

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
place_name = "Queensgate Shopping Centre"
get_place_reviews(place_name)