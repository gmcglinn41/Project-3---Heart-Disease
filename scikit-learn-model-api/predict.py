from flask_restful import Api, Resource, reqparse
import numpy as np
from sklearn.externals import joblib
# Load prebuilt model
IRIS_MODEL = joblib.load('iris.smd')

# Create predict method
class Predict(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('petal_length')
        parser.add_argument('petal_width')
        parser.add_argument('sepal_length')
        parser.add_argument('sepal_width')

        # Use parser to create dictionary of data input
        args = parser.parse_args() 
        # Convert input data to array
        X_new = np.fromiter(args.values(), dtype=float) 
        # Generate prediction for a single value
        out = {'Prediction': IRIS_MODEL.predict([X_new])[0]}
        return out, 200