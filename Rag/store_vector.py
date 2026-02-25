import chromadb
from chromadb.config import Settings

chroma_client = chromadb.Client(
    Settings(persist_directory="./chroma_db", is_persistent=True)
)

collection = chroma_client.get_or_create_collection(
    name="edu_collection"
)

def store_vector(chunk_id,chunk_text,embedded_text,meta_data):
    collection.add(
        ids=[chunk_id],
        documents=[chunk_text],
        embeddings=[embedded_text],
        metadatas=[meta_data]
    )