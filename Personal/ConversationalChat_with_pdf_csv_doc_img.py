import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber
from docx import Document  # For .docx files
from PIL import Image  # For .jpg files
import pytesseract  # For OCR on images

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Load and extract text from a PDF file
def load_pdf_data(file_path):
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

# Load and extract text from a .docx file
def load_docx_data(file_path):
    """Extracts text from a .docx file."""
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error loading DOCX file: {e}")
        return None

# Load and extract data from a CSV file
def load_csv_data(file_path):
    """Extracts data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data.to_string(index=False)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

# Load and extract text from a .jpg file using OCR
def load_jpg_data(file_path):
    """Extracts text from a .jpg file using OCR."""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error loading JPG file: {e}")
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
    # Get the file path and type
    file_path = input("Enter the path to the file: ")
    file_extension = os.path.splitext(file_path)[1].lower()

    # Extract content based on file type
    if file_extension == ".pdf":
        content = load_pdf_data(file_path)
    elif file_extension == ".docx":
        content = load_docx_data(file_path)
    elif file_extension == ".csv":
        content = load_csv_data(file_path)
    elif file_extension == ".jpg":
        content = load_jpg_data(file_path)
    else:
        print("Unsupported file type!")
        return

    if content is None:
        print("Failed to extract content from the file.")
        return

    print("File content loaded successfully!")
    print("Extracted Content Preview:")
    print(content[:500])  # Print the first 500 characters of the extracted content

    # Define the initial messages
    messages = [
        {"role": "developer", "content": "You are an expert in analyzing text and data from various file types. You can answer questions based on the content of the file. You must regret to answer questions not related to the file content."}
    ]

    # Add the extracted content to the conversation context
    messages.append({"role": "system", "content": f"The content of the file is as follows:\n{content}"})

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