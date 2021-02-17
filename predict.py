from flask_restful import Api, Resource, reqparse
import numpy as np
from sklearn.externals import joblib
# Load prebuilt model
HEART_MODEL = joblib.load('heart.model')

# Create predict method
class Predict(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('age')
        parser.add_argument('resting_bp')
        parser.add_argument('chol')
        parser.add_argument('max_heart_rate')

        # Use parser to create dictionary of data input
        args = parser.parse_args() 
        # Convert input data to array
        X_new = np.fromiter(args.values(), dtype=float) 
        # Generate prediction for a single value
        out = {'Prediction': str(HEART_MODEL.predict([X_new])[0])}
        # print('------------------------------------'+str(HEART_MODEL.predict([X_new])[0]))
        return out, 200