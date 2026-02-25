from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_youtube_content(video_id:list)->list:
    youtube_content=[]
    api=YouTubeTranscriptApi()
    for id in video_id:
        if id=="":
            return{
                "status":"error",
                "message":"video id is null or missing"
            }
        transcript=api.fetch(video_id)
        formatter=TextFormatter()
        text_transcript=formatter.format_transcript(transcript)
        youtube_content.append({
            "video_id":id,
            "text":text_transcript
        })
    return youtube_content

if __name__=="__main__":
    video_id=["SqcY0GlETPk","TtPXvEcE11E"]
    response=get_youtube_content(video_id)
    print(response)


    
