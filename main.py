import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Carbon Footprint Calculator", layout="centered")
st.markdown("""
    <style>
    h1 {
        text-align: center;
        color: #00C6A7;
    }
    .stNumberInput input {
        background-color: #1A1F24;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #00C6A7;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1> Carbon Footprint Calculator</h1>", unsafe_allow_html=True)
st.markdown("<h5> Estimate your yearly carbon footprint in kilograms of CO₂ equivalent (kg CO₂e).</h5>",unsafe_allow_html=True)
st.markdown("---")

#1.Transport
with st.container():
    st.subheader("Transportation")
    transport_type = st.radio(
        "Select your primary mode of transport:",
        ["Normal Vehicle (Petrol/Diesel)", "Public Transport (Bus/Train)", "Electric Vehicle"]
    )
    
    car_km = st.number_input("How many kilometers do you travel per week?", 0, 2000, 50)
    flight_hours = st.number_input("How many hours do you fly per year?", 0, 500, 0)

    emission_factors = {
        "Normal Vehicle (Petrol/Diesel)": 0.21,
        "Public Transport (Bus/Train)": 0.05,
        "Electric Vehicle": 0.06
    }
    
    car_emission = car_km * 52 * emission_factors[transport_type]
    flight_emission = flight_hours * 90  # 90 kg CO2e per flight hour

#2.Electricity
with st.container():
    st.subheader("Electricity")
    electricity_kwh = st.number_input("Electricity consumption per month (kWh)?", 0, 2000, 90)
    electricity_emission = electricity_kwh * 12 * 0.5  # 0.5 kg CO2e per kWh

#3.Diet
with st.container():
    st.subheader("Diet")
    diet = st.selectbox("What best describes your diet?", ["Heavy meat eater", "Average", "Vegetarian", "Vegan"])
    diet_factors = {
        "Heavy meat eater": 3.3,
        "Average": 2.5,
        "Vegetarian": 1.7,
        "Vegan": 1.5
    }
    diet_emission = diet_factors[diet] * 1000

#4.Waste
with st.container():
    st.subheader("Waste & Recycling")
    waste_kg = st.number_input("Household waste per week (kg)?", 0, 100, 10)
    recycle = st.radio("Do you recycle regularly?", ["Yes", "No"])
    waste_emission = waste_kg * 52 * 0.8
    if recycle == "Yes":
        waste_emission *= 0.7

#Main Result
st.markdown("---")
st.subheader("Your Carbon Footprint Summary")
total_emission = car_emission + flight_emission + electricity_emission + diet_emission + waste_emission
st.metric("Estimated Annual CO₂ Emissions", f"{total_emission:.2f} kg CO₂e")

weekly_emission = total_emission / 52
monthly_emission = total_emission / 12
yearly_emission = total_emission

col1, col2, col3 = st.columns(3)
col1.metric("Weekly CO₂ Emissions", f"{weekly_emission:.2f} kg CO₂e")
col2.metric("Monthly CO₂ Emissions", f"{monthly_emission:.2f} kg CO₂e")
col3.metric("Yearly CO₂ Emissions", f"{yearly_emission:.2f} kg CO₂e")

if yearly_emission > 5000:
    st.error("🔴 Your carbon footprint is high. Consider making eco-friendly changes.")
elif yearly_emission > 3000:
    st.warning("🟡 Moderate footprint. There’s room for improvement.")
else:
    st.success("🟢 Great job! Your carbon footprint is low compared to the average.")

#Pie Chart
st.markdown("### Emission Breakdown by Category")

categories = ["Transport", "Flights", "Electricity", "Diet", "Waste"]
values = [car_emission, flight_emission, electricity_emission, diet_emission, waste_emission]

fig = px.pie(
    names=categories,
    values=values,
    title="Proportion of Annual CO₂ Emissions",
    color_discrete_sequence=px.colors.sequential.Tealgrn
)
fig.update_traces(textinfo="percent+label")

st.plotly_chart(fig, use_container_width=True)

