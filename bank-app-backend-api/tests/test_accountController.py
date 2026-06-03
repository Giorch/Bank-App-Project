from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
import mongomock
from controllers.accountController import router as accountRouter
from unittest.mock import patch

app = FastAPI()
app.include_router(accountRouter)
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


class TestGetAllAccounts:
    def test_success_GetAllAccounts(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/accounts")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_empty_GetAllAccounts(self, mockMongo):
        response = client.get("/api/accounts")
        assert response.status_code == 200
        assert response.json() == []
    
class TestGetAccountByName:
    def test_success_GetAccountsByName(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/accounts/search?name=John Smith")
        assert response.status_code == 200
        results = response.json()
        assert len(results) > 0
        for account_list in results:
            for a in account_list:
                assert "accountId" in a
                assert "accountType" in a
                assert "balance" in a

    def test_failure_GetAccountsByName(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/accounts/search?name=Jane Smith")
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"

class TestGetAccountByID:
    def test_success_GetAccountById(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/accounts/CHK100001")
        assert response.status_code == 200
        assert response.json()["accountId"] == "CHK100001"

    def test_failure_GetAccountById(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.get("/api/accounts/CHK999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"

class TestCreateAccount:
    def test_success_CreateAccount(self, mockMongo):
        seedCustomers(mockMongo)
        uid = str(mockMongo.find_one({"name": "John Smith"})["_id"])
        payload = {"accountType": "Savings", "balance": 2122}
        response = client.post(f"/api/accounts?customerId={uid}", json=payload)

        assert response.status_code == 200
        assert response.json()["balance"] == 2122
        assert response.json()["accountType"] == "Savings"

    def test_failure_CreateAccount(self, mockMongo):
        seedCustomers(mockMongo)
        payload = {"accountType": "Savings"}
        response = client.post("/api/accounts?customerId=000000000000000000000999", json=payload)
        assert response.status_code == 422 

        payload = {"accountType": "testing", "balance": 2122}
        uid = str(mockMongo.find_one({"name": "John Smith"})["_id"])
        response = client.post(f"/api/accounts?customerId={uid}", json=payload)
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid Account Type: testing"

        payload = {"accountType": "Savings", "balance": 2122}
        response = client.post("/api/accounts?customerId=000000000000000000000999", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"
class TestUpdateAccount:
    def test_success_UpdateAccount(self, mockMongo):
        seedCustomers(mockMongo)
        payload = {"accountType": "Checking","balance": 1111111}
        response = client.put("/api/accounts/CHK100001", json=payload)
        assert response.status_code == 200
        assert response.json()["accountType"] == "Checking"
        assert response.json()["balance"] == 1111111

        response = client.get("/api/accounts/CHK100001")
        assert response.status_code == 200
        assert response.json()["accountType"] == "Checking"
        assert response.json()["balance"] == 1111111

    def test_faliure_UpdateAccount(self, mockMongo):
        seedCustomers(mockMongo)
        payload = {"accountType": "Checking","balance": 1111111}
        response = client.put("/api/accounts/CHK99999", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"
        payload = {"accountType": "Testing","balance": 1111111}
        response = client.put("/api/accounts/CHK100001", json=payload)
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid Account Type: Testing"

class TestDeleteAccount:
    def test_success_DeleteAccount(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.delete("/api/accounts/CHK100001")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        response = client.get("/api/accounts/CHK100001")
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"

    def test_failure_DeleteAccount(self, mockMongo):
        seedCustomers(mockMongo)
        response = client.delete("/api/accounts/CHK99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"

