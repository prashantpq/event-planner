from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class EventPlannerState(BaseModel):
    """
    State schema for the Event Planner Agentic AI system.
    Defines the entire state passed between agents in the LangGraph pipeline.
    """

    # Raw user input
    user_input: str = Field(..., description="User's original natural language request for event planning.")

    # Parsed NLU outputs
    event_name: Optional[str] = Field(None, description="Name or title of the event.")
    duration_hours: Optional[int] = Field(None, description="Duration of the event in hours.")
    start_date: Optional[str] = Field(None, description="Start date of the event (YYYY-MM-DD).")
    end_date: Optional[str] = Field(None, description="End date of the event (YYYY-MM-DD).")
    location: Optional[str] = Field(None, description="Location or area for the event.")
    num_people: Optional[int] = Field(2, description="Number of people attending. Defaults to 2.")

    feasible_slots: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="List of feasible time slots for the event.")

    nearby_places: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="List of nearby places (e.g. restaurants).")

    budget_estimate: Optional[Dict[str, float]] = Field(default_factory=dict, description="Estimated budget details for the event.")
