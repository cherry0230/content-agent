# ContentAI — Content Repurposing Agent

An AI-powered web app that turns any YouTube video into 5 ready-to-publish content formats in under 60 seconds.

**Built with:** Python · FastAPI · Anthropic Claude API · Docker · AWS EC2 · AWS ECR

---

## What it does

Paste a YouTube URL or video transcript and instantly get:

- Instagram caption with hashtags
- LinkedIn post with key insights
- Twitter/X thread (5 tweets)
- Blog post intro paragraph
- 5 alternative video title ideas

---

## Architecture

    Browser → FastAPI (Python) → Anthropic Claude API
                              → YouTube Transcript API
    Docker container → AWS ECR → AWS EC2

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| AI | Anthropic Claude API (claude-sonnet-4-6) |
| Transcript | YouTube Transcript API |
| Containerisation | Docker |
| Registry | AWS ECR |
| Deployment | AWS EC2 |
| Rate Limiting | SlowAPI (5 req/min per IP) |

---

## Project Structure

    content-agent/
    ├── main.py          # FastAPI server + routes
    ├── agent.py         # AI logic (transcript + generation)
    ├── index.html       # Frontend UI
    ├── requirements.txt # Python dependencies
    ├── Dockerfile       # Container definition
    └── .env             # API keys (never committed)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/cherry0230/content-agent.git
cd content-agent
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file:

ANTHROPIC_API_KEY=your_key_here

### 5. Run locally

```bash
uvicorn main:app --reload
```

Open: localhost:8000

---

## Run with Docker

```bash
docker build -t content-agent .
docker run -p 8000:8000 --env-file .env content-agent
```

---

## Deploy to AWS EC2

### 1. Push image to ECR

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-south-1.amazonaws.com

docker buildx build --platform linux/amd64 -t <account-id>.dkr.ecr.ap-south-1.amazonaws.com/content-agent:latest --push .
```

### 2. Launch EC2 and run container

```bash
ssh -i your-key.pem ubuntu@<public-ip>

sudo docker pull <account-id>.dkr.ecr.ap-south-1.amazonaws.com/content-agent:latest

sudo docker run -d -p 80:8000 -e ANTHROPIC_API_KEY=your_key <account-id>.dkr.ecr.ap-south-1.amazonaws.com/content-agent:latest
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Serves the web UI |
| POST | /repurpose | Generate content from YouTube URL |
| POST | /repurpose-text | Generate content from pasted transcript |

---

## Security

- API keys stored in environment variables only
- Never committed to version control
- Rate limiting: 5 requests per minute per IP
- Input validation via Pydantic models

---

## Known Limitations

- YouTube URL mode is blocked on AWS IPs due to YouTube's cloud provider policy
- Use the Paste Transcript mode when running on cloud servers
- Video must have captions enabled for the URL mode to work

---

## Roadmap

- Add authentication via API key header
- HTTPS with custom domain
- AWS Secrets Manager for secure key storage
- Support for additional output formats
- Batch processing for multiple videos