from langgraph.graph import StateGraph, END
from schemas.state import EventPlannerState
from tools.agent_tools import nlu_tool, slot_generator_tool, location_finder_tool, budget_estimator_tool

graph = StateGraph(EventPlannerState)

graph.add_node("nlu", lambda state: nlu_tool.run({"user_input": state.user_input}))
graph.add_node("slot", lambda state: slot_generator_tool.run({
    "start_date": state.start_date,
    "end_date": state.end_date,
    "duration_hours": state.duration_hours
}))
graph.add_node("location", lambda state: location_finder_tool.run({
    "location": state.location
}))
graph.add_node("budget", lambda state: budget_estimator_tool.run({
    "duration_hours": state.duration_hours,
    "num_people": state.num_people,
    "location": state.location
}))

graph.set_entry_point("nlu")

graph.add_edge("nlu", "slot")
graph.add_edge("slot", "location")
graph.add_edge("location", "budget")
graph.add_edge("budget", END)
