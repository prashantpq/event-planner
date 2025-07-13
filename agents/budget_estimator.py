def estimate_budget(num_people, location):
    """
    Estimate event budget based on number of people and location.

    For simplicity:
    - Flat base rate per person is assumed.
    - Premium locations can adjust the rate.

    Returns:
        dict: {
            "total_budget": float,
            "per_person_cost": float,
            "currency": str
        }
    """

    # Base assumptions
    base_rate_per_person = 100  # in INR (e.g., average dinner buffet cost per person)

    per_person_cost = base_rate_per_person
    total_budget = per_person_cost * num_people

    return {
        "total_budget": round(total_budget, 2),
        "per_person_cost": round(per_person_cost, 2),
        "currency": "INR"
    }


# if __name__ == "__main__":
#     # Quick test
#     result = estimate_budget(num_people=3, location="Malad")
#     print(result)
