from fastapi import HTTPException
from apps.api.service.llm import generate_trip_itinerary
from fastapi import FastAPI
from apps.api.schemas import TripPlanRequest, TripPlanResponse

app = FastAPI(title = "Trip Pilot AI API")

@app.post("/api/trip/plan", response_model= TripPlanResponse)
def plan_trip(request: TripPlanRequest):
    try:
        itinerary = generate_trip_itinerary(request)
        return TripPlanResponse(
            success= True,
            data=itinerary
        )
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail= f"Failed to generate trip plan: {str(e)}"
        )