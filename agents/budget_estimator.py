# agents/budget_estimator.py

def estimate_budget(duration_hours, num_people, location):
    """
    Estimate event budget based on duration, number of people, and location.

    For simplicity:
    - Base rate per hour per person is assumed.
    - Location can adjust the rate if needed (currently same for all).

    Returns:
        dict: {
            "total_budget": float,
            "per_person_cost": float,
            "currency": str
        }
    """

    # Base assumptions (adjust as needed for your domain)
    base_rate_per_hour_per_person = 300  # in INR

    # Example: adjust for premium locations
    premium_locations = ["Bandra", "Juhu", "Powai"]
    if location.lower() in [loc.lower() for loc in premium_locations]:
        base_rate_per_hour_per_person *= 1.5  # 50% increase

    per_person_cost = base_rate_per_hour_per_person * duration_hours
    total_budget = per_person_cost * num_people

    return {
        "total_budget": round(total_budget, 2),
        "per_person_cost": round(per_person_cost, 2),
        "currency": "INR"
    }


if __name__ == "__main__":
    # Quick test
    result = estimate_budget(duration_hours=2, num_people=3, location="Malad")
    print(result)
