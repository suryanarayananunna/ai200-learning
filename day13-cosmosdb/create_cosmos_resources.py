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

document2 = {
    "id": "doc-102",
    "category": "health",
    "title": "Health Insurance",
    "content": "Health insurance covers eligible medical expenses."
}

container.create_item(body=document2)

print("Second document inserted successfully!")


query = "SELECT * FROM c"

results = container.query_items(
    query=query,
    enable_cross_partition_query=True,
    populate_query_metrics=True
)

items = list(results)

print("Documents retrieved:", len(items))

request_charge = container.client_connection.last_response_headers[
    "x-ms-request-charge"
]

print("Request Units consumed:", request_charge)
headers = container.client_connection.last_response_headers

print("Query Metrics:", headers["x-ms-documentdb-query-metrics"])