#Reading NUmber Of Agents inthe Azure AI Foundry Project
# Very important program to step into the world of Azure AI Agents


import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import openai
from dotenv import load_dotenv
load_dotenv()

# Set your endpoint (or use os.environ if already set)

project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set
project_tenant= os.environ["PROJECT_TENANT_ID"] 
api_version="2025-05-01"

# Initialize the project client
project_client = AIProjectClient(
    endpoint=project_endpoint,
    project_tenant=project_tenant,  # Optional, set if needed        
    api_version=api_version,       
    credential=DefaultAzureCredential()
)



# List all agents and find the one named "Teacher"
agents = project_client.agents.list_agents()

# print("Available agents:")
# for agent in agents:
#     print(f"- Name: {agent.name}, ID: {agent.id}, Status: {getattr(agent, 'status', 'unknown')}")
    

teacher_agent = next((a for a in agents if a.name == "Teacher"), None)

if teacher_agent is None:
    print("Teacher agent not found.")
else:
    print(f"Found Teacher agent, ID: {teacher_agent.id}")

    # Create a new thread (or reuse an existing one)
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the agent
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hello Teacher, can you help me with my homework?"
    )
    print(f"Created message, ID: {message.id}")

    # Process the run and get a response
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=teacher_agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    else:
        # Get the agent's response
        messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages:
        print(f"Role: {message.role}, Content: {message.content}")