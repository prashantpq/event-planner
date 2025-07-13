def estimate_budget(number_of_people: int, place_name: str = "Generic Cafe"):
    """
    Returns estimated total and per person budget.
    """
    import random

    avg_cost_per_person = random.randint(100, 500)
    total_budget = avg_cost_per_person * number_of_people

    return {
        "currency": "INR",
        "total_budget": total_budget,
        "per_person_cost": avg_cost_per_person
    }
