from dotenv import load_dotenv
import requests
import os

load_dotenv()
youtube_api=os.getenv("YOUTUBE_API_KEY")

def get_youtube_videoID(query)->dict:
    endpoint_url="https://www.googleapis.com/youtube/v3/search"
    params={
        "part":"snippet",
        "q":query,
        "type": "video",
        "key":youtube_api,
        "maxResults":2
    }

    response=requests.get(endpoint_url,params=params,timeout=10)

    if response.status_code!=200:
        return{
            "status":"error",
            "message":f"responded with status code {response.status_code}"
        }
    
    data=response.json()
    result=[]

    for item in data["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        snippet=item.get("sinppet",{})
        result.append({
            "video_id":video_id,
            "title":title,
            "snippet":snippet
        })
    
    return result

    
    

if __name__=="__main__":
    response=get_youtube_videoID("react tutorial")
    print(response)
    