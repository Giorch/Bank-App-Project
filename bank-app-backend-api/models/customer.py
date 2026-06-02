from pydantic import BaseModel
from typing import List
from models.account import Account

class NewCustomer(BaseModel):
    name: str
    email: str
    accounts: List[Account] = []

class Customer(NewCustomer):
    id: int