from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Input sentence
text = "How can I apply for a home loan?"

# Generate embedding
embedding = model.encode(text)

print("Original text:", text)
print("\nFirst 10 embedding values:")
print(embedding[:10])

print("\nEmbedding dimensions:", len(embedding))





from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "How can I apply for a home loan?",
    "What are the eligibility requirements for a mortgage?",
    "How do I prepare vegetable biryani?"
]

# Generate embeddings for all documents
embeddings = model.encode(documents)

print("Number of documents:", len(documents))
print("Embedding dimensions:", embeddings.shape)

# Compare document 1 with documents 2 and 3
similarities = cosine_similarity(
    [embeddings[0]],
    embeddings[1:]
)

for i, score in enumerate(similarities[0]):
    print(f"Document 1 vs Document {i + 2}: {score:.4f}")



