from pydantic import BaseModel

from openai import OpenAI
import os


# Define the structure for each step
class Step(BaseModel):
    explanation: str
    code_snippet: str

# Define the structure for the overall response
class JavaProgramGuide(BaseModel):
    steps: list[Step]
    final_code: str


client = OpenAI()

# Use OpenAI's beta chat completion API with a custom response format
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",  # Specify the model
    messages=[
        	{"role": "system", "content": "You are a programming tutor."},
 	{"role": "user", "content": "Provide me with step by step procedure to write a Java program to calculate the factorial of a number."}
    ],
    response_format=JavaProgramGuide,  # Parse response into JavaProgramGuide
)

# Extract the structured guide
java_guide = completion.choices[0].message.parsed

# Display the guide
for step in java_guide.steps:
    print(f"Step Explanation: {step.explanation}")
    print(f"Code Snippet:\n{step.code_snippet}\n")
print("Final Java Code:\n", java_guide.final_code)
