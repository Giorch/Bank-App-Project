from fastapi import APIRouter, HTTPException
from data.store import customers, generateAccountId
from models.account import Account, NewAccount
router = APIRouter(prefix="/api", tags=["Accounts"])

@router.get("/accounts")
def GetAllAccounts():
    ret = []
    for c in customers:
        for a in c.accounts:
            ret.append(a)

    return ret

@router.get("/accounts/search")
def GetAccountByName(name: str):
    ret = []
    for c in customers:
        if c.name == name:
            ret.append(c.accounts)
    if not ret:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )
    return ret

@router.get("/accounts/{accountId}")
def GetAccountById(accountId: int):

    ret = next((a for c in customers for a in c.accounts if a.id == accountId), None)
    if not ret:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )
    return ret

@router.post("/accounts")
def CreateAccount(customerId: int, acc: NewAccount):
    newId = generateAccountId()
    for c in customers:
        if customerId == c.id:
            prefix = "SAV10000" if acc.accountType.lower() == "savings" else "CHK10000"
            accId = f"{prefix}{newId}"
            acc = Account(
                id= newId,
                accountId = accId,
                accountType = acc.accountType,
                balance = acc.balance
            )
            c.accounts.append(acc)
            return acc
        
    raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

@router.put("/accounts/{id}")
def UpdateAccount(id: int, acc: NewAccount):
    for c in customers:
        for a in c.accounts:
            if a.id == id:
                a.balance = acc.balance
                a.accountType = acc.accountType
                return a
    raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

@router.delete("/accounts/{id}")
def DeleteAccount(id: int):
    for c in customers:
        for a in c.accounts:
            if a.id == id:
                c.accounts.remove(a)
                return a

    raise HTTPException(
            status_code=404,
            detail="Account not found"
        )
    




