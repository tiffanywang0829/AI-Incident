import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="Abnormal Incidents Portal",
    page_icon="🚨",
    layout="wide"
)

# Custom CSS for modern look
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stDataFrame {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        margin-top: 1.5rem;
    }
    h1 {
        color: #1E3A8A;
        margin-bottom: 2rem;
    }
    .column-header {
        font-weight: 600;
        color: #1E3A8A;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 0.5rem 0;
    }
    .header-container {
        border-bottom: 2px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Generate mock data
def generate_mock_incidents(num_incidents=50):
    services = ["User Service", "Payment Service", "Auth Service", "Notification Service", "API Gateway"]
    states = ["Open", "In Progress", "Resolved", "Closed"]
    severities = ["Critical", "High", "Medium", "Low"]
    owners = ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Williams", "Alex Brown"]
    incident_types = ["External", "Internal"]
    
    incidents = []
    base_time = datetime.now()
    
    for i in range(num_incidents):
        incident_time = base_time - timedelta(hours=random.randint(1, 72))
        incidents.append({
            "Type": random.choice(incident_types),
            "Incident ID": f"INC-{random.randint(1000, 9999)}",
            "Severity": random.choice(severities),
            "State": random.choice(states),
            "Title": f"Service degradation in {random.choice(services)}",
            "Create Time": incident_time.strftime("%Y-%m-%d %H:%M"),
            "Owning Service": random.choice(services),
            "Owner": random.choice(owners)
        })
    
    return pd.DataFrame(incidents)

def handle_incident_click(incident_data):
    st.session_state.incident_data = incident_data
    st.switch_page("pages/1_Incident_Detail.py")

# Main app
def main():
    st.title("🚨 Abnormal Incidents Portal")
    
    # Add filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        severity_filter = st.multiselect(
            "Filter by Severity",
            ["Critical", "High", "Medium", "Low"],
            default=[]
        )
    
    with col2:
        state_filter = st.multiselect(
            "Filter by State",
            ["Open", "In Progress", "Resolved", "Closed"],
            default=[]
        )
    
    with col3:
        service_filter = st.multiselect(
            "Filter by Service",
            ["User Service", "Payment Service", "Auth Service", "Notification Service", "API Gateway"],
            default=[]
        )
        
    with col4:
        type_filter = st.multiselect(
            "Filter by Type",
            ["External", "Internal"],
            default=[]
        )
    
    # Generate and filter data
    df = generate_mock_incidents()
    
    # Apply filters
    if severity_filter:
        df = df[df["Severity"].isin(severity_filter)]
    if state_filter:
        df = df[df["State"].isin(state_filter)]
    if service_filter:
        df = df[df["Owning Service"].isin(service_filter)]
    if type_filter:
        df = df[df["Type"].isin(type_filter)]
    
    # Pagination
    items_per_page = 10
    total_pages = len(df) // items_per_page + (1 if len(df) % items_per_page > 0 else 0)
    
    # Add page navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        page = st.selectbox(
            "Page",
            range(1, total_pages + 1),
            format_func=lambda x: f"Page {x} of {total_pages}"
        )
    
    # Calculate start and end indices for the current page
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(df))
    
    # Display column headers
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    header_cols = st.columns([1, 1, 1, 1, 2, 1, 1, 1, 1])
    with header_cols[0]:
        st.markdown('<div class="column-header">Type</div>', unsafe_allow_html=True)
    with header_cols[1]:
        st.markdown('<div class="column-header">Incident ID</div>', unsafe_allow_html=True)
    with header_cols[2]:
        st.markdown('<div class="column-header">Severity</div>', unsafe_allow_html=True)
    with header_cols[3]:
        st.markdown('<div class="column-header">State</div>', unsafe_allow_html=True)
    with header_cols[4]:
        st.markdown('<div class="column-header">Title</div>', unsafe_allow_html=True)
    with header_cols[5]:
        st.markdown('<div class="column-header">Create Time</div>', unsafe_allow_html=True)
    with header_cols[6]:
        st.markdown('<div class="column-header">Owning Service</div>', unsafe_allow_html=True)
    with header_cols[7]:
        st.markdown('<div class="column-header">Owner</div>', unsafe_allow_html=True)
    with header_cols[8]:
        st.markdown('<div class="column-header">Actions</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display incidents with clickable rows
    for idx, row in df.iloc[start_idx:end_idx].iterrows():
        with st.container():
            cols = st.columns([1, 1, 1, 1, 2, 1, 1, 1, 1])  # Added one more column for the button
            with cols[0]:
                st.write(row["Type"])
            with cols[1]:
                st.write(row["Incident ID"])
            with cols[2]:
                st.write(row["Severity"])
            with cols[3]:
                st.write(row["State"])
            with cols[4]:
                st.write(row["Title"])
            with cols[5]:
                st.write(row["Create Time"])
            with cols[6]:
                st.write(row["Owning Service"])
            with cols[7]:
                st.write(row["Owner"])
            with cols[8]:
    # Escalation logic (can be customized)
                is_escalation_prone = (
                    row["Severity"] in ["Critical", "High"] and
                    row["State"] in ["Open", "In Progress"]
                )

                # Layout: Icon + View Details button side by side
                icon_col, btn_col = st.columns([1, 4])
                
                with icon_col:
                    if is_escalation_prone:
                        st.markdown("🚩", unsafe_allow_html=True)
                    else:
                        st.markdown("")  # Empty space for alignment

                with btn_col:
                    if st.button("View Details", key=f"btn_{idx}"):
                        handle_incident_click(row.to_dict())

            
            st.divider()
    
    # Display total number of incidents
    st.caption(f"Showing {start_idx + 1}-{end_idx} of {len(df)} incidents")

if __name__ == "__main__":
    main()