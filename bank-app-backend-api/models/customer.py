from pydantic import BaseModel, Field
from typing import List, Optional
from models.account import Account

class NewCustomer(BaseModel):
    name: str
    email: str
    accounts: List[Account] = []

class Customer(NewCustomer):
    id: Optional[str] = Field(default=None) 