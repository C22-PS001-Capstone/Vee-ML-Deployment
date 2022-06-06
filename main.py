import flask
from flask import jsonify
import numpy
import tensorflow as tf
import keras
import pandas as pd

app = flask.Flask(__name__)
WINDOW_SIZE = 60
trainMaxIndex = 876

@app.route("/predict", methods=["GET"])
def predict():
    data = {"success": False}
    try:
        model = keras.models.load_model("model.h5")
            # get request parameters
        params = flask.request.json
        if params is None:
            return flask.jsonify(data)
        if(params != None):
            input_data = numpy.array(params.get("data"))
            forecast = (model_forecast(model, pd.Series(input_data), WINDOW_SIZE))*100000
            data["success"] = True
            data["forecast"] = list(map(int, forecast.flatten().tolist()))
    except:
        print("Get exception")
    return flask.jsonify(data)

def model_forecast(model, data, window_size):
    ds = tf.data.Dataset.from_tensor_slices(data)
    ds = ds.window(window_size, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
    return forecast

app.run(host='0.0.0.0', port=8080, debug=True)