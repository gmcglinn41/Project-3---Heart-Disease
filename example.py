import requests

def run_request():
    url = 'http://127.0.0.1/predict'
    body = {
        "age": 20,
        "resting_bp": 120,
        "chol": 245,
        "max_heart_rate": 150
    }
    response = requests.post(url, data=body)
    return response.json()