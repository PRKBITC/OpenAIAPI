import openai

# Replace these with your actual values
openai.api_type = "azure"
openai.api_base = "https://prkcaihubresou5008222413.openai.azure.com/"
openai.api_version = "2024-05-01"
openai.api_key = "KLGO078QasicsY8VctaPILInFZ5TrkTEo7tKQHDcO4Gc0a9OyBQYJQQJ99BEACL93NaXJ3w3AAAAACOGLf1K"


# Replace with your deployed Foundry Agent's deployment name
deployment_name = "2024-12-01-preview"

# Call the Agent
response = openai.ChatCompletion.create(
    engine=deployment_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a fun fact about space."}
    ]
)

print(response["choices"][0]["message"]["content"])
