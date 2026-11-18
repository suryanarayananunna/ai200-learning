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

container_properties = container.read()

indexing_policy = container_properties["indexingPolicy"]

import json

print(json.dumps(indexing_policy, indent=4))



query = """
SELECT * FROM c
WHERE c.content = @content
"""

results = container.query_items(
    query=query,
    parameters=[
        {
            "name": "@content",
            "value": "The loan repayment period is 5 years."
        }
    ],
    partition_key="finance",
    populate_query_metrics=True
)

documents = list(results)

print("Matching documents:", len(documents))
print("Results:", documents)

headers = container.client_connection.last_response_headers
print("RU charge:", headers["x-ms-request-charge"])
print("Query metrics:", headers.get("x-ms-documentdb-query-metrics"))



new_policy = {
    "indexingMode": "consistent",
    "automatic": True,
    "includedPaths": [
        {"path": "/*"}
    ],
    "excludedPaths": [
        {"path": '/"_etag"/?'},
        {"path": "/content/?"}
    ]
}

database.replace_container(
    container,
    partition_key=PartitionKey(path="/category"),
    indexing_policy=new_policy
)

print("Indexing policy updated!")