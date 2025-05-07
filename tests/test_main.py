import os
import pprint
from fastapi.testclient import TestClient
from app.models.library import Library

from app.main import app


client = TestClient(app)

api_key = os.getenv("API_KEY")

# -------------- Heath Route Tests ------------

def test_health():
    response = client.get("/health", headers={ "X-Key": api_key })
    print("response: ", response.read())
    assert response.status_code == 200
    assert response.json() == { "status": "ok" }



# -------------- Libraries Route Tests ----------

def test_library_creation():
    response = client.post(
        "/libraries", 
        headers={ "X-Key": api_key }, 
        json={
            "name": "Test Library",
            "metadata": {"example": "valueA"}
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    print("response in json", response.json())
    lib = Library(**data)

    response = client.delete(
        f"/libraries/{lib.id}", 
        headers={ "X-Key": api_key }, 
    )


def test_listing_libraries():
    library_list = []

    response_one = client.post(
        "/libraries", 
        headers={ "X-Key": api_key }, 
        json={
            "name": "Test Library A",
            "metadata": {"example": "valueA"}
        }
    )
    library_list.append(Library(**response_one.json()))
    response_two = client.post(
        "/libraries", 
        headers={ "X-Key": api_key }, 
        json={
            "name": "Test Library B",
            "metadata": {"example": "valueB"}
        }
    )
    library_list.append(Library(**response_two.json()))
    
    response_three = client.post(
        "/libraries", 
        headers={ "X-Key": api_key }, 
        json={
            "name": "Test Library C",
            "metadata": {"example": "valueC"}
        }
    )
    library_list.append(Library(**response_three.json()))

    response = client.get(
        "libraries",
        headers={ "X-Key": api_key },
    )

    data = response.json()
    returned_list = []
    for item in data:
        returned_list.append(Library(**item))


    # Compare the lists by checking that each created library is in the returned list
    library_list_ids = sorted([str(lib.id) for lib in library_list])
    returned_list_ids = sorted([str(lib.id) for lib in returned_list])

    assert library_list_ids == returned_list_ids








