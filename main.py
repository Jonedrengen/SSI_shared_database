import requests

response_Patient_table = requests.get("http://0.0.0.0:8888/Patient")
print(response_Patient_table.json())