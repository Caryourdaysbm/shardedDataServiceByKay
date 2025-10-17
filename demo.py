import requests

url = "http://localhost:8000/store"
data = [
    {"userId": 1, "data": "Alice"},
    {"userId": 2, "data": "Bob"},
    {"userId": 3, "data": "Charlie"},
    {"userId": 4, "data": "Diana"}
]

for item in data:
    resp = requests.post(url, json=item)
    print(resp.json())

resp = requests.get("http://localhost:8000/shards")
print("Shard distribution:", resp.json())
