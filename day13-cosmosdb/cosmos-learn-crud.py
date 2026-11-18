from azure.identity import AzureCliCredential
from azure.cosmos import CosmosClient

ENDPOINT = "https://cosmosdb-learning1.documents.azure.com:443/"

# Authenticate using the current Azure CLI login
credential = AzureCliCredential()

# Connect to Cosmos DB
client = CosmosClient(
    url=ENDPOINT,
    credential=credential
)

# Test data-plane access by listing databases
databases = list(client.list_databases())

print("Successfully connected to Cosmos DB!")
print("Databases available:")

for database in databases:
    print("-", database["id"])