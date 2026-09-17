# 🚘 Used Car Price Prediction

A Machine Learning web application that predicts the selling price of a used car based on its characteristics.

The application was developed using Python, Scikit-learn, and Streamlit. A Random Forest Regressor was selected after comparing several regression algorithms.

## 🌐 Live Demo

👉 [Try the application](https://usedcarpriceprediction-9k3o42vwuz9wxdnd2axfwu.streamlit.app/)

---

## 📌 Project Overview

Buying or selling a used car requires estimating its market value.

This project aims to build a Machine Learning model capable of predicting the selling price of a used car using information such as:

- Kilometers driven
- Present price
- Fuel type
- Seller type
- Transmission
- Vehicle age

The trained model is integrated into an interactive Streamlit application.

---

## 🎯 Objectives

- Explore and prepare used car data.
- Compare different regression algorithms.
- Select a suitable model based on validation performance.
- Build an interactive prediction interface.
- Deploy the application using Streamlit Community Cloud.

---

## 📊 Features

The application allows users to:

- Enter the car's mileage.
- Specify the current price.
- Select the fuel type.
- Select the seller type.
- Select the transmission type.
- Enter the age of the vehicle.
- Obtain an estimated selling price.

---

## 🤖 Machine Learning Models

Several regression algorithms were compared:

- Random Forest Regressor
- XGBoost Regressor
- Decision Tree Regressor
- Linear Regression
- Ridge Regression
- Lasso Regression

### Selected Model

**Random Forest Regressor**

The Random Forest model was selected based on its validation performance among the compared models.

---

## ⚙️ Data Preprocessing

The project uses a Scikit-learn pipeline containing:

- `RobustScaler` for numerical features.
- `OneHotEncoder` for categorical features.
- `ColumnTransformer` to combine preprocessing steps.
- `Random Forest Regressor` for price prediction.

The complete pipeline is saved using Joblib.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Streamlit
- Git and GitHub

---

## 📁 Project Structure

```text
Used_Car_Price_Prediction/
│
├── app.py
├── car_price_model.joblib
├── requirements.txt
└── README.md
