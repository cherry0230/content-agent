from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent import get_transcript, generate_content

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/repurpose")
def repurpose(request: VideoRequest):
    try:
        transcript = get_transcript(request.url)
        content = generate_content(transcript)
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}