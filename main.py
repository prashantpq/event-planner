import streamlit as st
from tools.agent_tools import (
    nlu_tool,
    slot_generator_tool,
    location_finder_tool,
    budget_estimator_tool,
    slot_selection_tool
)

st.set_page_config(page_title="Event Planner AI", page_icon="🎉", layout="centered")

st.title("🎉 Event Planner AI")
st.markdown("Plan your events professionally with AI assistance.")

# User input form
user_input = st.text_area("Enter your event request:", placeholder="E.g. plan a birthday dinner tomorrow at Bandra for 4 people")

if st.button("Plan Event") and user_input.strip():
    with st.spinner("Planning your event..."):

        # NLU extraction
        event_details = nlu_tool.invoke(user_input)
        if "error" in event_details:
            st.error("❌ Could not parse event details.")
            st.json(event_details)
        else:
            st.success("✅ Event details extracted.")
            st.json(event_details)

            # Location finding
            venues_result = location_finder_tool.invoke({
            "location": event_details["location"],
            "query_type": event_details["query_type"],
            "brand_name": event_details.get("brand_name") or ""
            })

            venues = venues_result.get("nearby_places", [])
            if venues:
                st.subheader("🏠 Available Venues")
                for venue in venues:
                    st.markdown(f"**{venue['name']}**")
                    st.caption(f"Lat: {venue['latitude']}, Lon: {venue['longitude']}")

            # Slot generation
            slots_result = slot_generator_tool.invoke({
                "start_date": event_details["start_date"],
                "end_date": event_details["end_date"],
                "duration_hours": event_details["duration_hours"]
            })
            slots = slots_result.get("feasible_slots", [])
            if slots:
                st.subheader("🗓️ Available Slots")
                for slot in slots:
                    st.markdown(f"{slot['date']} | {slot['start_time']} - {slot['end_time']}")

            # Slot selection
            selected_slot_result = slot_selection_tool.invoke({
                "event_name": event_details["event_name"],
                "feasible_slots": slots
            })
            selected_slot = selected_slot_result.get("selected_slot")
            if selected_slot:
                st.subheader("✅ Selected Slot")
                st.markdown(f"{selected_slot['date']} | {selected_slot['start_time']} - {selected_slot['end_time']}")

            # Budget estimation per venue
            st.subheader("💰 Budget Estimates")
            for venue in venues:
                budget = budget_estimator_tool.invoke({
                    "number_of_people": event_details["number_of_people"],
                    "location": venue["name"]
                })["budget_estimate"]

                st.markdown(f"**{venue['name']}**")
                st.write(f"Total: {budget['currency']}{budget['total_budget']}, Per Person: {budget['currency']}{budget['per_person_cost']}")

            st.success("🎉 Event planning completed!")

