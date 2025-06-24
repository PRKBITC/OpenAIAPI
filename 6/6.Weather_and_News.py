import requests
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# ********* Step 1: Create a function to get the weather *********
# The function will take latitude and longitude as input and return the current temperature in Celsius.
def get_weather(latitude, longitude):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data['current']['temperature_2m']

# Replace with your API key
news_api_key = "c86245eca72141828e351e1ea1e92fae"

# Define the `get_news` function to retrieve news articles based on a given topic
def get_news(topic):
    print(f"In get news about {topic}")
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=5"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            news = json.dumps(response.json(), indent=4)
            news_json = json.loads(news)

            # Access all the fields and loop through articles
            status = news_json["status"]
            total_results = news_json["totalResults"]
            articles = news_json["articles"]
            final_news = []

            for article in articles:
                source_name = article["source"]["name"]
                author = article["author"]
                title = article["title"]
                description = article["description"]
                url = article["url"]
                content = article["content"]

                title_description = f"""
                Title: {title},
                Author: {author},
                Source: {source_name},
                Description: {description},
                URL: {url},
                Content: {content}
                """
                final_news.append(title_description)

            return final_news
        else:
            return []
    except requests.exceptions.RequestException as e:
        return f"Error occurred during API Request: {e}"

# Define the function schema for OpenAI API
get_news_function_schema = {
    "name": "get_news",
    "description": "Retrieve the latest news articles on a given topic.",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The topic to search news articles for.",
            }
        },
        "required": ["topic"],
    },
}

# ********* Step 2: Call model with functions defined – along with your system and user messages *********
get_weather_schema = {
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in Celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"},
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False,
    },
    "strict": True,
}

tools = [
    {"type": "function", "function": get_weather_schema},
    {"type": "function", "function": get_news_function_schema},
]

messages = [
    {
        "role": "user",
        "content": "What's the clothing suitable for the weather in Auckland and Wellington today? Also suggest the most happening events based on the latest news in the same cities.",
    }
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# Append model's function call message
messages.append(completion.choices[0].message)

# ********* Step 3: Model decides to call function(s) – model returns the name and input arguments *********
# Extract the arguments from the function
for tool_call in completion.choices[0].message.tool_calls:
    args = json.loads(tool_call.function.arguments)
    print(tool_call.function.name)
    print(args)

    if tool_call.function.name == "get_news":
        result = get_news(args["topic"])
    elif tool_call.function.name == "get_weather":
        result = get_weather(args["latitude"], args["longitude"])

    # Append result message
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result),
        }
    )

# Second API call: Get the final response from the model
completion_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# Print the final response
print(completion_2.choices[0].message.content)