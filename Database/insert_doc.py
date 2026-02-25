from .mongo_client import *


def insert_document(meta_data: dict) -> dict:
    try:
        result = collection.insert_one(meta_data)

        print("Inserted ID:", result.inserted_id)

        return {
            "status": "success",
            "inserted_id": str(result.inserted_id)
        }

    except Exception as e:
        print("Mongo Error:", e)
        return {
            "status": "fail",
            "error": str(e)
        }

if __name__=="__main__":
    meta_data={
        "document_id":"00007",
        "source_type":"website",
        "source_info":"https://build.nvidia.com/mistralai/mistral-7b-inst",
        "topic":"react",
        "subtopic":"usestate",
    }
    result=insert_document(meta_data)
    print(result)
