from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent import get_transcript, generate_content
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class VideoRequest(BaseModel):
    url: str

class TranscriptRequest(BaseModel):
    transcript: str

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/repurpose")
@limiter.limit("5/minute")
def repurpose(request: Request, body: VideoRequest):
    try:
        transcript = get_transcript(body.url)
        content = generate_content(transcript)
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/repurpose-text")
@limiter.limit("5/minute")
def repurpose_text(request: Request, body: TranscriptRequest):
    try:
        content = generate_content(body.transcript)
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}