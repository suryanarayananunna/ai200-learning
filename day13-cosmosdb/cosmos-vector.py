from azure.identity import AzureCliCredential
from azure.cosmos import CosmosClient
from sentence_transformers import SentenceTransformer

ENDPOINT = "https://cosmosdb-learning1.documents.azure.com:443/"

credential = AzureCliCredential()

client = CosmosClient(
    url=ENDPOINT,
    credential=credential
)

database = client.get_database_client("ai200-vector-db")

container = database.get_container_client("vector-documents")

print("Connected to vector container!")

model = SentenceTransformer("all-MiniLM-L6-v2")


documents = [
    {
        "id": "vec-101",
        "category": "finance",
        "text": "How can I apply for a home loan?"
    },
    {
        "id": "vec-102",
        "category": "finance",
        "text": "What are the eligibility requirements for a mortgage?"
    },
    {
        "id": "vec-103",
        "category": "finance",
        "text": "How do I check my loan repayment schedule?"
    },
    {
        "id": "vec-104",
        "category": "food",
        "text": "How do I prepare vegetable biryani?"
    }
]

embeddings = model.encode(
    [doc["text"] for doc in documents]
)

for doc, embedding in zip(documents, embeddings):
    doc["embedding"] = embedding.tolist()
    container.create_item(body=doc)

print("Successfully inserted", len(documents), "documents!")




query_text = "I want to know whether I qualify for a mortgage."

query_embedding = model.encode(query_text).tolist()

query_text = "Tell me how to cook an Indian rice dish."

query_embedding = model.encode(query_text).tolist()

query = """
SELECT TOP 3
    c.id,
    c.category,
    c.text,
    VectorDistance(c.embedding, @queryVector) AS similarity
FROM c
WHERE c.category = @category
ORDER BY VectorDistance(c.embedding, @queryVector)
"""

results = container.query_items(
    query=query,
    parameters=[
        {"name": "@queryVector", "value": query_embedding},
        {"name": "@category", "value": "food"}
    ],
    partition_key="finance"
)

for item in results:
    print("ID:", item["id"])
    print("Text:", item["text"])
    print("Vector distance:", item["similarity"])
    print("-" * 50)




query_text = "Tell me how to cook an Indian rice dish."

query_embedding = model.encode(query_text).tolist()

query = """
SELECT TOP 3
    c.id,
    c.category,
    c.text,
    VectorDistance(c.embedding, @queryVector) AS distance
FROM c
WHERE c.category = @category
ORDER BY VectorDistance(c.embedding, @queryVector)
"""

results = container.query_items(
    query=query,
    parameters=[
        {"name": "@queryVector", "value": query_embedding},
        {"name": "@category", "value": "food"}
    ],
    partition_key="food"
)

for item in results:
    print("ID:", item["id"])
    print("Text:", item["text"])
    print("Distance:", item["distance"])
    print("-" * 40)





loan_text = "Loan application LOAN-101 submitted by Rahul for INR 1000000"

loan_document = {
    "id": "change-101",
    "category": "finance",
    "eventType": "LoanApplicationSubmitted",
    "applicationId": "LOAN-101",
    "customer": "Rahul",
    "amount": 1000000,
    "status": "Submitted",
    "text": loan_text,
    "embedding": model.encode(loan_text).tolist()
}

container.upsert_item(body=loan_document)

print("Loan application successfully submitted!")



response_iterator = container.query_items_change_feed(
    start_time="Beginning"
)

for document in response_iterator:
    print("Change detected!")
    print("ID:", document.get("id"))
    print("Event:", document.get("eventType"))
    print("Application:", document.get("applicationId"))
    print("Customer:", document.get("customer"))
    print("Amount:", document.get("amount"))
    print("-" * 40)



    continuation_token = (
    container.client_connection.last_response_headers["etag"]
)

print("Continuation token saved!")
print("Token available:", bool(continuation_token))


loan_text = "Loan application LOAN-102 submitted by Priya for INR 500000"

loan_document = {
    "id": "change-102",
    "category": "finance",
    "eventType": "LoanApplicationSubmitted",
    "applicationId": "LOAN-102",
    "customer": "Priya",
    "amount": 500000,
    "status": "Submitted",
    "text": loan_text,
    "embedding": model.encode(loan_text).tolist()
}

container.upsert_item(body=loan_document)

print("Second loan application submitted!")




response_iterator = container.query_items_change_feed(
    continuation=continuation_token
)

for document in response_iterator:
    print("New change detected!")
    print("ID:", document.get("id"))
    print("Application:", document.get("applicationId"))
    print("Customer:", document.get("customer"))
    print("Amount:", document.get("amount"))
    print("-" * 40)

continuation_token = container.client_connection.last_response_headers["etag"]