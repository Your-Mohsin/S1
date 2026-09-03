import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Reading the encoders:
city_encoder = joblib.load("city_encoder.joblib")
location_encoder = joblib.load("location_encoder.joblib")

# Reading the model:
model = joblib.load("model.joblib")

# Reading the data:
df = pd.read_csv("data.csv")

# Main title of the application
st.title("House Price Prediction")

# Running command:
# python -m streamlit run app.py

data = {"Location": "JP Nagar Phase 1", "City": "Banglore"}
col1, col2 = st.columns(2)
with col1:
    # Taking area input
    area = st.number_input("Enter Area:", min_value=1, step=1, format="%d")
    if area:
        data["Area"] = area

    # Taking city input
    city = st.selectbox("Select You City: ", df.City.unique())
    if city:
        data["City"] = city

    # Taking CarParking input
    carParking = st.radio("Do You Want Car Parking:", ["Yes", "No"])
    if carParking:
        data["CarParking"] = 1 if carParking == "Yes" else 0

    # 24X7 security
    security = st.radio("Do You Want 24X7 security", ["Yes", "No"])
    if security:
        data["24X7Security"] = 1 if security == "Yes" else 0


with col2:
    # Taking bedrooms input
    bedrooms = st.number_input("Enter Number of Bed Rooms:")
    if bedrooms:
        data["No. of Bedrooms"] = bedrooms

    # Taking location input
    location = st.selectbox(
        "Select You Location: ", df[df.City == data["City"]]["Location"].unique()
    )
    if location:
        df["Location"] = location

    # Taking SwimmingPool input
    swimmingPool = st.radio("Do You want Swimming Pool:", ["Yes", "No"])
    if swimmingPool:
        data["SwimmingPool"] = 1 if swimmingPool == "Yes" else 0

    # Taking lift available input
    liftAvailable = st.radio("Do You Want Lift?", ["Yes", "No"])
    if liftAvailable:
        data["LiftAvailable"] = 1 if liftAvailable == "Yes" else 0

clubHouse = st.radio("Do You Want Club House", ["Yes", "No"])
if clubHouse:
    data["ClubHouse"] = 1 if clubHouse == "Yes" else 0

predict = st.button("Predict")
if predict:
    data2 = {
        "Area": data["Area"],
        "Location": data["Location"],
        "No. of Bedrooms": data["No. of Bedrooms"],
        "City": data["City"],
        "CarParking": data["CarParking"],
        "SwimmingPool": data["SwimmingPool"],
        "24X7Security": data["24X7Security"],
        "LiftAvailable": data["LiftAvailable"],
        "ClubHouse": data["ClubHouse"],
    }

    inputs = pd.DataFrame([data2])
    st.write(inputs)
    inputs["City"] = city_encoder.transform(inputs["City"])
    inputs["Location"] = location_encoder.transform(inputs["Location"])
    prediction = model.predict(inputs)
    st.success(f"Prediction: Rs.{round(prediction[0])}")
