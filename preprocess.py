import pandas as pd
import joblib
from datetime import datetime, timedelta

label_encoder = joblib.load('label_encoder.joblib')
scaler = joblib.load('scaler.joblib')

def append_data(df, hubid, current_time):
    new_data = []
    for i in range(1, 6):
        timestamp = current_time + timedelta(hours=i)
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        hour = timestamp.hour

        new_entry = {
            'hubId': hubid,
            'AQI_Avg': 0,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour
        }
        new_data.append(new_entry)
    new_df = pd.DataFrame(new_data)
    df = df._append(new_df, ignore_index=True)

    return df

def create_json_format(deviceId, current_time, value, index):
    timestamp = current_time + timedelta(hours=index)
    timestamp_iso = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
    data = {
        'deviceId': deviceId,
        'max': {
            'value': float(value),
            'created': timestamp_iso
        },
        'min': {
            'value': float(value),
            'created': timestamp_iso
        },
        'avg': float(value),
        'created': timestamp_iso
    }
    return data

def preprocess_data(formatted_results):
    df = pd.DataFrame(formatted_results)
    df['device_id'] = df['deviceid'].str.split('_').str[0]
    df['device_index'] = df['deviceid'].str.split('_').str[1]
    df['hubId'] = df['device_id'] + '_' + df['device_index']
    df = df.drop(columns=['deviceid', 'device_index', 'device_id'])
    df['hubId'] = label_encoder.transform(df['hubId'])
    df['AQI_Avg'] = scaler.transform(df[['AQI_Avg']])
    
    return df

def format_data(result, device_id):
    formatted_results = []
    for avg_data in result:
        avg_value = avg_data['avg']
        created_datetime = avg_data['created']
        
        year = created_datetime.year
        month = created_datetime.month
        day = created_datetime.day
        hour = created_datetime.hour
        formatted_result = {
            'deviceid': device_id,
            'AQI_Avg': avg_value,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour
        }
        formatted_results.append(formatted_result)
    return formatted_results

