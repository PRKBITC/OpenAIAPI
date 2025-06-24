import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Load the student marks file
def load_student_data(file_path="C:/Users/prave/Phython/BITC_Class_AI/Personal/AI_MS_RoadMap.pdf"):
    """Loads student data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Generate a response using OpenAI's model
def generate_response(messages):
    """Generates a response using OpenAI's chat completion API."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# Main function
def main():
    # Load student data
    file_path = input("Enter the path to the student marks file (CSV): ")
    data = load_student_data(file_path)
    if data is None:
        return

    print("Student data loaded successfully!")
    print(data)

    # Define the initial messages
    messages = [
        {"role": "developer", "content": "You are an expert in analyzing student marks. You can answer questions about the highest, lowest, average marks, or display all student data. You must regret to answer questions not related to student marks."}
    ]

    while True:
        # Get user input
        user_input = input("Enter your question (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add user input to the conversation
        messages.append({"role": "user", "content": user_input})

        # Generate a response using OpenAI
        response = generate_response(messages)
        print(response)

        # Add the assistant's response to the conversation
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()