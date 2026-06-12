
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Assam Flood Relief Forecasting",
    layout="wide"
)

st.title("🌊 Assam Flood Relief Resource Forecasting Dashboard")

st.markdown("""
This dashboard estimates district-wise ration-kit demand for Assam flood response.

**Primary forecasting model:** Prophet  
**Primary allocation model:** Random Forest  
**Forward signal:** Real 7-day rainfall forecast from Open-Meteo API output saved as CSV
""")

@st.cache_data
def load_data():
    base = pd.read_csv("ngo_resource_forecast.csv")
    forward = pd.read_csv("forward_7day_resource_forecast.csv")
    rain = pd.read_csv("real_7day_rainfall_forecast.csv")
    prophet = pd.read_csv("prophet_forecast_12_months.csv")
    importance = pd.read_csv("feature_importance.csv")
    comparison = pd.read_csv("model_comparison.csv")
    return base, forward, rain, prophet, importance, comparison

base, forward, rain, prophet, importance, comparison = load_data()

st.sidebar.header("District Planner")

district = st.sidebar.selectbox(
    "Select District",
    sorted(forward["district"].unique())
)

row = forward[forward["district"] == district].iloc[0]

st.subheader("7-Day Forward Resource Forecast")

c1, c2, c3, c4 = st.columns(4)

c1.metric("District", district)
c2.metric("7-Day Forecast Rainfall", f"{row['forecast_7day_rainfall_mm']:.1f} mm")
c3.metric("Base Allocation", f"{int(row['predicted_ration_kits']):,} kits")
c4.metric("7-Day Adjusted Demand", f"{int(row['forward_7day_ration_kits']):,} kits")

risk = row["forward_7day_risk"]

if risk == "Low":
    st.success(row["recommended_action"])
elif risk == "Medium":
    st.warning(row["recommended_action"])
else:
    st.error(row["recommended_action"])

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Top Districts by 7-Day Forward Demand")
    top10 = forward.sort_values("forward_7day_ration_kits", ascending=False).head(10)
    st.bar_chart(top10.set_index("district")["forward_7day_ration_kits"])

with right:
    st.subheader("Model Comparison")
    st.dataframe(comparison, use_container_width=True)

st.divider()

st.subheader("District-wise 7-Day Forecast Table")
st.dataframe(
    forward[[
        "district",
        "forecast_7day_rainfall_mm",
        "predicted_ration_kits",
        "forward_7day_ration_kits",
        "forward_7day_risk",
        "recommended_action"
    ]],
    use_container_width=True
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Prophet 12-Month Strategic Forecast")
    prophet["ds"] = pd.to_datetime(prophet["ds"])
    st.line_chart(prophet.set_index("ds")[["yhat", "yhat_lower", "yhat_upper"]])

with col2:
    st.subheader("Random Forest Feature Importance")
    st.bar_chart(importance.set_index("Feature")["Importance"])

st.divider()

st.subheader("Interactive Assam District Map")

try:
    with open("assam_district_risk_map.html", "r", encoding="utf-8") as f:
        html_map = f.read()
    st.components.v1.html(html_map, height=650)
except Exception as e:
    st.warning("Map file not found.")
    st.write(e)

with st.expander("Methodology"):
    st.markdown("""
The system combines historical IMD rainfall, district demographics, flood-frequency indicators,
road accessibility, Prophet forecasting, and Random Forest allocation modeling.

For forward-looking planning, a 7-day rainfall forecast is fetched for each district coordinate
and used to adjust base allocation demand. The dashboard supports pre-positioning decisions
for NGOs and district disaster response teams.
""")
