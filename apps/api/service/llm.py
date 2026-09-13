import os
from dotenv import load_dotenv
from openai import OpenAI
from apps.api.schemas import TripPlanRequest, TripItinerary

load_dotenv()

# Groq client:
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

# 1. Define constants at the top:
SYSTEM_PROMPT = """
You are a professional travel planning assistant.

Create practical, well-paced travel itineraries based on:
- destination
- dates/duration
- budget
- interests
- travel style

Guidelines:
1. Never invent precise real-time information (e.g., real-time train timings, current ticket stock).
2. Keep budget recommendations realistic based on the destination.
3. Optimize geography: group activities close to each other on the same day to minimize transit time.
4. You MUST respond with ONLY valid JSON matching this schema:
{
  "trip_title": "string",
  "destination": "string",
  "total_days": int,
  "estimated_total_cost": float,
  "budget_breakdown": "string",
  "daily_plan": [
    {
      "day": int,
      "theme": "string",
      "activities": [
        {
          "time_of_day": "string",
          "activity_name": "string",
          "description": "string",
          "estimated_cost": float
        }
      ],
      "meal_suggestion": "string"
    }
  ],
  "travel_tips": ["string"]
}

CRITICAL:
- Every single day in daily_plan MUST include a meal_suggestion.
- The root object MUST include travel_tips as a list of strings.
"""


# 2. Define the service function:
def generate_trip_itinerary(request: TripPlanRequest) -> TripItinerary:
    user_prompt = f"""
    Please generate a {request.days}-day itinerary for {request.destination}.
    - Total Budget: ${request.budget:.2f} USD
    - Travel Style: {request.travel_style}
    - Interests: {', '.join(request.interests) if request.interests else 'General sightseeing'}

    Make sure the schedule is practical and respects the budget.
    Return only valid JSON.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    raw_json = response.choices[0].message.content
    return TripItinerary.model_validate_json(raw_json)