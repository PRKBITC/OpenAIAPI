import openai
import json
from openai import OpenAI
import os

client = OpenAI()


def upload_file_and_create_batch():
    # Upload batch tasks file
    with open("7/Batch_File.json1", "rb") as f:
        batch_input_file = client.files.create(
            file=f,
            purpose="batch")
        print("File uploaded with ID: ", batch_input_file.id)

        # Create and execute a batch from an uploaded file of requests
        batch = client.batches.create(
            input_file_id=batch_input_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={"description": "nightly eval job"})
        print("Batch created with ID: ", batch.id)
        return batch


def print_batch_ids():
    batches = client.batches.list(limit=10)
    for batch in batches:  # ["data"]:
        print(f"Batch Id= {batch.id} Status= {batch.status}")


def print_batch_details(batch_id):
    batch = client.batches.retrieve(batch_id)
    print("Status=", batch.status)
    print("Total Tasks: ", batch.request_counts.total)
    print("Completed Tasks: ", batch.request_counts.completed)
    print("Failed Tasks: ", batch.request_counts.failed)
    if batch.status == "completed":
        file_response = client.files.content(batch.output_file_id)
        file_content = file_response.text
        lines = file_content.splitlines()
        for line in lines:
            if line.strip():
                line_json = json.loads(line)
                print("Response: ", line_json["response"])
                print(line_json["response"]["body"]
                      ["choices"][0]["message"]["content"])
                print("--------------------")


def get_batch_id_from_user():
    batch_id = input("Enter batch ID: ")
    return batch_id


def delete_batch(batch_id):
    client.batches.delete(batch_id)
    print("Batch deleted")


def main():
    print("Select an option:")
    print("1. Upload File and Create Batch")
    print("2. Get Batch Ids")
    print("3. Print Batch Details")
    choice = input("Enter your choice: ")
    if choice == '1':
        upload_file_and_create_batch()
    elif choice == '2':
        print_batch_ids()
    elif choice == '3':
        batch_to_print = get_batch_id_from_user()
        print_batch_details(batch_to_print)
    else:
        print("Invalid choice")


# Run the main function
main()
