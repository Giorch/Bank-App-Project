from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pytest
from controllers.accountController import router as accountRouter
import data.store as store
from models.customer import Customer
from models.account import Account

app = FastAPI()
app.include_router(accountRouter)
 
client = TestClient(app)

def reset_store():
    store.customers.clear()
    store.customers.extend([
        Customer(
        id=1,
        name="John Smith",
        email="john.smith@email.com",
        accounts=[
            Account(
                id=1, accountId="CHK100001", accountType="Checking", balance=2500
            ),
            Account(
                id=2, accountId="SAV100001", accountType="Savings", balance=10000
            )
            ]
        ),
        Customer(
            id=2,
            name="Sarah Johnson",
            email="sarah.johnson@email.com",
            accounts=[
                Account(
                    id=3, accountId="CHK100002", accountType="Checking", balance=1800
                )
            ]
        ),
        Customer(
            id=3,
            name="Michael Davis",
            email="michael.davis@email.com",
            accounts=[
                Account(
                    id=4, accountId="SAV100002", accountType="Savings", balance=25000
                )
            ]
        ),
        Customer(
            id=4,
            name="Emily Wilson",
            email="emily.wilson@email.com",
            accounts=[
                Account(
                    id=5, accountId="CHK100003", accountType="Checking", balance=3200
                ),
                Account(
                    id=6, accountId="SAV100003", accountType="Savings", balance=7800
                )
            ]
        ),
        Customer(
            id=5,
            name="David Martinez",
            email="david.martinez@email.com",
            accounts=[
                Account(
                    id=7, accountId="CHK100004", accountType="Checking", balance=950
                )
            ]
        )

    ])
    store.globalCustomerCount = 5
    store.globalAccountCount  = 7

@pytest.fixture(autouse=True)
def fresh_store():
    reset_store()


class TestGetAllAccounts:
    def test_success_GetAllAccounts(self):
        response = client.get("/api/accounts")
        assert response.status_code == 200
        assert len(response.json()) == store.globalAccountCount
    def test_empty_GetAllAccounts(self):
        store.customers.clear()
        response = client.get("/api/accounts")
        assert response.status_code == 200
        assert response.json() == []
    
class TestGetAccountByName:
    def test_success_GetAccountsByName(self):
        response = client.get("/api/accounts/search?name=John Smith")
        assert response.status_code == 200
        results = response.json()
        assert len(results) > 0
        for account_list in results:
            for a in account_list:
                assert "accountId" in a
                assert "accountType" in a
                assert "balance" in a
    def test_failure_GetAccountsByName(self):
        response = client.get("/api/accounts/search?name=Jane Smith")
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"

class TestGetAccountByID:
    def test_success_GetAccountById(self):
        response = client.get("/api/accounts/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["accountId"] == "CHK100001"
    def test_failure_GetAccountById(self):
        response = client.get("/api/accounts/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"

class TestCreateAccount:
    def test_success_CreateAccount(self):
        payload = {"accountType": "Savings", "balance": 2122}
        response = client.post("/api/accounts?customerId=1", json=payload)
        assert response.status_code == 200
        assert response.json()["balance"] == 2122
        assert response.json()["accountType"] == "Savings"
    def test_failure_CreateAccount(self):
        payload = {"accountType": "Savings"}
        response = client.post("/api/accounts?customerId=1", json=payload)
        assert response.status_code == 422 
        payload = {"accountType": "testing", "balance": 2122}
        response = client.post("/api/accounts?customerId=1", json=payload)
        assert response.status_code == 422 
        assert response.json()["detail"] == "Invalid Account Type: testing"
        payload = {"accountType": "Savings", "balance": 2122}
        response = client.post("/api/accounts?customerId=999", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"
class TestUpdateAccount:
    def test_success_UpdateAccount(self):
        payload = {"accountType": "Checking","balance": 1111111}
        response = client.put("/api/accounts/1", json=payload)
        assert response.status_code == 200
        assert response.json()["accountType"] == "Checking"
        assert response.json()["balance"] == 1111111
        response = client.get("/api/accounts/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["accountType"] == "Checking"
        assert response.json()["balance"] == 1111111

    def test_faliure_UpdateAccount(self):
        payload = {"accountType": "Checking","balance": 1111111}
        response = client.put("/api/accounts/999", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"
        payload = {"accountType": "Testing","balance": 1111111}
        response = client.put("/api/accounts/1", json=payload)
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid Account Type: Testing"

class TestDeleteAccount:
    def test_success_DeleteAccount(self):
        response = client.delete("/api/accounts/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        response = client.get("/api/accounts/1")
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"

    def test_failure_DeleteAccount(self):
        response = client.delete("/api/accounts/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Account not found"

