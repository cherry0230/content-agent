import anthropic
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_transcript(video_url: str) -> str:
    # Extract video ID from URL
    if "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")
    
    # Fetch transcript
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    
    # Join all text into one string
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
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response = message.content[0].text
    
    # Parse the response
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

def repurpose_video(video_url: str):
    print(f"\nFetching transcript for: {video_url}")
    transcript = get_transcript(video_url)
    print(f"Transcript fetched — {len(transcript)} characters")
    
    print("\nGenerating content...")
    content = generate_content(transcript)
    
    print("\n" + "="*50)
    print("INSTAGRAM CAPTION:")
    print(content.get("instagram", "Not generated"))
    
    print("\n" + "="*50)
    print("LINKEDIN POST:")
    print(content.get("linkedin", "Not generated"))
    
    print("\n" + "="*50)
    print("TWITTER THREAD:")
    for i, tweet in enumerate(content.get("twitter", []), 1):
        print(f"Tweet {i}: {tweet}")
    
    print("\n" + "="*50)
    print("BLOG INTRO:")
    print(content.get("blog", "Not generated"))
    
    print("\n" + "="*50)
    print("ALTERNATIVE TITLES:")
    for i, title in enumerate(content.get("titles", []), 1):
        print(f"{i}. {title}")

# Test with a video
if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    repurpose_video(url)