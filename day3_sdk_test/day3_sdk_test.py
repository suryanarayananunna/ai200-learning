import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

credential = DefaultAzureCredential()

client = ResourceManagementClient(
    credential=credential,
    subscription_id=subscription_id
)

print("Azure SDK client created successfully.")

print("\nResource groups:")
for rg in client.resource_groups.list():
    print(f"- {rg.name} | {rg.location}")