import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import requests

def generate_draft_with_perplexity(incident_data, api_key):
    prompt = f"""You are a professional customer communications specialist.
Draft a clear, concise incident message for customers based on the following info:

- Title: {incident_data.get("Title")}
- Severity: {incident_data.get("Severity")}
- Service: {incident_data.get("Owning Service")}
- State: {incident_data.get("State")}
- Time Created: {incident_data.get("Create Time")}
- Owner: {incident_data.get("Owner")}

Keep it under 300 words. Inform users of the impact and steps being taken. Include a reassurance message and status link.
"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "sonar",  # or other available models
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_token": 300
    }
    response = requests.post("https://api.perplexity.ai/chat/completions", json=body, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        st.error(f"Perplexity API Error: {response.status_code} - {response.text}")
        return None

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
    tab1, tab2, tab3 = st.tabs(["Summary and Discussion", "Customer Communication", "RCA and Postmortems"])
    
    with tab1:
        st.subheader("⚡ AI Generated Summary")
        summary = generate_mock_summary()
        st.caption("AI generated, please check for accuracy")
        
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
        st.subheader("🪄 Draft Communication")

        # Call Perplexity API to generate draft
        if "perplexity_draft" not in st.session_state:
            st.session_state.perplexity_draft = ""

        if st.button("✨ Generate Draft with Perplexity"):
            with st.spinner("Contacting Perplexity AI..."):
                api_key = st.secrets["PERPLEXITY_API_KEY"]
                generated = generate_draft_with_perplexity(incident_data, api_key)
                if generated:
                    st.session_state.perplexity_draft = generated

        # Editable text area
        st.text_area("📄 Draft Message", value=st.session_state.perplexity_draft or "", height=200)

        st.text_area("AI generated, please check for accuracy and make any necessary changes before publishing", value=st.session_state.get("perplexity_draft", ""), height=200)

            # --- Feedback Section ---
        st.markdown("### 🗣️ Feedback on Draft")

        # Initialize state
        if "feedback_vote" not in st.session_state:
            st.session_state.feedback_vote = None
        if "feedback_pending" not in st.session_state:
            st.session_state.feedback_pending = None
        if "feedback_confirmed" not in st.session_state:
            st.session_state.feedback_confirmed = False
        if "feedback_comment" not in st.session_state:
            st.session_state.feedback_comment = ""

        # Initial vote buttons
        if not st.session_state.feedback_confirmed:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Looks good"):
                    st.session_state.feedback_pending = "up"
            with col2:
                if st.button("👎 Needs improvement"):
                    st.session_state.feedback_pending = "down"

        # Confirmation step
        if st.session_state.feedback_pending and not st.session_state.feedback_confirmed:
            label = "👍 Looks good" if st.session_state.feedback_pending == "up" else "👎 Needs improvement"
            st.warning(f"Confirm your feedback: **{label}**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, confirm"):
                    st.session_state.feedback_vote = st.session_state.feedback_pending
                    st.session_state.feedback_confirmed = True
                    st.session_state.feedback_pending = None
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.feedback_pending = None
        if st.session_state.feedback_confirmed:
            st.session_state.feedback_comment = st.text_area(
                "Optional comment:",
                value=st.session_state.feedback_comment,
                placeholder="Let us know how we can improve this message...",
                height=100
            )

            if st.button("📨 Submit Feedback"):
                vote_label = "👍 Looks good" if st.session_state.feedback_vote == "up" else "👎 Needs improvement"
                st.success(f"Thanks for your feedback! You voted: {vote_label}")
                if st.session_state.feedback_comment.strip():
                    st.info(f"Comment: _{st.session_state.feedback_comment.strip()}_")

        st.markdown("### 📣 Recommended Communication Channels")

        # Simulated subscriber counts
        channel_subscribers = {
            "Slack": 42,
            "Email": 128,
            "SMS": 65
        }

        raw_channels = ["Status Page", "Slack", "Email", "SMS"]
        display_channels = [
            f"{ch} ({channel_subscribers[ch]} subs)" if ch in channel_subscribers else ch
            for ch in raw_channels
        ]

        display_to_raw = {
            f"{ch} ({channel_subscribers[ch]} subs)" if ch in channel_subscribers else ch: ch
            for ch in raw_channels
        }

        # Default selections
        default_channels = ["Status Page", "Slack"]
        default_display = [
            f"{ch} ({channel_subscribers[ch]} subs)" if ch in channel_subscribers else ch
            for ch in default_channels
        ]

        if "selected_display_channels" not in st.session_state:
            st.session_state.selected_display_channels = default_display.copy()

        selected_display = st.multiselect(
            "Choose communication channels:",
            options=display_channels,
            default=st.session_state.selected_display_channels
        )
        st.session_state.selected_display_channels = selected_display

        selected_channels = [display_to_raw[d] for d in selected_display]

        # Confirm and publish
        if st.button("🚀 Publish to Selected Channels"):
            st.session_state.confirm_publish = True

        # Confirmation step
        if st.session_state.get("confirm_publish") and not st.session_state.get("message_published"):
            with st.expander("🔒 Confirm Your Action", expanded=True):
                st.markdown("You're about to send the message to the following channels:")
                for ch in selected_channels:
                    label = f"{ch} ({channel_subscribers[ch]} subs)" if ch in channel_subscribers else ch
                    st.markdown(f"- ✅ **{label}**")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, publish now"):
                        st.session_state.message_published = True
                        #st.success(f"Message published to: {', '.join(selected_channels)}")
                with col2:
                    if st.button("❌ Cancel"):
                        st.session_state.confirm_publish = False
                        st.info("Publish canceled.")

        if st.session_state.get("message_published"):
            st.success(f"✅ Message successfully sent to: {', '.join(selected_channels)}")
    with tab3:
        st.subheader("📚 RCA and Postmortem Reports")
        st.caption("AI-generated drafts — please verify and edit before sharing.")

        service = incident_data.get("Owning Service", "[SERVICE]")
        root_cause = incident_data.get("Title", "[ROOT CAUSE]")
        created_time = incident_data.get("Create Time", "[DATE]")
        resolved_time = incident_data.get("Resolved Time", "[TIME]")

        customer_postmortem = f"""
    On {created_time}, our {service} experienced a disruption due to {root_cause}. We mitigated the issue and restored service by {resolved_time}.

    We sincerely apologize for the inconvenience and are implementing additional safeguards to prevent recurrence.
        """

        internal_postmortem = f"""

    - Date/Time of Incident: {created_time}  
    - Root Cause: {root_cause}  
    - Detection Timeline: [WHO/WHEN]  
    - Mitigation: [ACTIONS TAKEN]  
    - Impact Analysis: [USERS IMPACTED, DURATION]  
    - Lessons Learned:  
        - [1]
        - [2]
    - Next Steps: 
        - [Actionable Item 1]
        - [Owner & Timeline]
        """
        customer_draft = st.text_area("📄 Customer-Facing Report", value=customer_postmortem, height=250)
        internal_draft = st.text_area("🔒 Internal Report", value=internal_postmortem, height=300)

        # --- Communication Channel Section (only for customer-facing postmortem) ---
        st.markdown("### 📣 Publish Customer-Facing Report")

        # Simulated subscriber counts
        channel_subscribers = {
            "Slack": 42,
            "Email": 128,
            "SMS": 65
        }

        raw_channels = ["Status Page", "Slack", "Email", "SMS"]
        display_channels = [
            f"{ch} ({channel_subscribers[ch]} subs)" if ch in channel_subscribers else ch
            for ch in raw_channels
        ]
        display_to_raw = {
            f"{ch} ({channel_subscribers[ch]} subs)" if ch in channel_subscribers else ch: ch
            for ch in raw_channels
        }

        default_channels = ["Status Page", "Slack"]
        default_display = [
            f"{ch} ({channel_subscribers[ch]} subs)" if ch in channel_subscribers else ch
            for ch in default_channels
        ]

        if "rca_selected_display_channels" not in st.session_state:
            st.session_state.rca_selected_display_channels = default_display.copy()

        selected_display = st.multiselect(
            "Choose where to publish the customer-facing report:",
            options=display_channels,
            default=st.session_state.rca_selected_display_channels
        )
        st.session_state.rca_selected_display_channels = selected_display
        selected_channels = [display_to_raw[d] for d in selected_display]

        # Confirm and publish
        if st.button("🚀 Publish Customer-Facing Report"):
            st.session_state.rca_confirm_publish = True

        if st.session_state.get("rca_confirm_publish") and not st.session_state.get("rca_report_published"):
            with st.expander("🔒 Confirm Your Action", expanded=True):
                st.markdown("You're about to publish this customer-facing report to:")
                for ch in selected_channels:
                    label = f"{ch} ({channel_subscribers[ch]} subs)" if ch in channel_subscribers else ch
                    st.markdown(f"- ✅ **{label}**")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, publish now (Postmortem)"):
                        st.session_state.rca_report_published = True
                        st.success(f"Report published to: {', '.join(selected_channels)}")
                with col2:
                    if st.button("❌ Cancel (Postmortem)"):
                        st.session_state.rca_confirm_publish = False
                        st.info("Publish canceled.")

        if st.session_state.get("rca_report_published"):
            st.success(f"✅ Customer-Facing Postmortem published to: {', '.join(selected_channels)}")

        # --- Feedback Section ---
        st.markdown("### 🗣️ Feedback on Drafts")

        if "postmortem_feedback_vote" not in st.session_state:
            st.session_state.postmortem_feedback_vote = None
        if "postmortem_feedback_pending" not in st.session_state:
            st.session_state.postmortem_feedback_pending = None
        if "postmortem_feedback_confirmed" not in st.session_state:
            st.session_state.postmortem_feedback_confirmed = False
        if "postmortem_feedback_comment" not in st.session_state:
            st.session_state.postmortem_feedback_comment = ""

        if not st.session_state.postmortem_feedback_confirmed:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Looks good (Postmortem)"):
                    st.session_state.postmortem_feedback_pending = "up"
            with col2:
                if st.button("👎 Needs improvement (Postmortem)"):
                    st.session_state.postmortem_feedback_pending = "down"

        if st.session_state.postmortem_feedback_pending and not st.session_state.postmortem_feedback_confirmed:
            label = "👍 Looks good" if st.session_state.postmortem_feedback_pending == "up" else "👎 Needs improvement"
            st.warning(f"Confirm your feedback: **{label}**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, confirm (Postmortem)"):
                    st.session_state.postmortem_feedback_vote = st.session_state.postmortem_feedback_pending
                    st.session_state.postmortem_feedback_confirmed = True
                    st.session_state.postmortem_feedback_pending = None
            with col2:
                if st.button("❌ Cancel (Postmortem)"):
                    st.session_state.postmortem_feedback_pending = None

        if st.session_state.postmortem_feedback_confirmed:
            st.session_state.postmortem_feedback_comment = st.text_area(
                "Optional comment:",
                value=st.session_state.postmortem_feedback_comment,
                placeholder="Suggestions to improve the postmortem...",
                height=100
            )

            if st.button("📨 Submit Postmortem Feedback"):
                vote_label = "👍 Looks good" if st.session_state.postmortem_feedback_vote == "up" else "👎 Needs improvement"
                st.success(f"Thanks for your feedback! You voted: {vote_label}")
                if st.session_state.postmortem_feedback_comment.strip():
                    st.info(f"Comment: _{st.session_state.postmortem_feedback_comment.strip()}_")

def main():
    # Get incident data from session state
    if "incident_data" not in st.session_state:
        st.error("No incident selected. Please return to the main page.")
        if st.button("Return to Main Page"):
            st.switch_page("home.py")
        return
    
    incident_data = st.session_state.incident_data
    show_incident_detail(incident_data)
    
    # Add a button to return to main page
    if st.button("← Return to Incidents List"):
        st.switch_page("home.py")

if __name__ == "__main__":
    main() 