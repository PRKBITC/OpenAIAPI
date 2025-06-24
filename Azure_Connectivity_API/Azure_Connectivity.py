import os
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from typing import List, Optional
import openai

client = openai.AzureOpenAI(
    api_key="KLGO078QasicsY8VctaPILInFZ5TrkTEo7tKQHDcO4Gc0a9OyBQYJQQJ99BEACL93NaXJ3w3AAAAACOGLf1K",
    azure_endpoint="https://prkcaihubresou5008222413.openai.azure.com/",
    api_version="2024-12-01-preview"
)