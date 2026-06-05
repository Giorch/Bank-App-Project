from pymongo import MongoClient
from dotenv import load_dotenv
import os
 
load_dotenv()
 
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "BankApp")


if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")

try:
    # Disable SSL verification temporarily for testing
    client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
    db = client[DB_NAME]
    customersCollection = db["customers"]
    print("✅ MongoDB connected")
except Exception as e:
    print(f"Error: {e}")
    raise

 