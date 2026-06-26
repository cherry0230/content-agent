import anthropic
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_transcript(video_url: str) -> str:
    if "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")
    
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    full_text = " ".join([entry.text for entry in transcript])
    return full_text

def generate_content(transcript: str) -> dict:
    prompt = f"""You are a content repurposing expert. 
Based on the following YouTube video transcript, generate:

1. INSTAGRAM CAPTION: An engaging caption with relevant hashtags (max 150 words)
2. LINKEDIN POST: A professional post with key insights (max 200 words)  
3. TWITTER THREAD: 5 tweets that break down the main points (each max 280 chars)
4. BLOG INTRO: An engaging first paragraph for a blog post (max 100 words)
5. VIDEO TITLES: 5 alternative title ideas for this video

TRANSCRIPT:
{transcript[:4000]}

Format your response exactly like this:
INSTAGRAM: [your caption here]
LINKEDIN: [your post here]
TWITTER: [tweet 1] | [tweet 2] | [tweet 3] | [tweet 4] | [tweet 5]
BLOG: [your intro here]
TITLES: [title 1] | [title 2] | [title 3] | [title 4] | [title 5]"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response = message.content[0].text
    result = {}
    
    for line in response.split("\n"):
        if line.startswith("INSTAGRAM:"):
            result["instagram"] = line.replace("INSTAGRAM:", "").strip()
        elif line.startswith("LINKEDIN:"):
            result["linkedin"] = line.replace("LINKEDIN:", "").strip()
        elif line.startswith("TWITTER:"):
            tweets = line.replace("TWITTER:", "").strip().split(" | ")
            result["twitter"] = tweets
        elif line.startswith("BLOG:"):
            result["blog"] = line.replace("BLOG:", "").strip()
        elif line.startswith("TITLES:"):
            titles = line.replace("TITLES:", "").strip().split(" | ")
            result["titles"] = titles
    
    return result