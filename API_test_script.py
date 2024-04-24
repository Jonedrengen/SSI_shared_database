import requests

response = requests.get("http://0.0.0.0:8888/Patient")

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code {response.status_code}")