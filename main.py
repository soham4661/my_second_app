from os import name
import time
from google import genai
from dotenv import load_dotenv
import streamlit as st
import rich

load_dotenv()
client = genai.Client()
import streamlit as st

st.set_page_config(page_title="Soham's Weekend Planner", page_icon="🌤️", layout="wide")

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main app background: Deep Charcoal Grey */
.stApp {
    background: #18191C !important;
    background-attachment: fixed;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header banner */
.header-banner {
    background: linear-gradient(90deg, #FF6B6B, #FFD93D);
    padding: 28px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 28px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.4);
}
.header-banner h1 {
    color: white;
    margin: 0;
    font-size: 40px;
}
.header-banner p {
    color: #fff8f0;
    margin: 6px 0 0 0;
    font-size: 16px;
}

/* Day cards - Dark themed container */
.day-card {
    background: #232529;
    border: 1px solid #32353B;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    margin-bottom: 20px;
    color: #F0F2F5;
}

/* Sidebar - Darker Charcoal */
section[data-testid="stSidebar"] {
    background-color: #121315 !important;
}

/* Buttons */
.stButton>button {
    border-radius: 10px;
    border: none;
    background: linear-gradient(90deg, #FF6B6B, #FFD93D);
    color: white !important;
    font-weight: 600;
    padding: 8px 18px;
}
.stButton>button:hover {
    opacity: 0.9;
    color: white !important;
}
.stButton>button p {
    color: white !important;
    font-weight: 600;
}

/* Force widget labels to bright light color for high contrast */
label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] span,
.stTextInput label,
.stSelectbox label,
.stRadio label,
.stMultiSelect label,
.stNumberInput label,
.stSlider label {
    color: #E2E8F0 !important;
    font-weight: 600 !important;
    -webkit-text-fill-color: #E2E8F0 !important;
    opacity: 1 !important;
}

/* Radio button option text */
.stRadio [data-testid="stMarkdownContainer"] p,
.stRadio div[role="radiogroup"] label p {
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="header-banner">
    <h1>🌤️ Weekend Planner</h1>
    <p>Plan your perfect Saturday & Sunday ✨</p>
</div>
""", unsafe_allow_html=True)



name = st.text_input("Enter your name: ")
day_of_plan = st.selectbox("Which Day you want to plan ? ", ["Friday-night","Saturday","Sunday"])
company_type = st.radio("Select with whom you would like to spend the weekend:", ["Family", "Solo", "friends"])
type_of_activities = st.selectbox("Choose a type of activities", ["Outdoor", "Indoor", "Mixed"])


# Tracks whether the user is in "planning a trip" mode, so we know later
# whether to show the trip button or the regular weekend-plan button.
planning_a_trip = False

if type_of_activities == "Outdoor":
    activities = st.selectbox("Select outdoor activities", ["Hiking", "Cycling", "Picnic", "Beach", "Plan a trip"])
    if "Plan a trip" in activities:
        planning_a_trip = True
        location = st.text_input("Enter your destination:")
        days_trip = st.number_input("Enter the number of days for your trip:", min_value=1, max_value=30)
        budget = st.selectbox("Select your budget range:", ["Luxury", "Moderate", "Budgeted"])
        travel_type = st.radio("Select your preferred travel type:", ["Family", "Solo", "friends"])
        prompt = (f"""You are a travel planner, user is saying he wants to go to {location} for {days_trip} days, please give answer in bullet points, he is on the budget of {budget} and prefers {travel_type} travel.""")

if type_of_activities == "Indoor":
    activities = st.selectbox("Select indoor activities", ["Cooking", "Board Games", "Netflix", "Art & Craft"])
if type_of_activities == "Mixed":
    activities = st.selectbox("Select mixed activities", ["Hiking", "Cooking", "Cycling", "Board Games", "Picnic", "Movies", "Beach", "Art & Craft", "Watch latest release movies"])

# ---------- BUTTONS: only one of these shows at a time ----------
if planning_a_trip:
    if st.button("Plan the trip"):
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input= prompt
        )
        with st.spinner("Wait for it...", show_time=True):
            time.sleep(5)
        st.success("Trip plan generated successfully!")
        st.markdown(f'<p style="color: black;">{interaction.output_text}</p>', unsafe_allow_html=True)
else:
    var = ( f"""
             Please generate a weekend plan for me using these details:
            * Name: {name}
            * Day: {day_of_plan}
            * Companion: {company_type}
            * Vibe/Activities: {type_of_activities}
            * Selected activity: {activities}
                       """)


    if st.button("Give me weekend plan"):
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=var
        )
        with st.spinner("Wait for it...", show_time=True):
            time.sleep(5)
        st.success("Weekend plan generated successfully!")
        st.markdown(f'<p style="color: black;">{interaction.output_text}</p>', unsafe_allow_html=True)