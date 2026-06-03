from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
import mongomock
from controllers.customerController import router as customerRouter
from unittest.mock import patch

app = FastAPI()
app.include_router(customerRouter)
client = TestClient(app)

@pytest.fixture(autouse=True)
def mockMongo():
    mock_col = mongomock.MongoClient().db["customers"]
    with patch("controllers.customerController.customersCollection", mock_col), \
         patch("controllers.accountController.customersCollection", mock_col):
        yield mock_col

def seedCustomers(collection):
    collection.insert_many([
        {
            "name": "John Smith",
            "email": "john.smith@email.com",
            "accounts": [
                {"id": 1, "accountId": "CHK100001", "accountType": "Checking", "balance": 2500},
                {"id": 2, "accountId": "SAV100001", "accountType": "Savings",  "balance": 10000}
            ]
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@email.com",
            "accounts": [
                {"id": 3, "accountId": "CHK100002", "accountType": "Checking", "balance": 1800}
            ]
        },
        {
            "name": "Michael Davis",
            "email": "michael.davis@email.com",
            "accounts": [
                {"id": 4, "accountId": "SAV100002", "accountType": "Savings", "balance": 25000}
            ]
        },
        {
            "name": "Emily Wilson",
            "email": "emily.wilson@email.com",
            "accounts": [
                {"id": 5, "accountId": "CHK100003", "accountType": "Checking", "balance": 3200},
                {"id": 6, "accountId": "SAV100003", "accountType": "Savings",  "balance": 7800}
            ]
        },
        {
            "name": "David Martinez",
            "email": "david.martinez@email.com",
            "accounts": [
                {"id": 7, "accountId": "CHK100004", "accountType": "Checking", "balance": 950}
            ]
        }
    ])



class TestGetAllCustomers:
    def test_success_GetAllCustomers(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/customers")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_empty_GetAllCustomers(self, mockMongo):
        response = client.get("/api/customers")
        assert response.status_code == 200
        assert response.json() == []
    
class TestGetCustomerByName:
    def test_success_GetCustomersByName(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/customers/search?name=John Smith")
        assert response.status_code == 200
        assert response.json()[0]["name"] == "John Smith"

    def test_failure_GetCustomersByName(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/customers/search?name=Jane Smith")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"
class TestGetAllPremiumCustomers:
    def test_success_GetAllPremiumCustomers(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/customers/premium")
        assert response.status_code == 200
        customers = response.json()
        assert len(customers) > 0
        for customer in customers:
            total_balance = sum(a["balance"] for a in customer["accounts"])
            assert total_balance > 5000

    def test_failure_GetAllPremiumCustomers(self, mockMongo):
        mockMongo.insert_many([
            {"name": "Poor Pete", "email": "pete@email.com", "accounts": [
                {"accountId": "CHK999", "accountType": "Checking", "balance": 100}
            ]},
            {"name": "Broke Bob", "email": "bob@email.com", "accounts": [
                {"accountId": "SAV999", "accountType": "Savings", "balance": 200}
            ]}
        ])
        response = client.get("/api/customers/premium")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customers not found"
class TestGetCustomerByID:
    def test_success_GetCustomerById(self, mockMongo):
        seedCustomers(mockMongo)
        uid = str(mockMongo.find_one({"name": "John Smith"})["_id"])
        response = client.get(f"/api/customers/{uid}")
        assert response.status_code == 200
        assert response.json()["id"] == uid
        assert response.json()["name"] == "John Smith"

    def test_failure_GetCustomerById(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/customers/000000000000000000000999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"

class TestCreateCustomer:
    def test_success_CreateCustomer(self, mockMongo):
        seedCustomers(mockMongo)
        payload = {"name": "Alice Brown", "email": "alice@email.com", "accounts": []}
        response = client.post("/api/customers", json=payload)
        assert response.status_code == 200
        assert response.json()["name"] == "Alice Brown"
        assert "id" in response.json()

    def test_failure_CreateCustomer(self, mockMongo):
        seedCustomers(mockMongo)
        payload = {"name": "No Email"}
        response = client.post("/api/customers", json=payload)
        assert response.status_code == 422
        payload = {"email": "noName@missing.com", "accounts": []}
        response = client.post("/api/customers", json=payload)
        assert response.status_code == 422
class TestUpdateCustomer:
    def test_success_UpdateCustomer(self, mockMongo):
        seedCustomers(mockMongo)
        uid = str(mockMongo.find_one({"name": "John Smith"})["_id"])
        payload = {"name": "John Updated", "email": "updated@email.com", "accounts": []}
        response = client.put(f"/api/customers/{uid}", json=payload)
        assert response.status_code == 200
        assert response.json()["name"] == "John Updated"
        assert response.json()["email"] == "updated@email.com"
        response = client.get(f"/api/customers/{uid}")
        assert response.status_code == 200
        assert response.json()["name"] == "John Updated"
        assert response.json()["email"] == "updated@email.com"

    def test_faliure_UpdateCustomer(self, mockMongo):
        seedCustomers(mockMongo)
        payload = {"name": "Ghost", "email": "ghost@email.com", "accounts": []}
        response = client.put("/api/customers/000000000000000000000999", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"
        payload = {"name": "NoEmail", "accounts": []}
        response = client.put("/api/customers/1", json=payload)
        assert response.status_code == 422
        payload = {"email": "noName@missing.com", "accounts": []}
        response = client.put("/api/customers/1", json=payload)
        assert response.status_code == 422

class TestDeleteCustomer:
    def test_success_DeleteCustomer(self, mockMongo):
        payload = {"name": "John New", "email": "new@email.com", "accounts": []}
        response = client.post("/api/customers", json=payload)
        assert response.status_code == 200
        uid = response.json()["id"]
        response = client.delete(f"/api/customers/{uid}")
        assert response.status_code == 200
        assert response.json()["name"] == "John New"
        response = client.get(f"/api/customers/{uid}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"

    def test_failure_DeleteCustomer(self, mockMongo):
        response = client.delete("/api/customers/000000000000000000000999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"
        
    




