# Spike AI Analytics & SEO Agent

An agent-based AI backend system that answers natural-language marketing questions by orchestrating multiple specialized agents over real analytics and SEO datasets.

The system dynamically routes each query to the correct agent and always responds in clear, human-readable language rather than raw JSON or database output.

---

## Project Overview

This project demonstrates how AI agents can be used to reason over real-world marketing data sources such as Google Analytics and SEO crawl datasets.

Each query is interpreted using an LLM, routed to the appropriate agent, processed using deterministic logic, and returned as a natural-language explanation.

---

## Supported Data Sources

### Google Analytics 4 (GA4 Data API)

- Active users
- Total users
- Sessions
- Page views
- Time-based trends

### Screaming Frog SEO Crawl (Google Sheets)

- Meta descriptions
- Titles and headings
- Canonical tags
- Status codes (4xx / 5xx)
- Word count and content quality

### LiteLLM Proxy (Gemini Models)

- Intent extraction
- Natural-language explanation generation

---

## Architecture Overview

The backend follows an agent-based orchestration pattern.

POST /query
↓
Orchestrator
↓
Analytics Agent (GA4) OR SEO Agent (Google Sheets)
↓
Natural Language Response Generator (LLM)


Each agent:
- Extracts intent from the user query
- Queries its respective data source
- Applies deterministic business rules
- Produces a natural-language answer

---

## API Endpoint

### POST `/query`

Accepts a natural-language question and optionally a GA4 property ID.

### Request Body

```json
{
  "query": "Give me daily page views and users for the last 7 days",
  "propertyId": "GA4_PROPERTY_ID"
}

## Example Queries

### Analytics (GA4)
- Give me daily page views and users for the last 14 days
- How many active users did we have recently?

### SEO (Google Sheets)
- Find pages with missing meta descriptions
- Which pages have low word count?
- Show pages with 4xx or 5xx errors
- Find pages missing canonical tags

## Example Response
{
  "agent": "analytics",
  "answer": "I checked your Google Analytics data for the last 14 days, but there is currently no recorded traffic available. Once your website starts receiving users, this agent will provide daily trends and insights.",
  "data": {
    "metrics": ["screenPageViews", "activeUsers"],
    "dimensions": ["date"],
    "row_count": 0
  }
}

The system always responds in natural language, even when no data is available.

## Configuration
All environment-specific configuration is managed using a .env file.
# App
APP_PORT=8080

# LiteLLM
LITELLM_API_KEY=sk-...
LITELLM_BASE_URL=http://3.110.18.218
LITELLM_MODEL=gemini-1.5-flash

# SEO
SEO_SPREADSHEET_ID=1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VEE

Sensitive files such as credentials.json are excluded from version control.

## Running Instructions
Start the FastAPI server using Uvicorn.
uvicorn app.main:app --port 8080
http://127.0.0.1:8080/docs


## Design Principles

- Agent-based orchestration
- Deterministic fallbacks (no hallucination)
- Natural-language answers over raw JSON
- Clean separation of configuration and logic
- Production-style backend architecture

## Final Status

- GA4 Analytics Agent implemented
- SEO Agent (all sheets) implemented
- Natural-language responses enabled
- Clean configuration management


