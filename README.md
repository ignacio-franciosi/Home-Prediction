# California Home Price Prediction

This project predicts median house values in California districts using a trained XGBoost regression model. The notebook tested three models: Linear Regression, Random Forest Regressor, and XGBoost. XGBoost performed best and was selected as the final model used by the app. The app includes a small FastAPI backend and a clean web frontend for interactive predictions.

## Project Structure

- `app.py`: FastAPI application that loads the model and serves predictions.
- `templates/index.html`: Main frontend page.
- `static/`: CSS and JavaScript assets.
- `xgboost_model.pkl`: Serialized trained model used by the API.
- `HomePrediction.ipynb`: Notebook used to explore the dataset and train the model.
- `housing.csv`: Dataset used for the notebook workflow.

## Requirements

- Python 3.12 or compatible Python 3 version
- `pip`

## Setup

Create and activate the virtual environment, then install the dependencies:

```powershell
& ".venv/Scripts/Activate.ps1"
python -m pip install -r requirements.txt
```

If you do not have the virtual environment yet, create it first:

```powershell
python -m venv .venv
& ".venv/Scripts/Activate.ps1"
python -m pip install -r requirements.txt
```

## Run the Project

Start the backend and frontend with Uvicorn:

```powershell
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open the app in your browser:

```text
http://127.0.0.1:8000
```

## API Endpoints

- `GET /` serves the frontend.
- `GET /health` checks that the API is running.
- `POST /api/predict` returns a house price prediction.
- `GET /api/schema` returns the input schema for the prediction form.

## Example Prediction Request

```powershell
curl -X POST "http://127.0.0.1:8000/api/predict" -H "Content-Type: application/json" -d @'
{
  "longitude": -122.23,
  "latitude": 37.88,
  "housing_median_age": 41,
  "total_rooms": 880,
  "total_bedrooms": 129,
  "population": 322,
  "households": 126,
  "median_income": 8.3252,
  "ocean_proximity": "NEAR BAY"
}
'@
```

## Notes

- The backend automatically loads `xgboost_model.pkl` from the project root.
- The API computes derived features internally, so the frontend only needs the original dataset fields.
- Keep the model file in the repository if you want the app to run immediately after cloning.