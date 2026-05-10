# California Home Price Prediction 🏠

This project applies Machine Learning techniques to predict median house values in California districts based on 1990 Census data. The primary objective is to build a regression model capable of estimating property prices using various demographic and geographical features.

## 📋 Project Overview

The notebook follows a comprehensive data science workflow, including:
- **Exploratory Data Analysis (EDA):** Identifying patterns and correlations.
- **Data Cleaning:** Handling missing values using advanced techniques.
- **Feature Engineering:** Preprocessing categorical variables and scaling.
- **Model Evaluation:** Training regression models to predict continuous values.

## 📊 Dataset

The dataset contains information on over 20,000 districts. Key features include:

- **Features:**
  - `longitude` / `latitude`: Geographic location.
  - `housing_median_age`: Median age of houses in the district.
  - `total_rooms` / `total_bedrooms`: Room counts.
  - `population` / `households`: Demographic density.
  - `median_income`: Median income for households (highly correlated with price).
  - `ocean_proximity`: Categorical location relative to the coast.

- **Target:**
  - `median_house_value`: The median house value for households within a block.

## 🛠️ Tech Stack

- **Python 3**
- **Pandas & NumPy:** For data manipulation and numerical analysis.
- **Scikit-Learn:** Used for **KNNImputer** (handling missing data) and regression modeling.
- **Matplotlib & Seaborn:** For data visualization and correlation heatmaps.