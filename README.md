# ✈️ Trip Pilot AI

**Trip Pilot AI** is an AI-powered travel itinerary generation engine built with **FastAPI**, **Pydantic v2**, and **Groq LPUs** for ultra-fast, structured travel planning.

The service accepts traveler preferences (destination, duration, budget, travel style, interests) and generates a geographically grouped, budget-conscious, day-by-day travel plan with real-world activity and meal recommendations.

---

## 🌟 Core Capabilities

- **Strict Schema Enforcement:** Guarantees 100% valid JSON responses adhering to a typed Pydantic schema using constrained JSON decoding.
- **Geographic Activity Clustering:** Groups activities by geographic proximity to minimize transit time.
- **Budget Allocation:** Balances accommodation, transit, meal, and activity expenses within the traveler's stated budget.
- **Defensive Error Handling:** Uses Pydantic default fallbacks to ensure graceful degradation if optional descriptive fields are omitted.
- **Fast Inference:** Powered by Groq's LPU inference engine running `openai/gpt-oss-120b`, returning complete itineraries in under 2 seconds.

---

## 🏗️ Architecture & Data Flow

```text
┌──────────────┐         POST /api/trip/plan         ┌─────────────────────────┐
│              │ ──────────────────────────────────> │                         │
│ Client / Web │                                     │  FastAPI Request Router │
│ (Swagger UI) │ <────────────────────────────────── │     (apps/api/main.py)  │
└──────────────┘           200 OK + JSON             └───────────┬─────────────┘
                                                                 │
                                                       Validates │ TripPlanRequest
                                                                 ▼
                                                     ┌─────────────────────────┐
                                                     │       LLM Service       │
                                                     │ (apps/api/service/llm)  │
                                                     └───────────┬─────────────┘
                                                                 │
                                                      Chat Prompt│ System Prompt + JSON Schema
                                                                 ▼
                                                     ┌─────────────────────────┐
                                                     │    Groq LPU Engine      │
                                                     │  (openai/gpt-oss-120b)  │
                                                     └───────────┬─────────────┘
                                                                 │
                                                       Raw JSON  │ Response
                                                                 ▼
                                                     ┌─────────────────────────┐
                                                     │    Pydantic Validator   │
                                                     │   (TripItinerary Model) │
                                                     └─────────────────────────┘
```

---

## 📁 Project Structure

```text
trip-pilot-ai/
├── apps/
│   ├── api/
│   │   ├── main.py          # FastAPI application & route definitions
│   │   ├── schemas.py       # Pydantic request & response validation models
│   │   └── service/
│   │       └── llm.py       # LLM client setup, system prompts, & inference logic
│   └── web/                 # Web application interface
├── docs/                    # Technical documentation
├── .env.example             # Template for environment variables
├── .gitignore               # Ignored files (protects credentials & venv)
└── README.md                # Project documentation
```

---

## 🛠️ Tech Stack & Configuration

| Component | Technology | Description |
| :--- | :--- | :--- |
| **API Framework** | FastAPI | Asynchronous web framework with automatic OpenAPI docs |
| **Data Validation** | Pydantic v2 | High-performance schema validation and serialization |
| **ASGI Server** | Uvicorn | Lightning-fast ASGI web server |
| **LLM Provider** | Groq Cloud | Ultra-low latency LPU inference |
| **Model** | `openai/gpt-oss-120b` | High-capacity open weights model with JSON mode |
| **Sampling Params** | Temperature: `0.3` | Low temperature to ensure factual consistency and schema adherence |
| **SDK** | OpenAI Python SDK | Standardized client configured with Groq `base_url` |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- A free Groq API key from [console.groq.com](https://console.groq.com/)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/anujkashyap18/trip-pilot-ai.git
cd trip-pilot-ai

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic openai python-dotenv
```

### 3. Configure Environment
Create your `.env` file from the provided example:
```bash
cp .env.example .env
```
Edit `.env` and set your Groq API key:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 4. Run the API Server
```bash
uvicorn apps.api.main:app --reload --port 8000
```

---

## 📖 API Documentation & Testing

FastAPI automatically generates interactive, self-documenting OpenAPI schemas directly from your Pydantic models.

When the server is running, visit:
- **Swagger UI (Interactive):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc (Specification):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Quick Smoke Test (cURL)
Test the plan generation endpoint directly from your terminal:

```bash
curl -X POST "http://127.0.0.1:8000/api/trip/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Kyoto, Japan",
    "days": 3,
    "budget": 1200,
    "interests": ["temples", "street food", "gardens"],
    "travel_style": "balanced"
  }'
```

---

## 📄 License
MIT License.