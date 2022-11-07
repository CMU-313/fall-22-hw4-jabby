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
        return "try the predict route it is great!"


    @app.route('/predict')
    def predict():
        #use entries from the query string here but could also use json
        failures = request.args.get('failures')
        absences = request.args.get('absences')
        G1 = request.args.get('G1')
        G2 = request.args.get('G2')
        
        # TODO: check that all 4 features are provided (not None)


        # TODO: check that all 4 features are the proper type (ints or can be parsed to ints)


        # TODO: check that all 4 features are in the right ranges


        # pass features as a query into the ML model
        query_df = pd.DataFrame({
            'failures': pd.Series(failures),
            'absences': pd.Series(absences),
            'G1': pd.Series(G1),
            'G2': pd.Series(G2)
        })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.asscalar(prediction))