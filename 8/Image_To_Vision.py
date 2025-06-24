from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user",
         "content":
         [
             {"type":"text", "text": "What's in this image?"},
                {
                "type":
                    "image_url",
                    "image_url":
                    {
                        "url": "https://bdtmaterial.blob.core.windows.net/shared/Website%20Rewamp/HomePage/BITC%20logo%20new.png",
                        "detail": "high"  # (low, high or [auto])
                    },
                },
         ],
         }],
)
print(response.choices[0].message.content)
