from __future__ import annotations

from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH_CANDIDATES = [BASE_DIR / "xgboost.pkl", BASE_DIR / "xgboost_model.pkl"]

MODEL_PATH = next((path for path in MODEL_PATH_CANDIDATES if path.exists()), None)
if MODEL_PATH is None:
    raise FileNotFoundError("xgboost.pkl or xgboost_model.pkl not found in the project root.")

model = joblib.load(MODEL_PATH)

app = FastAPI(title="Home Price API", version="1.0.0")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class PredictionInput(BaseModel):
    longitude: float = Field(..., description="District longitude")
    latitude: float = Field(..., description="District latitude")
    housing_median_age: float = Field(..., ge=0, description="Median age of housing in the district")
    total_rooms: float = Field(..., gt=0, description="Total number of rooms")
    total_bedrooms: float = Field(..., ge=0, description="Total number of bedrooms")
    population: float = Field(..., ge=0, description="Population of the district")
    households: float = Field(..., gt=0, description="Number of households")
    median_income: float = Field(..., ge=0, description="Median household income")
    ocean_proximity: str = Field(..., description="Relative location to the ocean (categorical)")


def build_model_frame(payload: PredictionInput) -> list[list[float]]:
    if payload.latitude == 0:
        raise HTTPException(status_code=400, detail="latitude cannot be 0 because coords is calculated as longitude / latitude.")

    bedrooms_per_room = payload.total_bedrooms / payload.total_rooms
    population_per_household = payload.population / payload.households
    coords = payload.longitude / payload.latitude

    ocean_value = payload.ocean_proximity.strip().upper()
    ocean_features = {
        "ocean_proximity__1h_ocean": 1.0 if ocean_value == "<1H OCEAN" else 0.0,
        "ocean_proximity_inland": 1.0 if ocean_value == "INLAND" else 0.0,
        "ocean_proximity_island": 1.0 if ocean_value == "ISLAND" else 0.0,
        "ocean_proximity_near_bay": 1.0 if ocean_value == "NEAR BAY" else 0.0,
        "ocean_proximity_near_ocean": 1.0 if ocean_value == "NEAR OCEAN" else 0.0,
    }

    feature_row = {
        "housing_median_age": payload.housing_median_age,
        "median_income": payload.median_income,
        "bedrooms_per_room": bedrooms_per_room,
        "population_per_household": population_per_household,
        "coords": coords,
        **ocean_features,
    }

    expected_columns = list(getattr(model, "feature_names_in_", feature_row.keys()))
    return [[feature_row[column] for column in expected_columns]]


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "model_name": type(model).__name__,
            "model_path": MODEL_PATH.name,
        },
    )


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "model": MODEL_PATH.name})


@app.post("/api/predict")
def predict(payload: PredictionInput) -> JSONResponse:
    try:
        features = build_model_frame(payload)
        prediction = float(model.predict(features)[0])
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive guard for runtime issues
        raise HTTPException(status_code=500, detail=f"Failed to generate prediction: {exc}") from exc

    return JSONResponse(
        {
            "prediction": round(prediction, 2),
            "prediction_formatted": f"${prediction:,.2f}",
            "input": payload.model_dump(),
        }
    )


@app.get("/api/schema")
def schema() -> JSONResponse:
    return JSONResponse(PredictionInput.model_json_schema())