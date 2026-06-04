from pymongo import MongoClient
from dotenv import load_dotenv
import os
 
load_dotenv()
 
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "BankApp")

print(MONGO_URI) #Render debugging
print(DB_NAME)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
 
customersCollection = db["customers"]
 