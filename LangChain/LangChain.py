from langchain_openai import AzureChatOpenAI
from langchain.agents import initialize_agent, Tool


# Your LLM (Azure OpenAI)
llm = AzureChatOpenAI(deployment_name="2024-12-01-preview", temperature=0.7)

# A simple tool
def add_numbers(a, b):
    return str(int(a) + int(b))

tools = [
    Tool(name="Adder", func=lambda x: add_numbers(*x.split()), description="Add two numbers")
]

# Create agent
agent = initialize_agent(tools, llm, agent="Teacher", verbose=True)

# Use agent
agent.run("What is 10 plus 25?")
