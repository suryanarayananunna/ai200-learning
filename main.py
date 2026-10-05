import json

from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

print("Azure credential object created successfully")
print(type(credential))


