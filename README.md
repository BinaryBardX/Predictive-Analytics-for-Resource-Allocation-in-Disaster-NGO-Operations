# Predictive Analytics for Resource Allocation in Disaster & NGO Operations

## Assam Flood Relief Ration Kit Forecasting

This project is an AI/ML-based disaster resource allocation system designed to support NGOs and district disaster-response teams in Assam. It forecasts where and how many flood-relief ration kits may be required using rainfall, demographic, flood-proneness, and accessibility indicators.

The system combines historical rainfall analysis, machine learning allocation models, time-series forecasting, geospatial visualization, and a 7-day forward rainfall forecast signal.

---

## Live Demo

Streamlit App:  
https://cvqfqhaxkeetvtfru7roan.streamlit.app/

---

## Problem Statement

Floods in Assam cause recurring displacement, food insecurity, and disruption of road connectivity. Relief organizations often respond after flood impacts are already visible, which delays supply delivery.

This project aims to predict district-wise ration-kit demand so that NGOs can pre-position supplies before flood impacts peak.

---

## Objectives

- Forecast district-wise ration-kit demand for Assam.
- Identify high-risk districts requiring urgent relief support.
- Use rainfall, population, flood vulnerability, and accessibility indicators.
- Provide an interactive dashboard for NGOs.
- Generate a 7-day forward resource forecast using rainfall forecast data.
- Visualize demand geographically using Folium maps.

---

## Models Used

### Primary Forecasting Model

**Prophet**

Used for strategic time-series forecasting of average monthly relief demand.

Hold-out performance:

| Metric | Value |
|---|---:|
| MAE | 302.80 |
| RMSE | 413.55 |
| MAPE | 6.20% |

This satisfies the target condition of forecast MAPE below 20%.

### Primary Allocation Model

**Random Forest Regressor**

Used for district-level ration-kit allocation based on climatic, demographic, vulnerability, and accessibility features.

### Comparison Models

- Random Forest Regressor
- XGBoost Regressor
- LightGBM Regressor

---

## Dataset Description

The project uses a combined district-month dataset created from:

- IMD historical rainfall data
- Assam district population and area indicators
- Flood-frequency vulnerability score
- Road accessibility proxy
- District-level rainfall adjustment factors
- Open-Meteo 7-day rainfall forecast data

Due to the lack of publicly available district-level NGO relief distribution records, the target variable `ration_kits_needed` is constructed using humanitarian planning assumptions.

---

## Target Variable Strategy

The target variable estimates ration-kit demand using:

- rainfall intensity
- flood-proneness
- population exposure
- road accessibility
- monsoon season effect

Assumption:

> One ration kit supports approximately one household of five people.

This target is a planning proxy, not an official NGO distribution record.

---

## Feature Engineering

The following features were created:

- district rainfall
- rainfall lag features
- rolling 3-month rainfall
- rolling 6-month rainfall
- flood severity score
- monsoon flag
- population density
- road accessibility index
- flood frequency score
- encoded district variable
- month and quarter features

---

## Forward 7-Day Forecasting

The dashboard includes a forward-looking rainfall signal.

Open-Meteo API is used to fetch 7-day rainfall forecast data for Assam district coordinates. This forecast rainfall is then converted into the same feature structure used by the Random Forest allocation model.

The model predicts:

- 7-day ration-kit demand
- district risk level
- recommended NGO action

---

## Dashboard Features

The Streamlit dashboard includes:

- district selector
- 7-day rainfall forecast display
- predicted ration-kit demand
- risk-level classification
- district-wise forward forecast table
- Prophet 12-month strategic forecast
- Random Forest feature importance
- model comparison table
- interactive Assam district map
- NGO action recommendations

---

## Geospatial Analysis

GeoPandas and Folium are used to create an Assam district-level risk map.

The map visualizes:

- predicted ration-kit demand
- risk level
- rainfall
- flood severity
- district-wise relief priority

---

## NGO Operational Playbook

### Low Risk

- Continue rainfall monitoring.
- Maintain basic buffer stock.
- No immediate mobilization required.

### Medium Risk

- Pre-position ration kits at block-level storage points.
- Alert local volunteer networks.
- Monitor rainfall and road accessibility.

### High Risk

- Mobilize district-level relief teams.
- Arrange transport and warehouse space.
- Prepare ration kits for rapid deployment.

### Severe Risk

- Immediate pre-positioning required.
- Coordinate with district administration.
- Activate multi-agency emergency response.
- Prioritize vulnerable and low-accessibility areas.

---

## Project Structure

```text
.
├── app.py
├── README.md
├── requirements.txt
├── ngo_resource_forecast.csv
├── forward_7day_resource_forecast.csv
├── real_7day_rainfall_forecast.csv
├── prophet_forecast_12_months.csv
├── feature_importance.csv
├── model_comparison.csv
├── assam_district_risk_map.html
