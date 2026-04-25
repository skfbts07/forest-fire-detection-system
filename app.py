import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium

st.title("Forest Fire Detection Using Machine Learning")

# Load model and encoder
model = joblib.load("model.pkl")
le = joblib.load("location_encoder.pkl")

# Coordinates dictionary
forest_coords = {
    "amazon forest": [-3.4653, -62.2159],
    "araku valley": [18.33, 82.87],
    "nallamala forest": [15.34, 78.56],
    "seshachalam hills": [13.65, 79.42],
    "gir national park": [21.12, 70.79],
}

# Inputs
location_name = st.text_input("Enter Location Name (e.g., Amazon Forest)")
temperature = st.number_input("Temperature (°C)", min_value=0, max_value=60, value=30)
humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=50)
wind = st.number_input("Wind Speed (km/h)", min_value=0, max_value=100, value=10)
rainfall = st.number_input("Rainfall (mm)", min_value=0, max_value=500, value=0)

# Predict button
if st.button("Predict Fire Risk"):
    try:
        loc_encoded = le.transform([location_name])[0]
    except:
        st.error("❌ Location not recognized. Please use a known forest name.")
        st.stop()

    input_data = pd.DataFrame([{
        "Location": loc_encoded,
        "Temperature": temperature,
        "Humidity": humidity,
        "WindSpeed": wind,
        "Rainfall": rainfall
    }])

    prediction = model.predict(input_data)[0]
    confidence = max(model.predict_proba(input_data)[0])

    # Save results in session_state
    st.session_state["prediction"] = prediction
    st.session_state["confidence"] = confidence
    st.session_state["location_name"] = location_name

# Show results if available
if "prediction" in st.session_state:
    prediction = st.session_state["prediction"]
    confidence = st.session_state["confidence"]
    location_name = st.session_state["location_name"]

    if prediction == 1:
        st.error(f"🔥 Fire Detected in {location_name}! Confidence: {confidence:.2f}")
        color = "red"
    else:
        st.success(f"✅ No Fire Detected in {location_name}! Confidence: {confidence:.2f}")
        color = "green"

    # Map rendering
    loc_key = location_name.strip().lower()
    if loc_key in forest_coords:
        lat, lon = forest_coords[loc_key]
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon],
                      popup=f"{location_name} - {'Fire' if prediction==1 else 'Safe'}",
                      icon=folium.Icon(color=color)).add_to(m)
        st_folium(m, width=700, height=500)
    else:
        st.warning("⚠️ Coordinates not available in demo mode.")
