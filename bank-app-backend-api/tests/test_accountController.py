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

