# Content Repurposing Agent

An AI agent that takes any YouTube video URL and repurposes 
it into 5 content formats in under 60 seconds.

## What it does

Paste a YouTube URL and get:
- Instagram caption with hashtags
- LinkedIn post with key insights
- Twitter/X thread (5 tweets)
- Blog post intro paragraph
- 5 alternative video title ideas

## Tech Stack
Python · Anthropic Claude API · YouTube Transcript API · FastAPI

## How it works

1. Fetches the video transcript using YouTube Transcript API
2. Sends transcript to Claude via Anthropic API
3. Claude generates all 5 content formats simultaneously
4. Returns structured output ready to copy and post

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
pip install fastapi uvicorn anthropic youtube-transcript-api python-dotenv
```

### 4. Add your API key
Create a `.env` file:

ANTHROPIC_API_KEY=your_key_here

### 5. Run
```bash
python main.py
```
Enter any YouTube URL when prompted.

## Its in PROGRESS.........
