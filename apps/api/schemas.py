from typing import List, Optional
from pydantic import BaseModel, Field


# --- Request Models ---
class TripPlanRequest(BaseModel):
    destination: str = Field(..., description="Destination city or country")
    days: int = Field(..., ge=1, le=30, description="Duration of the trip in days")
    budget: float = Field(..., gt=0, description="Total budget in USD")
    interests: List[str] = Field(default_factory=list, description="List of traveler interests (e.g. food, art, nature)")
    travel_style: Optional[str] = Field("balanced", description="e.g. budget, luxury, relaxed, fast-paced")


# --- Structured LLM Output Models (With Resilient Defaults) ---
class Activity(BaseModel):
    time_of_day: str = Field("Morning", description="e.g. Morning, Afternoon, Evening")
    activity_name: str = Field(..., description="Name of the activity or attraction")
    description: str = Field("", description="Brief description of what to do")
    estimated_cost: float = Field(0.0, description="Approximate cost in USD")


class DayPlan(BaseModel):
    day: int = Field(..., description="Day number (1, 2, 3...)")
    theme: str = Field(..., description="Theme for the day, e.g. 'Historic Highlights'")
    activities: List[Activity] = Field(default_factory=list, description="List of activities for this day")
    meal_suggestion: Optional[str] = Field(
        "Enjoy local cafes and street food in the area.", 
        description="Recommended local food or dining spot"
    )


class TripItinerary(BaseModel):
    trip_title: str = Field(..., description="Catchy title for the trip")
    destination: str
    total_days: int
    estimated_total_cost: float
    budget_breakdown: str = Field(..., description="Short explanation of how budget is allocated")
    daily_plan: List[DayPlan]
    travel_tips: List[str] = Field(
        default_factory=list, 
        description="Practical tips for this destination"
    )


# --- API Endpoint Response ---
class TripPlanResponse(BaseModel):
    success: bool
    data: TripItinerary