import streamlit as st
from tools.agent_tools import (
    nlu_tool,
    slot_generator_tool,
    location_finder_tool,
    budget_estimator_tool,
    slot_selection_tool,
)
from fpdf import FPDF
import folium
from streamlit_folium import st_folium
from langchain_groq import ChatGroq

st.set_page_config(page_title="Event Planner AI", page_icon="🎉")

chatgroq_client = ChatGroq(model="llama3-70b-8192")

def chatgroq_conversation(user_input, history=[]):
    messages = [{"role": "system", "content": "You are an event planning assistant."}]
    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})
    messages.append({"role": "user", "content": user_input})
    response = chatgroq_client.invoke(messages)
    return response.content

def create_pdf(plan_text, filename="event_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in plan_text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=1)
    pdf.output(filename)
    return filename

st.title("Your Event Planner AI")
st.write("Plan your events professionally with AI assistance.")

user_input = st.text_input("Enter your event request:")

if user_input:
    event_details = nlu_tool.invoke({"user_input": user_input})
    st.success("✅ Event details extracted.")
    st.json(event_details)

    # Location finder
    venues_result = location_finder_tool.invoke({
        "location": event_details["location"],
        "query_type": event_details["query_type"],
        "brand_name": event_details.get("brand_name") or ""
    })
    venues = venues_result.get("nearby_places", [])

    if venues:
        st.subheader("🏠 Available Venues")
        cols = st.columns(len(venues))
        for idx, place in enumerate(venues):
            with cols[idx]:
                st.markdown(f"""
                **{place['name']}**

                _{place.get('address', 'Address not available')}_

                **Lat:** {place['latitude']}  
                **Lon:** {place['longitude']}
                """)

        st.subheader("🗺️ Venue Locations Map")
        m = folium.Map(location=[float(venues[0]['latitude']), float(venues[0]['longitude'])], zoom_start=14)
        for place in venues:
            folium.Marker(
                [float(place['latitude']), float(place['longitude'])],
                popup=place['name'],
            ).add_to(m)
        st_folium(m, width=700, height=500)

    slots_result = slot_generator_tool.invoke({
        "start_date": event_details["start_date"],
        "end_date": event_details["end_date"],
        "duration_hours": event_details["duration_hours"]
    })
    slots = slots_result.get("feasible_slots", [])
    if slots:
        st.subheader("🗓️ Available Slots")
        for slot in slots:
            st.write(f"{slot['date']} | {slot['start_time']} - {slot['end_time']}")

    selected_slot_result = slot_selection_tool.invoke({
        "event_name": event_details["event_name"],
        "feasible_slots": slots
    })
    selected_slot = selected_slot_result.get("selected_slot")
    if selected_slot:
        st.success(f"✅ Selected Slot: {selected_slot['date']} | {selected_slot['start_time']} - {selected_slot['end_time']}")

    st.subheader("💰 Budget Estimates")
    for place in venues:
        estimate = budget_estimator_tool.invoke({
            "number_of_people": event_details["number_of_people"],
            "location": place["name"]
        })
        budget = estimate["budget_estimate"]
        st.markdown(f"""
        **{place['name']}, {place.get('address')}**

        Total: {budget['currency']}{budget['total_budget']}, Per Person: {budget['currency']}{budget['per_person_cost']}
        """)

    final_plan = f"""
Event: {event_details['event_name'].title()}
Date: {selected_slot['date']}
Time: {selected_slot['start_time']} to {selected_slot['end_time']}
Guests: {event_details['number_of_people']}
Venue Options:
"""
    for place in venues:
        final_plan += f"- {place['name']} ({place.get('address', 'Address not available')})\n"

    st.subheader("📄 Final Plan Summary")
    st.text(final_plan)

    if st.button("📥 Download Plan as PDF"):
        pdf_file = create_pdf(final_plan)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name=pdf_file, mime="application/pdf")

st.divider()
st.subheader("💬 Chat with Event Planner AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_q = st.text_input("Ask follow-up question:")

if user_q:
    answer = chatgroq_conversation(user_q, st.session_state.chat_history)
    st.session_state.chat_history.append({"user": user_q, "assistant": answer})
    st.write(answer)
