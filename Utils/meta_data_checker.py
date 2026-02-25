from Database.mongo_client import *

def check_metaData(topic:str,subtopic:str)->dict:
    query = {
        "topic": {"$regex": topic, "$options": "i"},
        "subtopic": {"$regex": subtopic, "$options": "i"}
    }
    results=list(collection.find(query))
    if results:
        document_ids=[doc["document_id"] for doc in results]
        return{
            "status":"found",
            "document_ids":document_ids
        }
    else:
        return{
            "status":"not_found",
            "document_ids":[]
        }
