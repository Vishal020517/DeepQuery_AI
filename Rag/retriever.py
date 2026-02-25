from .store_vector import *
from .embedder import *


def retrieve_vectors(query:str,top_k:int=5):
    emb_query=embed_query(query)
    result=collection.query(
        query_embeddings=[emb_query],
        n_results=top_k
    )
    documents = result["documents"][0]
    metadatas = result["metadatas"][0]

    return documents,metadatas