# Predictive Analytics for Resource Allocation in Disaster & NGO Operations

## Assam Flood Relief Ration Kit Forecasting

This project is an AI/ML-based disaster resource allocation system for forecasting district-wise flood relief ration-kit demand in Assam.

It combines:

- historical IMD rainfall data
- district demographic indicators
- flood-proneness indicators
- road accessibility proxy
- Prophet time-series forecasting
- Random Forest allocation modeling
- GeoPandas + Folium geospatial visualization
- Open-Meteo 7-day rainfall forecast signal

---

## Live Demo

Streamlit App:  
https://cvqfqhaxkeetvtfru7roan.streamlit.app/

---

## Problem Statement

Assam faces recurring floods that disrupt food supply, transport, housing, and healthcare access. NGOs and district authorities often face difficulty deciding where to pre-position relief supplies.

This project forecasts:

- which districts may need relief
- how many ration kits may be required
- which areas should be prioritized
- what action NGOs should take

---

## Dataset Sources

| Dataset / Data Component | Source | Usage |
|---|---|---|
| Historical monthly rainfall | IMD rainfall dataset, 1901–2015 | Climatic input |
| Assam district population | Census 2011-based district reference | Exposure estimation |
| District area | District reference data | Population density calculation |
| Flood frequency score | Flood-proneness / historical incident proxy | Vulnerability indicator |
| Road accessibility index | Terrain and accessibility proxy | Logistics difficulty indicator |
| Assam district boundaries | India district GeoJSON | GeoPandas/Folium district map |
| 7-day rainfall forecast | Open-Meteo Forecast API | Forward-looking rainfall signal |
| Relief demand target | Humanitarian planning proxy | Model target |

---

## Important Dataset Note

Public district-level NGO ration distribution records are not readily available. Therefore, the target variable `ration_kits_needed` is constructed as a proxy using humanitarian planning assumptions.

The proxy target considers:

- rainfall intensity
- flood frequency
- population exposure
- road accessibility
- monsoon effect

Assumption:

> One ration kit supports approximately one household of five people.

---

## Models Used

### 1. Prophet Forecasting Model

Prophet is used as the **primary time-series forecasting model**.

It forecasts strategic monthly relief demand trends based on historical demand patterns.

Hold-out performance:

| Metric | Value |
|---|---:|
| MAE | 302.80 |
| RMSE | 413.55 |
| MAPE | 6.20% |

This satisfies the target condition:

> Forecast MAPE below 20% on hold-out historical data.

---

### 2. Random Forest Allocation Model

Random Forest is used as the **primary district-level allocation model**.

It predicts ration-kit requirements using:

- rainfall
- rainfall lag features
- rolling rainfall features
- population
- population density
- flood frequency score
- road accessibility index
- flood severity
- district encoding
- month and quarter

Random Forest is used for operational allocation because it can ingest climatic, demographic, and vulnerability features.

---

### 3. Model Comparison

The following models were compared:

- Random Forest Regressor
- XGBoost Regressor
- LightGBM Regressor
- Prophet forecasting baseline

---

## Feature Engineering

Created features include:

- district rainfall
- rainfall lag 1, 2, and 3
- rolling 3-month rainfall
- rolling 6-month rainfall
- month number
- quarter
- monsoon flag
- flood severity score
- population density
- road accessibility index
- encoded district variable

---

## 7-Day Forward Forecasting

The system fetches or uses saved Open-Meteo 7-day rainfall forecast data for Assam district coordinates.

The workflow is:

```text
7-day rainfall forecast
+ district demographic features
+ flood-proneness indicators
+ accessibility indicators
↓
Random Forest allocation model
↓
Forward 7-day ration-kit demand
