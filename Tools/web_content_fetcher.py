import requests
from bs4 import BeautifulSoup
import re

def web_content_fetcher(url)->dict:
    if url=="" :
        return {
            "status":"error",
            "message":"empty url passed"
        }
    
    header={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response=requests.get(
            url,
            header,
            timeout=10
        )

        if response.status_code!=200:
            return{
                "status":"error",
                "message":f"responsed with status code {response.status_code}"
            }
        
        else:
            html_content=response.text
            soup=BeautifulSoup(html_content,"html.parser")
            unwanted_tags = ["script", "style", "nav", "footer", "header", "aside", "form"]

            for tag in unwanted_tags:
                for element in soup.find_all(tag):
                    element.decompose()
            
            text = soup.get_text(separator="\n")
            lines = text.split("\n")
            cleaned_lines = []

            for line in lines:
                line=line.strip()
                cleaned_lines.append(line)
                cleaned_text="\n".join(cleaned_lines)
                cleaned_text = re.sub(r"\s+", " ", cleaned_text)
            
            return {
                "url":url,
                "text":cleaned_text
            }
    
    except Exception as e:
        return Exception
        
    
        
if __name__=="__main__":
    url="https://react.dev/learn/installation"
    result=web_content_fetcher(url)
    print(result)