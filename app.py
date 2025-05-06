from flask import Flask, render_template, request
import joblib
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

app = Flask(__name__)

# Load the trained model
try:
    model = joblib.load('ari_prediction_model.joblib')
except FileNotFoundError:
    print("Error: Trained model file 'ari_prediction_model.joblib' not found. Please run trained_model.py first.")
    exit()

# Load the original DataFrame (for city names and mean weather data)
try:
    original_df = pd.read_csv('laguna_allcities25_ari_weather_cases_2015_2023_final.csv')
    original_df.dropna(subset=['City', 'Year', 'Month', 'Temperature_C', 'Humidity_%', 'Rainfall_mm'], inplace=True)
except FileNotFoundError:
    print("Error: Original data file 'laguna_allcities25_ari_weather_cases_2015_2023_final.csv' not found.")
    exit()

def predict_future_ari(model, input_month, input_year, original_df):
    try:
        input_date = datetime.strptime(f"{input_month}-{input_year}", '%m-%Y')
    except ValueError:
        return [{"Month_Year": "Invalid", "Location": "-", "Risk_Level": "-", "Predicted_ARI_Type": "Invalid date format"}]

    future_predictions = []
    unique_cities = original_df['City'].unique()

    for city in unique_cities:
        city_data = original_df[original_df['City'] == city]
        if city_data.empty:
            continue

        for i in range(1, 6):
            future_date = input_date + relativedelta(months=i)
            future_data = {
                'City': [city],
                'Year': [future_date.year],
                'Month': [future_date.month],
                'Temperature_C': [city_data['Temperature_C'].mean()],
                'Humidity_%': [city_data['Humidity_%'].mean()],
                'Rainfall_mm': [city_data['Rainfall_mm'].mean()]
            }
            future_df = pd.DataFrame(future_data)
            predicted_ari = model.predict(future_df)[0]

            if predicted_ari in ['Influenza', 'Pneumonia']:
                risk_level = 'High'
            elif predicted_ari in ['Bronchitis']:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'

            future_predictions.append({
                'Month_Year': future_date.strftime('%B-%Y'),
                'Location': city,
                'Risk_Level': risk_level,
                'Predicted_ARI_Type': predicted_ari
            })

    return future_predictions

@app.route('/', methods=['GET', 'POST'])
def index():
    predictions = []

    if request.method == 'POST':
        month = request.form.get('month')
        year = request.form.get('year')

        if month and year:
            predictions = predict_future_ari(model, month, year, original_df)

    return render_template('index.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)