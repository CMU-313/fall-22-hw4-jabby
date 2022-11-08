import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)
    
    @app.route('/')
    def hello():
        return "to interact with this API, use the predict route", 200 

    @app.route('/predict')
    def predict():
        ERROR_422 = jsonify({"error": "Query values do not satisfy accepted data ranges"})
        ERROR_400 = jsonify({"error": "Malformed request"})
        
        #use entries from the query string here but could also use json
        failures = request.args.get('failures')
        absences = request.args.get('absences')
        G1 = request.args.get('G1')
        G2 = request.args.get('G2')
        
        # status=400: check that all 4 features are provided (not None)
        if failures == None or absences == None or G1 == None or G2 == None:
            return ERROR_400, 400
            

        # status=422: check values are okay
        def check422(var, vmin, vmax):
            # must be int or can be parsed to int
            val = None
            if type(var) == int:
                val = var
            elif type(var) == str and var.isdigit():
                val = int(var)
            else:
                return False
            
            # must not be a decimal
            if int(val) != val:
                return False
            
            # must be in the right ranges
            return val >= vmin and val <= vmax

        if not (check422(failures, 1, 4) and check422(absences, 0, 93) \
            and check422(G1, 0, 20) and check422(G2, 0, 20)):
            return ERROR_422, 422


        # pass features as a query into the ML model
        query_df = pd.DataFrame({
            'failures': pd.Series(failures),
            'absences': pd.Series(absences),
            'G1': pd.Series(G1),
            'G2': pd.Series(G2)
        })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        result = {"high_quality": np.ndarray.item(prediction) == 1}
        return jsonify(result), 200