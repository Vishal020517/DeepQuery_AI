from openai import OpenAI
import os
from dotenv import load_dotenv
from .retriever import *

load_dotenv()

client = OpenAI(
    api_key="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",
    base_url="https://integrate.api.nvidia.com/v1"
)

def generate_answer(query: str):
    documents, _ = retrieve_vectors(query)

    context = "\n\n".join(documents)

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct-v0.3",
        messages=[
            {"role": "system", "content": "You are a helpful educational assistant. Answer only using the given context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content