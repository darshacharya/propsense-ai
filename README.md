# TrendIQ — Bangalore Real Estate Intelligence

Multi-agent AI system that tells you **if** you should invest in a Bangalore locality — and **why**.

## Architecture

```
User Input (Location + Budget)
        │
        ▼
┌─────────────────────┐
│  Researcher Agent    │  → Collects market data (pricing, infra, trends)
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌──────────┐ ┌──────────────┐
│ Analyst  │ │ Investigator │
│ Agent    │ │ Agent        │
│ (price)  │ │ (why/risks)  │
└────┬─────┘ └──────┬───────┘
     └───────┬──────┘
             ▼
     ┌──────────────┐
     │ Reporter     │  → Final verdict with score + reasoning
     │ Agent        │
     └──────────────┘
             │
             ▼
     ┌──────────────┐
     │ Streamlit UI │  → Map + Verdict Card + Insights
     └──────────────┘
```

**4 Agents:**
- **Researcher** — collects structured market data for the location
- **Analyst** — evaluates pricing, ROI, rental yield, budget feasibility
- **Investigator** — uncovers WHY trends exist, pain points, hidden risks
- **Reporter** — synthesizes everything into a scored investment report

## Dataset

14 Bangalore localities with synthetic data covering:
- Price per sqft (min/max/avg)
- Trend direction and YoY growth
- Demand level and rental yields
- Infrastructure and connectivity
- Upcoming projects
- Buyer sentiment (pros/cons/score)
- GPS coordinates for map visualization

## Setup

```bash
cd trendiq
pip install -r requirements.txt
cp .env.example .env
# Add your API key to .env
```

## Run

**Streamlit UI (recommended):**
```bash
streamlit run app.py
```

**CLI:**
```bash
python main.py --location "Whitefield" --budget 80
```

## Tech Stack

- **CrewAI** — multi-agent orchestration
- **Gemini / OpenAI / Groq** — LLM reasoning
- **Streamlit** — web UI
- **Folium** — map visualization
- **Static JSON** — Bangalore synthetic dataset
