from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
import json
from datetime import datetime, timedelta
from pipeline import get_stats_by_device
from preprocess import preprocess_data, format_data, append_data, create_json_format
import pandas as pd
from sequence import to_sequences
import joblib
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message=".*Trying to unpickle estimator LabelEncoder from version.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*Trying to unpickle estimator StandardScaler from version.*")

app = Flask(__name__)

model = load_model('model1.keras')
if(model):
    print("Model Loaded!")
scaler = joblib.load('scaler.joblib')

@app.route('/predict_aqi', methods=['POST'])
def predict_aqi():
    try:
        data = request.get_json()
        device_id = data.get('device_id')
        start_date = '2024-03-14T00:00:00Z'  
        end_date = '2024-03-15T07:59:59Z'
        filter = 'hourly'  
        print(device_id)
        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%SZ')

        result = get_stats_by_device(device_id, start_date, end_date, filter)
        print(len(result))

        if result:
            formatted_results = format_data(result, device_id)
            df = preprocess_data(formatted_results[:10])
            df = append_data(df, df['hubId'][0], end_date)
            spots_test = df['AQI_Avg'].tolist()
            x_future_test, y_future_test= to_sequences(10, spots_test)
            predictions = model.predict(x_future_test)
            predictions_original_scale = scaler.inverse_transform(predictions)
            # print(predictions_original_scale)
            results = []
            for index, value in enumerate(predictions_original_scale, start=1):
                json_data = create_json_format(device_id, end_date, value[0], index)
                # print(json_data)
                results.append(json_data)
            # print(results)
            return jsonify({'predictions': results}), 200
        else:
            return jsonify({'message': 'No results found.'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



