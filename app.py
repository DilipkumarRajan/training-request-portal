import streamlit as st
import gspread
from datetime import date, timedelta
from google.oauth2.service_account import Credentials

# --------------------
# Google Sheets Setup
# --------------------
# Replace with your sheet name
SHEET_NAME = "Customer Training Requests"

# Path to your downloaded JSON key
SERVICE_ACCOUNT_FILE = "credentials.json"

# Define the scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open(SHEET_NAME).sheet1

# --------------------
# UI Styling and Branding
# --------------------
st.set_page_config(page_title="SupportLogic Training Request", layout="centered")


st.markdown("""
    <div style="background-color: #4A4DDE; padding: 20px; border-radius: 10px; text-align: center;">
        <img src="https://www.supportlogic.io/wp-content/uploads/2023/03/SupportLogic_logo.svg" alt="SupportLogic" width="200">
        <h1 style="color: #1f2937; margin-top: 10px;">Customer Training Request Portal</h1>
    </div>
""", unsafe_allow_html=True)

st.write("Use this form to schedule training for a customer during onboarding.")

# --------------------
# Training Request Form
# --------------------
with st.form("training_request_form"):
    customer_name = st.text_input("Customer Name", "")
    email = st.text_input("Your Email", "")
    go_live_date = st.date_input("Customer Go-Live Date", min_value=date.today())

    trainings = st.multiselect("Training Required", [
        "SupportLogic Core", "Administrator Training", "Analytics Training"
    ])

    num_users = st.number_input("Number of Users Attending", min_value=1)

    package = st.selectbox("Package Purchased", ["CoreSX Standard", "Expand standard", "Elevate", "Assist"])

    custom_training = st.radio("Need Customized Training?", ["No", "Yes"])

    # Set min training lead time
    lead_days = 14 if custom_training == "Yes" else 7
    min_pref_date = date.today() + timedelta(days=lead_days)
    preferred_date = st.date_input("Preferred Training Date", value=min_pref_date, min_value=min_pref_date)

    # Show text box only if custom training selected
    custom_details = ""
    if custom_training == "Yes":
        custom_details = st.text_area("Customization Details (please specify)")

    confirm = st.checkbox("I confirm this request is based on a real customer schedule.")

    submitted = st.form_submit_button("Submit Request")

# --------------------
# Submission Handling
# --------------------
if submitted:
    if not confirm:
        st.error("Please confirm before submitting.")
    elif not trainings:
        st.error("Please select at least one training topic.")
    else:
        sheet.append_row([
            customer_name,
            email,
            go_live_date.isoformat(),
            ", ".join(trainings),
            int(num_users),
            package,
            preferred_date.isoformat(),
            custom_training,
            custom_details,
            "Yes",  # Confirmed
            date.today().isoformat()
        ])
        st.success("✅ Your training request has been submitted successfully.")
