from flask import Flask
import numpy as np
from flask_restful import Api
from predict import Predict
import requests
from example import run_request
# from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
# Create APP
app = Flask(__name__)
API = Api(app)
# Load database
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite" #os.environ.get('DATABASE_URL', '') or 
# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Add predict to route predict
API.add_resource(Predict, '/predict')
# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")
@app.route('/example')
def run_example():
    res = run_request()
    return res
@app.route('/parameters/<age>&<resting_bp>&<chol>&<max_heart_rate>')
def get_prediction(age=5, resting_bp=5, chol=5, max_heart_rate=5):
    url = 'https://heartdiseasegail.herokuapp.com/predict'
    body = {
        "age": age,
        "resting_bp": resting_bp,
        "chol": chol,
        "max_heart_rate": max_heart_rate
    }
    response = requests.post(url, data=body)
    return response.json()
@app.route('/create/<first_name>&<last_name>')
def create(first_name=None, last_name=None):
  return 'Hello ' + first_name + ',' + last_name
# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["petName"]
        lat = request.form["petLat"]
        lon = request.form["petLon"]
        pet = Pet(name=name, lat=lat, lon=lon)
        db.session.add(pet)
        db.session.commit()
        return redirect("/", code=302)
    return render_template("form.html")
@app.route("/api/pals")
def pals():
    results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()
    hover_text = [result[0] for result in results]
    lat = [result[1] for result in results]
    lon = [result[2] for result in results]
    pet_data = [{
        "type": "scattergeo",
        "locationmode": "USA-states",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",
        "marker": {
            "size": 50,
            "line": {
                "color": "rgb(8,8,8)",
                "width": 1
            },
        }
    }]
    return jsonify(pet_data)
# allow both GET and POST requests
@app.route('/heart-calculator', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        age = request.form.get('age')
        resting_bp = request.form.get('resting_bp')
        chol = request.form.get('chol')
        max_heart_rate = request.form.get('max_heart_rate')
        url = 'https://heartdiseasegail.herokuapp.com/predict'
        body = {
            "age": age,
            "resting_bp": resting_bp,
            "chol": chol,
            "max_heart_rate": max_heart_rate
        }
        response = requests.post(url, data=body)      
        print(response.json())  
        return render_template('prediction.html',prediction=response.json()["Prediction"])
    # otherwise handle the GET request
    return render_template('calculator.html')
if __name__ == '__main__':
    app.run(debug=True, port='80')