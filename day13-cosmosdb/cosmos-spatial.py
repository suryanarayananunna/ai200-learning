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


locations = [
    {
        "id": "store-101",
        "category": "store",
        "name": "Store A",
        "location": {
            "type": "Point",
            "coordinates": [77.5946, 12.9716]
        }
    },
    {
        "id": "store-102",
        "category": "store",
        "name": "Store B",
        "location": {
            "type": "Point",
            "coordinates": [77.6040, 12.9750]
        }
    }
]

for location in locations:
    container.upsert_item(body=location)

print("Location documents inserted!")




query = """
SELECT c.id, c.name,
    ST_DISTANCE(
        c.location,
        {
            "type": "Point",
            "coordinates": [77.5946, 12.9716]
        }
    ) AS distanceInMeters
FROM c
WHERE c.category = "store"
AND ST_DISTANCE(
    c.location,
    {
        "type": "Point",
        "coordinates": [77.5946, 12.9716]
    }
) < 2000
"""

results = container.query_items(
    query=query,
    partition_key="store"
)

for item in results:
    print(
        item["id"],
        item["name"],
        round(item["distanceInMeters"], 2),
        "meters"
    )