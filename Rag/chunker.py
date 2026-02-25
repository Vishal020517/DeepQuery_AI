from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
from .embedder import *
from .store_vector import *

def chunker(raw_text,meta_data)->dict:

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(raw_text)
    chunk_list=[]

    for chunk in chunks:
        chunk_id=str(uuid.uuid4())

        chunk_metadata = {
            "document_id": meta_data["document_id"],
            "source_type": meta_data["source_type"],
            "source_info": meta_data["source_info"],
            "topic": meta_data["topic"],
            "subtopic": meta_data["subtopic"]
        }

        embedded_text=embed_text(chunk)
        store_vector(chunk_id,chunk,embedded_text,chunk_metadata)

        chunk_list.append({
            "chunk_id": chunk_id,
            "text": chunk,
            **chunk_metadata
        })


    return chunk_list

if __name__ == "__main__":
    raw_text = "Your long text here vheuhqir3hwewu1ruhg80bj1t4o-ernqf qhydugfc78trgu9hgrobuf g 89ybr9f7tbr7bt128qrhbn yrbqry8brbkjrjbvhrqv97 rubvh9rqyb79b "

    meta_data = {
        "document_id": "00002",
        "source_type": "website",
        "source_info": "https://example.com",
        "topic": "react",
        "subtopic": "usestate",
    }

    response = chunker(raw_text, meta_data)
    print(response)