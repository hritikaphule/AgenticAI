import streamlit as st
from backend.calendar import create_event
from models.scheduler_agent import generate_schedule
import json
import re

# ---- TEMPORARY TEST DATA ----
free_slots = [
  {"date": "2025-06-10", "start": "10:00", "end": "12:00"},
  {"date": "2025-06-10", "start": "14:00", "end": "18:00"},
]

todoist_tasks = [
  {"task": "Finish report", "priority": 4, "due": "2025-06-11", "duration": 2},
  {"task": "Doctor appointment", "priority": 3, "due": None, "duration": 1},
]

# ---- STREAMLIT UI ----

st.set_page_config(page_title="Agentic AI Auto Scheduler", page_icon="🧠", layout="centered")

st.title("🧠 Agentic AI Auto Scheduler")
st.write("Easily auto-schedule your tasks using LLaMA powered agent!")

with st.expander("📅 View input data (free slots & tasks)", expanded=False):
    st.subheader("Available Free Slots")
    for slot in free_slots:
        st.write(f"{slot['date']} — {slot['start']} to {slot['end']}")

    st.subheader("Todoist Tasks")
    for task in todoist_tasks:
        st.write(f"Task: {task['task']} | Priority: {task['priority']} | Due: {task['due']} | Duration: {task['duration']}h")

st.divider()

if st.button("🚀 Generate AI Schedule", use_container_width=True):
    with st.spinner("🤖 Generating schedule via LLaMA..."):

        schedule = generate_schedule(free_slots, todoist_tasks)
        st.success("✅ Schedule generated successfully!")

        st.subheader("📝 LLaMA Agent Output:")
        st.code(schedule, language="json")

        json_match = re.search(r'\[\s*\{.*?\}\s*\]', schedule, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
            try:
                schedule_list = json.loads(json_text)

                st.subheader("📊 Final Scheduled Tasks:")
                for item in schedule_list:
                    with st.container(border=True):
                        st.write(f"📅 **Date:** {item['date']}")
                        st.write(f"🕒 **Time:** {item['time']}")
                        st.write(f"📝 **Task:** {item['task']}")

                # Push to Google Calendar
                for item in schedule_list:
                    create_event(item['date'], item['time'], item['task'])

                st.success("🎯 Events successfully created in Google Calendar!")

            except Exception as e:
                st.error(f"❌ Error parsing extracted JSON: {e}")
        else:
            st.error("❌ Could not extract valid JSON from agent response.")
