# Abnormal Incidents Portal

A modern, responsive web application for tracking and managing incidents.

## Features

- Display list of incidents with key information
- Filter incidents by severity, state, and service
- Modern and responsive design
- Mock data generation for testing

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To start the application, run:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

- The main page displays a table of incidents with all required information
- Use the filters at the top to filter incidents by:
  - Severity (Critical, High, Medium, Low)
  - State (Open, In Progress, Resolved, Closed)
  - Service (User Service, Payment Service, etc.)
- The table is responsive and will adjust to your screen size 