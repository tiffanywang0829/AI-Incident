import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_mock_summary():
    what_we_know = [
        "Service degradation detected in the Payment Service API",
        "Error rate increased by 15% in the last hour",
        "Affecting approximately 5% of all payment transactions",
        "Primary error: Timeout in payment gateway communication"
    ]
    
    what_has_been_done = [
        "Initial investigation completed by the Payment Service team",
        "Identified the root cause as increased latency in the payment gateway",
        "Implemented temporary rate limiting to prevent cascading failures",
        "Deployed hotfix to improve error handling and retry logic"
    ]
    
    customer_communication = [
        "Initial notification sent to affected customers",
        "Regular updates provided every 30 minutes",
        "Estimated resolution time communicated: 2 hours",
        "Alternative payment methods suggested to customers"
    ]
    
    return {
        "what_we_know": what_we_know,
        "what_has_been_done": what_has_been_done,
        "customer_communication": customer_communication
    }

def generate_communication_draft(incident_data):
    severity = incident_data["Severity"]
    service = incident_data["Owning Service"]
    title = incident_data["Title"]
    
    draft = f"""
Dear valued customers,

We are currently experiencing {severity.lower()} issues with our {service.lower()}. {title}

Our team is actively working on resolving this issue. We will provide updates every 30 minutes until the situation is resolved.

You could check the status of the incident on our status page: https://status.abnormal.ai and subscribe for notifications.

We apologize for any inconvenience this may cause and appreciate your patience.

Best regards,
Abnormal AI Incident Response Team
    """
    return draft

def show_incident_detail(incident_data):
    st.title("🚨 Incident Details")
    
    # Essential Section
    st.header("Essential Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Incident ID", incident_data["Incident ID"])
        st.metric("Severity", incident_data["Severity"])
        st.metric("State", incident_data["State"])
        st.metric("Type", incident_data["Type"])
    
    with col2:
        st.metric("Owning Service", incident_data["Owning Service"])
        st.metric("Owner", incident_data["Owner"])
        st.metric("Create Time", incident_data["Create Time"])
    
    # Tabs
    tab1, tab2 = st.tabs(["Summary and Discussion", "Customer Communication"])
    
    with tab1:
        st.subheader("AI Generated Summary")
        
        summary = generate_mock_summary()
        
        # What We Know
        st.markdown("### What We Know")
        for item in summary["what_we_know"]:
            st.markdown(f"- {item}")
        
        # What Has Been Done
        st.markdown("### What Has Been Done")
        for item in summary["what_has_been_done"]:
            st.markdown(f"- {item}")
        
        # Customer Communication
        st.markdown("### What Has Been Communicated to the customer")
        for item in summary["customer_communication"]:
            st.markdown(f"- {item}")
    
    with tab2:
        st.subheader("Draft Communication")
        
        # Generate and display draft
        draft = generate_communication_draft(incident_data)
        st.text_area("Draft Message", draft, height=200)
        
        # Review and publish buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Review Draft"):
                st.success("Draft reviewed and approved!")
        with col2:
            if st.button("Publish to Customers"):
                st.success("Message published to customers!")

def main():
    # Get incident data from session state
    if "incident_data" not in st.session_state:
        st.error("No incident selected. Please return to the main page.")
        if st.button("Return to Main Page"):
            st.switch_page("Home.py")
        return
    
    incident_data = st.session_state.incident_data
    show_incident_detail(incident_data)
    
    # Add a button to return to main page
    if st.button("← Return to Incidents List"):
        st.switch_page("Home.py")

if __name__ == "__main__":
    main() 