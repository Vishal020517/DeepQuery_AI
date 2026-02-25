from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mogo_uri=os.getenv("MONGO_URI")

client=MongoClient(mogo_uri)

db=client["EDU_AGENT"]
collection=db["Documents"]
