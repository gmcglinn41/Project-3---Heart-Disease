import requests

def run_request():
    url = 'https://jl-uwa-demo.herokuapp.com/predict'
    body = {
        "petal_length": 2,
        "sepal_length": 2,
        "petal_width": 0.5,
        "sepal_width": 3
    }
    response = requests.post(url, data=body)
    return response.json()