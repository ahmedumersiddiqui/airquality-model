# Air Quality Index (AQI) Prediction API

This API provides predictions for the Air Quality Index (AQI) for the next few hours using a pre-trained machine learning model. The model leverages historical AQI data from a device, retrieved from an external source. The model is loaded using TensorFlow and the scaler is loaded using `joblib`.

## Features

- Retrieves AQI data from a device for a specific time range.
- Preprocesses the last 10 AQI entries to make predictions for the next few hours.
- Serves predictions using a trained model that utilizes sequential forecasting.
- The model and scaler are loaded using TensorFlow (`model1.keras`) and `joblib` (`scaler.joblib`).

## Prerequisites

- Python 3.x
- MongoDB or other source for AQI data retrieval.
- Required Python libraries (see `requirements.txt`).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ahmedumersiddiqui/aqi-prediction-api.git
   cd aqi-prediction-api
