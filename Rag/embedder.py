from openai import OpenAI

client = OpenAI(
  api_key="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",
  base_url="https://integrate.api.nvidia.com/v1"
)

def embed_text(text:str)->list:
    response=client.embeddings.create(
        input=[text],
        model="nvidia/nv-embed-v1",
        encoding_format="float",
        extra_body={"input_type": "passage", "truncate": "NONE"}
    )
    return response.data[0].embedding

def embed_query(query:str)->list:
    response=client.embeddings.create(
        input=[query],
        model="nvidia/nv-embed-v1",
        encoding_format="float",
        extra_body={"input_type":"query","truncate":"NONE"}
    )
    return response.data[0].embedding


if __name__=="__main__":
    text="chjevojhr2ojvbeihviycirqdhjbp irh d8gf79qvgiosuhvb2jkr3vbiutqv78dtv98ryhqoiewbvijdgviyredv8rupogqhvorjbgduivhr90by8rguifughourh2g8"
    response=embed_text(text)
    print(response)