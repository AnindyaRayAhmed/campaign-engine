# Multi-Agent Content Campaign Engine (Google ADK + Gemini)

Simple, hackathon-ready multi-agent system:

User input → Idea Agent → Copy Agent → Planner Agent → Save to SQLite.

## 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env .env.local  # optional copy for local edits
```

Edit `.env` and set your `GOOGLE_API_KEY`.

## 2) Run locally

```bash
adk web
```

When prompted, send a message like:

```text
Create a campaign for Sparkling Protein Water
```

## 3) Expected output

The final response is structured as:

- Campaign Idea
- Ad Copy (Headline, Description, CTA)
- Posting Plan (Platform, Schedule)
- Saved Campaign ID

## 4) Deploy to Cloud Run

From this project directory:

```bash
adk deploy cloud_run
```

Tip: in production, inject secrets (like `GOOGLE_API_KEY`) via Cloud Run + Secret Manager.

## 5) Files

- `agent.py`: Main orchestration pipeline
- `sub_agents.py`: Idea/Copy/Planner LLM agents
- `tools.py`: Simulated MCP-style tools (`save_campaign`, `get_campaigns`)
- `db.py`: SQLite persistence layer
