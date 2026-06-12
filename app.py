
import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Assam Flood Relief Forecasting",
    layout="wide"
)

st.title("🌊 Assam Flood Relief Ration Kit Forecasting Dashboard")

st.markdown("""
This dashboard supports NGO and disaster-response planning by estimating district-wise ration-kit demand.
Primary forecasting model: **Prophet**  
Primary allocation model: **Random Forest**
""")

# Load data
forecast = pd.read_csv("ngo_resource_forecast.csv")
prophet_forecast = pd.read_csv("prophet_forecast_12_months.csv")
feature_importance = pd.read_csv("feature_importance.csv")
model_comparison = pd.read_csv("model_comparison.csv")

# Sidebar
st.sidebar.header("District Prediction Input")

district = st.sidebar.selectbox(
    "Select District",
    sorted(forecast["district"].unique())
)

district_row = forecast[forecast["district"] == district].iloc[0]

rainfall = st.sidebar.slider(
    "Rainfall (mm)",
    min_value=0.0,
    max_value=600.0,
    value=float(district_row["district_rainfall"]),
    step=1.0
)

flood_severity = st.sidebar.slider(
    "Flood Severity Score",
    min_value=0.0,
    max_value=10.0,
    value=float(district_row["flood_severity"]),
    step=0.1
)

predicted_kits = int(district_row["predicted_ration_kits"])

def classify_risk(kits):
    if kits < 2000:
        return "Low"
    elif kits < 5000:
        return "Medium"
    elif kits < 8000:
        return "High"
    else:
        return "Severe"

risk = classify_risk(predicted_kits)

# Main KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Selected District", district)
col2.metric("Predicted Ration Kits", f"{predicted_kits:,}")
col3.metric("Risk Level", risk)
col4.metric("Flood Severity", f"{flood_severity:.2f}")

st.divider()

# Tables and charts
left, right = st.columns(2)

with left:
    st.subheader("Top Districts by Predicted Demand")
    top10 = forecast.sort_values(
        "predicted_ration_kits",
        ascending=False
    ).head(10)

    st.bar_chart(
        top10.set_index("district")["predicted_ration_kits"]
    )

with right:
    st.subheader("Model Comparison")
    st.dataframe(model_comparison, use_container_width=True)

st.divider()

colA, colB = st.columns(2)

with colA:
    st.subheader("Prophet 12-Month Forecast")
    prophet_forecast["ds"] = pd.to_datetime(prophet_forecast["ds"])
    prophet_plot = prophet_forecast.set_index("ds")[["yhat", "yhat_lower", "yhat_upper"]]
    st.line_chart(prophet_plot)

with colB:
    st.subheader("Feature Importance")
    st.bar_chart(
        feature_importance.set_index("Feature")["Importance"]
    )

st.divider()

st.subheader("Interactive Assam District Risk Map")

try:
    with open("assam_district_risk_map.html", "r", encoding="utf-8") as f:
        html_map = f.read()
    st.components.v1.html(html_map, height=600)
except:
    st.warning("Map file not found. Please ensure assam_district_risk_map.html is in the same folder as app.py.")

st.divider()

st.subheader("NGO Operational Recommendation")

if risk == "Low":
    st.success("Low demand: Maintain monitoring and keep basic buffer stock ready.")
elif risk == "Medium":
    st.warning("Medium demand: Pre-position supplies at block-level storage points.")
elif risk == "High":
    st.error("High demand: Mobilize transport, volunteers, and district-level relief teams.")
else:
    st.error("Severe demand: Immediate pre-positioning, emergency coordination, and multi-agency response recommended.")

st.dataframe(
    forecast.sort_values("predicted_ration_kits", ascending=False),
    use_container_width=True
)
