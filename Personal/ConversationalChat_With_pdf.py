import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber  # Library for extracting text from PDFs

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Load and extract text from a PDF file
def load_pdf_data(file_path="C:/Users/prave/Phython/BITC_Class_AI/Personal/AI_MS_RoadMap.pdf"):
    """Extracts text from a PDF file."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error loading PDF file: {e}")
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
    # Load PDF data
    file_path = input("Enter the path to the PDF file: ")
    pdf_text = load_pdf_data(file_path)
    if pdf_text is None:
        return

    print("PDF data loaded successfully!")
    print("Extracted Text Preview:")
    print(pdf_text[:500])  # Print the first 500 characters of the extracted text

    # Define the initial messages
    messages = [
        {"role": "developer", "content": "You are an expert in analyzing text from PDF documents. You can answer questions based on the content of the PDF. You must regret to answer questions not related to the PDF content."}
    ]

    # Add the extracted PDF text to the conversation context
    messages.append({"role": "system", "content": f"The content of the PDF is as follows:\n{pdf_text}"})

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