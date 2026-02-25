from openai import OpenAI
import json
import uuid

client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = "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"
    )

def make_meta_data(query,source_type,source_url)->dict:
    prompt = f"""
        Extract the main technical topic and subtopic from the following query.

        Return output strictly in JSON format:
        {{
        "topic": "single word if possible",
        "subtopic": "short phrase"
        }}

        Query: {query}

        Only return JSON. No explanations.
    """

   
    completion = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct-v0.3",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=False
    )

    response=completion.choices[0].message.content.strip()
    
    try:
        parsed=json.loads(response)
        topic=parsed.get("topic","general").lower()
        subtopic=parsed.get("subtopic").lower()
    except:
        topic="general"
        subtopic=query.lower()
    
    return {
        "document_id": str(uuid.uuid4()),
        "source_type": source_type,
        "source_info": source_url,
        "topic": topic,
        "subtopic": subtopic
    }

if __name__=="__main__":
    query="I want to learn react usestate"
    source_type="website"
    source_url="https://build.nvidia.com/mistralai/mistral-7b-instruct-v03"
    response=make_meta_data(query,source_type,source_url)
    print(response)