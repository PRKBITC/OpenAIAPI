from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
import requests

credential = DefaultAzureCredential()

try:
    token = credential.get_token("https://management.azure.com/.default")
    print("✅ Access token acquired.")
    
    headers = {
        "Authorization": f"Bearer {token.token}"
    }

    whoami = requests.get("https://management.azure.com/tenants?api-version=2020-01-01", headers=headers)
    print("You are authenticated! ✅")
    print(whoami.json())

except ClientAuthenticationError as e:
    print("❌ Authentication failed:", e.message)
