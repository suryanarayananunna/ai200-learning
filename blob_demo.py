from azure.storage.blob import BlobServiceClient

# Connect to local Azurite Blob Storage
connection_string = "UseDevelopmentStorage=true"

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

print("Connected to local Blob Storage!")

# 1. Get a client for the "documents" container
container_name = "documents"

container_client = blob_service_client.get_container_client(
    container_name
)

# 2. Create the container
try:
    container_client.create_container()
    print(f"Container '{container_name}' created!")
except Exception:
    print(f"Container '{container_name}' already exists.")

# 3. Get a client for our blob
blob_name = "sample.txt"

blob_client = container_client.get_blob_client(blob_name)

# 4. Upload the local file
with open("sample.txt", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print(f"Uploaded '{blob_name}' successfully!")

# Download the blob
download_stream = blob_client.download_blob()

downloaded_data = download_stream.readall()

with open("sample_downloaded.txt", "wb") as file:
    file.write(downloaded_data)

print("Blob downloaded successfully!")
