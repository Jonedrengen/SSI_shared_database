import requests
from Pydantic_models import PatientUpdate

def test_get_request():
    response = requests.get("http://0.0.0.0:8888/Patient")

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")


def test_put_request():
    # Create an instance of PatientUpdate with the data you want to update
    patient_update = PatientUpdate(identifier="002bbe31-332f-4817-a400-9f77b8eadfd8", 
                                name="Johnny test", 
                                age=30,
                                gender="Male",
                                birthDate="2000-01-01",
                                deceased="0",
                                address="333 a test street")

    # Convert the PatientUpdate instance to a dictionary
    data = patient_update.model_dump()

    # Make the PUT request
    response = requests.put(f"http://0.0.0.0:8888/Patient/{patient_update.identifier}", json=data)

    if response.status_code == 200:
        print("Patient updated successfully")
    else:
        print(f"Request failed with status code {response.status_code}")

test_put_request()