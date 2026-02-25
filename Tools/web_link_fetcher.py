from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

load_dotenv()
serp_api_key=os.getenv("SERP_API_KEY")

def get_website_link(query)->list:
    params={
        "q":query,
        "api_key":os.getenv("SERP_API_KEY"),
        "hl":"en",
        "engine":"google"
    }
    search=GoogleSearch(params)
    result=search.get_dict()
    organic_result=result.get("organic_results",[])
    clean_results=[]
    for item in organic_result[:3]:
        clean_results.append({
            "title":item.get("title"),
            "url":item.get("link"),
            "snippet":item.get("snippet")
        })
    return clean_results
        
        
if __name__=="__main__":
    params={
        "q":"React setup from react documentation",
        "api_key":serp_api_key,
        "hl":"en",
        "engine":"google"
    }
    res=get_website_link(params)
    print(res)
    # url="https://react.dev/learn'"
    # result=get_website_content(url)
    # print(result)