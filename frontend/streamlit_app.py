import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.set_page_config(page_title="Ticket Analysis", page_icon="🧭", layout="centered")

st.title("Ticket Analysis with LLM")
st.caption("Enter ticket details and analyze against your service catalog definitions.")

with st.form("ticket_form"):
    description = st.text_area("Description", height=150, placeholder="Paste full ticket description...")
    short_description = st.text_input("Short Description", placeholder="One-line summary")
    submitted = st.form_submit_button("Analyze")

if submitted:
    if not description and not short_description:
        st.error("Please enter Description or Short Description.")
    else:
        with st.spinner("Analyzing..."):
            try:
                resp = requests.post(f"{API_BASE}/analyze", json={
                    "description": description,
                    "short_description": short_description
                }, timeout=60)
                if resp.status_code != 200:
                    st.error(f"Error: {resp.text}")
                else:
                    data = resp.json()
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.metric(label="Accuracy", value=f"{data.get('accuracy', 0)} %")
                    with col2:
                        st.write("")

                    st.subheader("Matched fields")
                    st.write(f"• Assignment Group: {data.get('assignment_group','')}")
                    st.write(f"• Service: {data.get('service','')}")
                    st.write(f"• Service Offering: {data.get('service_offering','')}")

                    if data.get("reasoning"):
                        st.subheader("LLM reasoning")
                        st.write(data["reasoning"])

            except Exception as e:
                st.error(f"Request failed: {e}")
