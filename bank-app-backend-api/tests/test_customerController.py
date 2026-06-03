from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pytest
from controllers.customerController import router as customerRouter
import data.store as store
from models.customer import Customer, NewCustomer
from models.account import Account

app = FastAPI()
app.include_router(customerRouter)
 
client = TestClient(app)

def reset_store():
    store.customers.clear()
    store.customers.extend([
        Customer(
        id="1",
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
            id="2",
            name="Sarah Johnson",
            email="sarah.johnson@email.com",
            accounts=[
                Account(
                    id=3, accountId="CHK100002", accountType="Checking", balance=1800
                )
            ]
        ),
        Customer(
            id="3",
            name="Michael Davis",
            email="michael.davis@email.com",
            accounts=[
                Account(
                    id=4, accountId="SAV100002", accountType="Savings", balance=25000
                )
            ]
        ),
        Customer(
            id="4",
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
            id="5",
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

class TestGetAllCustomers:
    def test_success_GetAllCustomers(self):
        response = client.get("/api/customers")
        assert response.status_code == 200
        assert len(response.json()) == store.globalCustomerCount
    def test_empty_GetAllCustomers(self):
        store.customers.clear()
        response = client.get("/api/customers")
        assert response.status_code == 200
        assert response.json() == []
    
class TestGetCustomerByName:
    def test_success_GetCustomersByName(self):
        response = client.get("/api/customers/search?name=John Smith")
        assert response.status_code == 200
        assert response.json()[0]["name"] == "John Smith"
    def test_failure_GetCustomersByName(self):
        response = client.get("/api/customers/search?name=Jane Smith")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"
class TestGetAllPremiumCustomers:
    def test_success_GetAllPremiumCustomers(self):
        response = client.get("/api/customers/premium")
        assert response.status_code == 200
        customers = response.json()
        assert len(customers) > 0
        for customer in customers:
            total_balance = sum(a["balance"] for a in customer["accounts"])
            assert total_balance > 5000
    def test_failure_GetAllPremiumCustomers(self):
        # Set all balances to 0
        for c in store.customers:
            for a in c.accounts:
                a.balance = 0
        response = client.get("/api/customers/premium")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customers not found"
class TestGetCustomerByID:
    def test_success_GetCustomerById(self):
        response = client.get("/api/customers/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["name"] == "John Smith"
    def test_failure_GetCustomerById(self):
        response = client.get("/api/customers/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"

class TestCreateCustomer:
    def test_success_CreateCustomer(self):
        payload = {"name": "Alice Brown", "email": "alice@email.com", "accounts": []}
        response = client.post("/api/customers", json=payload)
        assert response.status_code == 200
        assert response.json()["name"] == "Alice Brown"
        assert response.json()["id"] == 6
    def test_failure_CreateCustomer(self):
        payload = {"name": "No Email"}
        response = client.post("/api/customers", json=payload)
        assert response.status_code == 400
        payload = {"email": "noName@missing.com", "accounts": []}
        response = client.post("/api/customers", json=payload)
        assert response.status_code == 400
class TestUpdateCustomer:
    def test_success_UpdateCustomer(self):
        payload = {"name": "John Updated", "email": "new@email.com", "accounts": []}
        response = client.put("/api/customers/1", json=payload)
        assert response.status_code == 200
        assert response.json()["name"] == "John Updated"
        assert response.json()["email"] == "new@email.com"
        response = client.get("api/customers/1")
        assert response.status_code == 200
        assert response.json()["name"] == "John Updated"
        assert response.json()["email"] == "new@email.com"

    def test_faliure_UpdateCustomer(self):
        payload = {"name": "Ghost", "email": "ghost@email.com", "accounts": []}
        response = client.put("/api/customers/999", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"
        payload = {"name": "NoEmail", "accounts": []}
        response = client.put("/api/customers/1", json=payload)
        assert response.status_code == 400
        payload = {"email": "noName@missing.com", "accounts": []}
        response = client.put("/api/customers/1", json=payload)
        assert response.status_code == 400

class TestDeleteCustomer:
    def test_success_DeleteCustomer(self):
        response = client.delete("/api/customers/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        response = client.get("/api/customers/1")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"

    def test_failure_DeleteCustomer(self):
        response = client.delete("/api/customers/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"
        
    




