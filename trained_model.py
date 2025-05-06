import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def train_and_save_model(csv_file_path, model_save_path='ari_prediction_model.joblib'):
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
        return False

    df.dropna(subset=['City', 'Year', 'Month', 'ARI_Type', 'Temperature_C', 'Humidity_%', 'Rainfall_mm'], inplace=True)

    X = df.drop('ARI_Type', axis=1)
    y = df['ARI_Type']

    categorical_features = ['City']
    numerical_features = ['Year', 'Month', 'Temperature_C', 'Humidity_%', 'Rainfall_mm']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)])

    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', LogisticRegression(solver='liblinear', multi_class='ovr', random_state=42, max_iter=1000))])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, model_output_path)
    print(f"Trained model saved to {model_save_path}")
    return True

if __name__ == '__main__':
    csv_file = 'laguna_allcities25_ari_weather_cases_2015_2023_final.csv'
    model_output_path = 'ari_prediction_model.joblib'
    train_and_save_model(csv_file, model_output_path)