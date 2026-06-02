from pydantic import BaseModel

class NewAccount(BaseModel):
    accountType: str
    balance: int

class Account(NewAccount):
    id: int
    accountId: str
