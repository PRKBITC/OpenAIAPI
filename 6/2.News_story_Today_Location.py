#Expensive search dont use much for "gpt-4o-search-preview"
#Expensive search dont use much for "gpt-4o-search-preview"
#Expensive search dont use much for "gpt-4o-search-preview"
#Expensive search dont use much for "gpt-4o-search-preview"

from openai import OpenAI


client = OpenAI()


completion = client.chat.completions.create(model="gpt-4o-search-preview", web_search_options={
    "search_context_size": "low", #low, medium, high
    "user_location": {
        "type": "approximate",
        "approximate": {
            "country": "NZ",
            "city": "Wellington", "region": "Wellington",
        },
    }
},
    messages=[
    {
        "role": "user",
        "content": "What was a positive news story from today in my location?",
    }
],
)
print("Content: ", completion.choices[0].message.content)
print(
    "Title: ", completion.choices[0].message.annotations[0].url_citation.title)
print("URL: ", completion.choices[0].message.annotations[0].url_citation.url)
