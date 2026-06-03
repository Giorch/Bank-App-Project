from fastapi import APIRouter, HTTPException
from bson import ObjectId
from data.database import customersCollection
from models.account import Account, NewAccount
 
router = APIRouter(prefix="/api", tags=["Accounts"])
 

def generateAccountId(accountType: str, count: int) -> str:
    prefix = "SAV10000" if accountType.lower() == "savings" else "CHK10000"
    return f"{prefix}{count}"
 
 
@router.get("/accounts")
def GetAllAccounts():
    ret = []
    for c in customersCollection.find():
        for a in c.get("accounts", []):
            ret.append(a)
    return ret
 
@router.get("/accounts/search")
def GetAccountByName(name: str):
    ret = []
    for c in customersCollection.find({"name": name}):
        ret.append(c.get("accounts", []))
    if not ret:
        raise HTTPException(status_code=404, detail="Account not found")
    return ret
 
@router.get("/accounts/{accountId}")
def GetAccountById(accountId: str):
    for c in customersCollection.find():
        for a in c.get("accounts", []):
            if a.get("accountId") == accountId:
                return a
    raise HTTPException(status_code=404, detail="Account not found")
 
@router.post("/accounts")
def CreateAccount(customerId: str, acc: NewAccount):
    if acc.accountType.lower() not in ["savings", "checking"]:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid Account Type: {acc.accountType}"
        )
    try:
        oid = ObjectId(customerId)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid customer ID format")
 
    customer = customersCollection.find_one({"_id": oid})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
 
    count = sum(len(c.get("accounts", [])) for c in customersCollection.find()) + 1
    new_account = {
        "accountId": generateAccountId(acc.accountType, count),
        "accountType": acc.accountType,
        "balance": acc.balance
    }
 
    customersCollection.update_one(
        {"_id": oid},
        {"$push": {"accounts": new_account}}
    )
    return new_account
 
 
@router.put("/accounts/{accountId}")
def UpdateAccount(accountId: str, acc: NewAccount):
    if acc.accountType.lower() not in ["savings", "checking"]:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid Account Type: {acc.accountType}"
        )
    result = customersCollection.update_one(
        {"accounts.accountId": accountId},
        {"$set": {
            "accounts.$.balance": acc.balance,
            "accounts.$.accountType": acc.accountType
        }}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Account not found")
 
    for c in customersCollection.find():
        for a in c.get("accounts", []):
            if a.get("accountId") == accountId:
                return a
 
@router.delete("/accounts/{accountId}")
def DeleteAccount(accountId: str):
   
    deleted_account = None
    for c in customersCollection.find():
        for a in c.get("accounts", []):
            if a.get("accountId") == accountId:
                deleted_account = a
                break
 
    if not deleted_account:
        raise HTTPException(status_code=404, detail="Account not found")
 
    customersCollection.update_one(
        {"accounts.accountId": accountId},
        {"$pull": {"accounts": {"accountId": accountId}}}
    )
    return deleted_account
 