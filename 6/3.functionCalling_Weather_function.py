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

# ********* Step 2: Call model with functions defined – along with your system and user messages. *********
get_weather_schema = {
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in Celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"}
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    },
    "strict": True
}

tools = [
    {
        "type": "function",
        "function": get_weather_schema
    }
]

messages = [
    {"role": "user", "content": "What's the best clothing based on weather in Wellington today?"}
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

# Append model's function call message
messages.append(completion.choices[0].message)

# ********* Step 3: Model decides to call function(s) – model returns the name and input arguments. *********
# Extract the arguments from the function
tool_call = completion.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

print(tool_call.function.name)
print(args)

# ********* Step 4: Execute function code – parse the model's response and handle function calls. *********
result = get_weather(args["latitude"], args["longitude"])

# ********* Step 5: Supply model with results – so it can incorporate them into its final response. *********
# Append result message
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

completion_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

print(completion_2.choices[0].message.content)