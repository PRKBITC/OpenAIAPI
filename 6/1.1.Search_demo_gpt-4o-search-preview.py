
#Expensive search dont use much for "gpt-4o-search-preview"
#Expensive search dont use much for "gpt-4o-search-preview"
#Expensive search dont use much for "gpt-4o-search-preview"
#Expensive search dont use much for "gpt-4o-search-preview"

#Websearch

from openai import OpenAI 
client = OpenAI() 
completion = client.chat.completions.create( 
    model="gpt-4o-search-preview", 
    web_search_options={}, 
    messages=[ 
            { 
            "role": "user", 
            "content": "What was a positive news story from today?", 
            } 
        ], 
    ) 
print(completion.choices[0].message.content)