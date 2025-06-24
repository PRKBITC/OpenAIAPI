from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient

credential = DefaultAzureCredential()
client = SubscriptionClient(credential)

#for sub in client.subscriptions.list():
#print(f"Subscription: {sub.display_name} ({sub.subscription_id})")
print(credential)
print(client.subscriptions.list())

token = credential.get_token("https://management.azure.com/.default")
print(token)
