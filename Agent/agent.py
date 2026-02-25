import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Tools.web_content_fetcher import *
from Tools.web_link_fetcher import *
from Tools.youtube_content_fetcher import *
from Tools.youtube_vid_fetcher import *
from Utils.topic_extractor import *
from Utils.meta_data_checker import *
from Utils.meta_data_maker import *
from Rag.rag_pipeline import *
from Database.insert_doc import *
from Rag.chunker import *
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)


prompt=f"""
You are an AI assistant,your work is to reply the user with the content they ask for.
You should be in an loop of thought,action,observation and repeat until you get an final answer.

I'll now provide you the set of tools that I have 

TOOLS:

1.extract_topic:
-Use this tool to extract the topic and subtopic from the user query
-This will be the first and compulsory step you should do for evry query you get
-Input:query(eg:"what is the meant by cell in biology")

2.check_metaData:
-Use this tool to check if the data is available in our databse
-This is the second thing that you should call after extract topic so that it will help you to decide which tool to call next.
-Input:topic(eg:"Biology),subtopic(eg:"cell")

3.generate_answer:
-Use this tool if you got the status as found from the check_metaData tool
-This tool helps you to fetch the relevant content from the vector db and generate an answer
-Once you retrieved the answer you no need to continue the loop you can stop by giving the Final answer using the generate answers output
-Input:query(eg:"what is cell in biology)

4.get_website_link:
-This tool allows you to get the url of the websites of the query that you give
-Use this tool if the output from the check_metaData is not_found
-Input:query(eg:"what is cell in biology)

5.web_content_fetcher:
-After the get_website_link tool you need to immidiately call this tool
-This tool allows you to get the content from an given website link
-Input:url(eg:"some url")

6.get_youtube_video_id:
-This tool should be called only if the user specifies youtube in their query
-It is used to retrieve the youtube video id 
-Input:query(eg:"react tutorial")

7.get_youtube_transcription:
-This tool should be called after you got the youtube video id
-this will help you to transcript the youtube video and store them as content
-Input:video_id(eg:"v123")

8.make_meta_data:
-Use this tool to make meta data if the check_metaData returned status as not found,this tool should be called after fetched content from the web_content_fetcher tool or from the get_youtube_transcription tool
-This will make meta data of the new content we have got from the web_content_fetcher or geet_youtube_transcription
-Input:query(eg:"explain me about cell in biology),source_type(eg:"webiste"),source_url(eg:"some url")

9.insert_document:
-Once the make_meta_data function is returned its output using that meta data you should execute this action it is very important,you should not skip this action this action should be performed immidiately after creating an new meta data
-This tool should be called for inserting the meta data to the mongodb
-This tool should be called only after calling the action make_meta_data
-Input:query(eg:"meta_data={{
        "document_id":"00007",
        "source_type":"website",
        "source_info":"https://build.nvidia.com/mistralai/mistral-7b-inst",
        "topic":"react",
        "subtopic":"usestate",
    }}")

10.chunker:
-After getting the content from the web_content_fetcher or from the get_youtube_transcript you need to chunk them ,embed them and store them in vector db so use this.
-Input:raw_text(eg:"some raw text"),meta_data(eg:"some meta data in json format)

So these are the tools that you should use,use this wisely

RULES:

1.You should only use the specified actions
2.Dont give the final answer directly
3.You should return only one action at an time
4.Dont give any spacing or special characters because it will provide parsing errors
5.Always respond in an strict Json format
6.Give the action with "Action:" keyword
7.Give the input for the action with "Action Input:" keyword
8.If you got the final answer give it with "Final Answer:" keyword

Some basic rules:
-Action Input MUST always be a JSON object.
-Never send string inputs like "topic=...,subtopic=...".
-Always send structured JSON with proper key names.

FORMAT RULE:

If calling check_metaData, you MUST send:
{
{
  "Action": "check_metaData",
  "Action Input": {
    "topic": "<string>",
    "subtopic": "<string>"
  }
}}
So always be in an loop follow the rules and work properly

If calling insert_document, you MUST send:

{{
  "Action": "insert_document",
  "Action Input": {{
    "meta_data": {{
      "document_id": "<uuid>",
      "source_type": "<string>",
      "source_info": "<string>",
      "topic": "<string>",
      "subtopic": "<string>"
    }}
  }}
}}


Let me now tell you the work flow first the user will give the query using that query you have to extract the topic and subtopic so with that topic and subtopic you need to check the mongodb if the meta data exist if exist then you can call the generate answer directly if not exist you should get youtube video id or else website link and then after getting the link you need to fetch the content from that url okay then after that you have to create an meta data of the fethced document then insert them in mongodb after that you should chunk the content you have fetched embed them and store in vectordb and after that you should call generate answer for final answers like this it should work so follow the exact same workflow given 
"""

Tools={
    "extract_topic":extract_topic,
    "check_metaData":check_metaData,
    "make_meta_data":make_meta_data,
    "generate_answer":generate_answer,
    "get_website_link":get_website_link,
    "web_content_fetcher":web_content_fetcher,
    "get_youtube_video_id":get_youtube_videoID,
    "get_youtube_transcription":get_youtube_content,
    "chunker":chunker,
    "insert_document":insert_document

}

def run_agent(query,max_steps=20):
    messages=[
        {"role":"system","content":prompt},
        {"role":"user","content":query}
    ]
    for step in range(max_steps):
        response=client.chat.completions.create(
            model="nvidia/nemotron-3-nano-30b-a3b",
            messages=messages,
            temperature=0.2
        )
        reply = response.choices[0].message.content
        print("\nLLM Output:\n", reply)

        try:
            parsed=json.loads(reply)
        except Exception as e:
            return f"Parsing error: {e}"
        
        if "Final Answer" in parsed:
            return parsed["Final Answer"]
        
        action=parsed.get("Action")
        action_input=parsed.get("Action Input")

        if not action:
            return "Error: No action provided by the model"
        
        if action not in Tools:
            return f"Error: Unknown action{action},not pesent in tools"
        
        if not isinstance(action_input,dict):
            return f"Error: Action Input must be a JSON object."
        elif isinstance(action_input, dict):
            parsed_input = action_input
        else:
            return "Error: Invalid action input format"
        
        try:
            observation=Tools[action](**parsed_input)
        except Exception as e:
            return f"Tool exceution error :{e}"
        
        print("Tool called:", action)
        print("Observation:", observation)


        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": json.dumps({"Observation": observation})})


    return "Max steps reached without final answer."



if __name__ == "__main__":
    user_query = input()
    answer = run_agent(user_query)
    print("\nFinal Answer:\n", answer)