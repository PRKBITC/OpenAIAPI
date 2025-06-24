from openai import OpenAI 
client = OpenAI() 
completion = client.chat.completions.create( 
    model="gpt-4o", 
    #web_search_options={}, 
    messages=[ 
            { 
            "role": "user", 
            "content": "What was a positive news story from today?", #keyword today so unable to get a result
            } 
        ], 
    ) 
print(completion.choices[0].message.content)

#Output: I'm sorry, but I can't provide real-time news updates. 
#For the most recent news, I recommend checking a reliable news website or app.
