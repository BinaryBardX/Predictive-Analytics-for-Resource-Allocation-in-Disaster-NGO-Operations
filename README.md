# Assam Flood Relief Ration Kit Forecasting

This project predicts flood-relief ration kit demand for Assam districts using rainfall, population, flood-proneness, road accessibility, and time-series forecasting.

## Models Used

- Primary forecasting model: Prophet
- Primary allocation model: Random Forest
- Comparison models: XGBoost, LightGBM

## Dataset

The dataset combines:
- IMD subdivision-level monthly rainfall data
- Assam district population and area reference data
- Flood frequency score
- Road accessibility proxy
- Constructed humanitarian proxy target: ration_kits_needed

Due to the lack of publicly available district-level NGO relief distribution records, a proxy demand variable is constructed using humanitarian planning assumptions.

## Outputs

- final_training_dataset.csv
- ngo_resource_forecast.csv
- prophet_forecast_12_months.csv
- model.pkl
- prophet_forecasting_model.pkl
- district_encoder.pkl
- feature_columns.pkl
- model_comparison.csv
- feature_importance.csv

## Usage

Install dependencies:

pip install -r requirements.txt

Run dashboard:

streamlit run app.py