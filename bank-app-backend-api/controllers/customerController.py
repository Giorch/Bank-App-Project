from fastapi import APIRouter, HTTPException
from data.store import customers, generateCustomerId
from models.customer import NewCustomer, Customer

router = APIRouter(prefix="/api", tags=["Customers"])

@router.get("/customers")
def GetAllCustomers():
    return customers

@router.get("/customers/search")
def GetCustomerByName(name: str):
    ret = []
    for c in customers:
        if c.name == name:
            ret.append(c)
    if not ret:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return ret

@router.get("/customers/premium")
def GetAllPremiumCustomers():
    ret = []
    for c in customers:
        balance = 0
        for a in c.accounts:
            balance += a.balance
        if balance > 5000:
            ret.append(c)
    if not ret:
        raise HTTPException(
            status_code=404,
            detail="Customers not found"
        )
    return ret

@router.get("/customers/{customerId}")
def GetCustomerById(customerId: int):
    ret = next((c for c in customers if c.id == customerId), None)
    if not ret:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return ret

@router.post("/customers")
def CreateCustomer(c: NewCustomer):
    newC = Customer(
        id= generateCustomerId(),
        name= c.name,
        email= c.email, 
        accounts= c.accounts,
        )
    customers.append(newC)
    return newC

@router.put("/customers/{id}")
def UpdateCustomer(id: int, customer: NewCustomer):
    for c in customers:
        if c.id == id:
            c.name = customer.name
            c.email = customer.email
            c.accounts = customer.accounts
            return c
        
    raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

@router.delete("/customers/{id}")
def DeleteCustomer(id: int):
    for c in customers:
        if c.id == id:
            customers.remove(c)
            return c
    raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
