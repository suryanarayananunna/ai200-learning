from azure.identity import AzureCliCredential
from azure.cosmos import CosmosClient, PartitionKey

ENDPOINT = "https://cosmosdb-learning1.documents.azure.com:443/"

credential = AzureCliCredential()

client = CosmosClient(
    url=ENDPOINT,
    credential=credential
)

# Connect to the database created using Azure CLI
database = client.get_database_client("ai200-learning-db")
container = database.get_container_client("documents")

query = """
SELECT * FROM c
ORDER BY c.category ASC, c.title ASC
"""

results = container.query_items(
    query=query,
    enable_cross_partition_query=True
)

for item in results:
    print(item["id"], item["category"], item["title"])