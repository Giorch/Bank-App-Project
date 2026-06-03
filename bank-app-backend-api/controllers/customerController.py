from fastapi import APIRouter, HTTPException
from bson import ObjectId
from data.database import customersCollection
from models.customer import NewCustomer, Customer

router = APIRouter(prefix="/api", tags=["Customers"])

def docToCustomer(doc) -> dict:
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


@router.get("/customers")
def GetAllCustomers():
    return [docToCustomer(c) for c in customersCollection.find()]


@router.get("/customers/search")
def GetCustomerByName(name: str):
    results = [docToCustomer(c) for c in customersCollection.find({"name": name})]
    if not results:
        raise HTTPException(status_code=404, detail="Customer not found")
    return results

@router.get("/customers/premium")
def GetAllPremiumCustomers():
    ret = []
    for c in customersCollection.find():
        balance = sum(a["balance"] for a in c.get("accounts", []))
        if balance > 5000:
            ret.append(docToCustomer(c))
    if not ret:
        raise HTTPException(status_code=404, detail="Customers not found")
    return ret

@router.get("/customers/{customerId}")
def GetCustomerById(customerId: str):
    try:
        oid = ObjectId(customerId)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid customer ID format")
    doc = customersCollection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Customer not found")
    return docToCustomer(doc)


@router.post("/customers")
def CreateCustomer(c: NewCustomer):
    new_doc = {
        "name": c.name,
        "email": c.email,
        "accounts": [a.dict() for a in c.accounts]
    }
    result = customersCollection.insert_one(new_doc)
    print("Inserted ID:", result.inserted_id)
    new_doc["id"] = str(result.inserted_id)
    del new_doc["_id"]
    return new_doc


@router.put("/customers/{id}")
def UpdateCustomer(id: str, customer: NewCustomer):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid customer ID format")
    update = {
        "$set": {
            "name": customer.name,
            "email": customer.email,
            "accounts": [a.dict() for a in customer.accounts]
        }
    }
    result = customersCollection.find_one_and_update(
        {"_id": oid},
        update,
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return docToCustomer(result)

@router.delete("/customers/{id}")
def DeleteCustomer(id: str):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid customer ID format")
    doc = customersCollection.find_one_and_delete({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Customer not found")
    return docToCustomer(doc)