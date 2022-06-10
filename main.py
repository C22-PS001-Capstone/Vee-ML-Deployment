import flask
# from flask import jsonify
import numpy
import tensorflow as tf
import keras
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

app = flask.Flask(__name__)
# WINDOW_SIZE = 60
# trainMaxIndex = 876

# @app.route("/v1/predict", methods=["POST"])
# def predict():
#     data = {"success": False, "forecast": []}
#     try:
#         model = keras.models.load_model("model/v1.h5")
#             # get request parameters
#         params = flask.request.json
#         if params is None:
#             return flask.jsonify(data)
#         if(params != None):
#             input_data = numpy.array(params.get("data"))
#             forecast = (model_forecast(model, pd.Series(input_data), WINDOW_SIZE))*100000
#             data["success"] = True
#             data["forecast"] = list(map(int, forecast.flatten().tolist()))
#     except:
#         print("Get exception")
#     return flask.jsonify(data)

@app.route("/v2/predict", methods=["POST"])
def predict2():
    data = {"success": False, "forecast": []}
    try:
        model = keras.models.load_model("model/v2.h5")
        scaler = MinMaxScaler()

        params = flask.request.json
        if params is None:
            return flask.jsonify(data)
        if(params != None):
            input_data = numpy.array(params.get("data"))
            input_series = pd.Series(input_data)
            input_series = input_series.values.reshape(-1, 1)
            scaler_input_series = scaler.fit_transform(input_series)
            seq_len = int(len(input_data)/5)
            if(len(input_data) < 5):
                raise Exception("Input data is too short")
            if(len(input_data) > 100):
                seq_len = 100
            input_sequences = to_sequences(scaler_input_series, seq_len)
            input_sequences = input_sequences[:,-1,:]

            forecast = model.predict(input_sequences)
            forecast = scaler.inverse_transform(forecast)
            data["success"] = True
            data["forecast"] = list(map(int, forecast.flatten().tolist()))
    except Exception as e:
        print(e)
    return flask.jsonify(data)

# def model_forecast(model, data, window_size):
#     ds = tf.data.Dataset.from_tensor_slices(data)
#     ds = ds.window(window_size, shift=1, drop_remainder=True)
#     ds = ds.flat_map(lambda w: w.batch(window_size))
#     ds = ds.batch(32).prefetch(1)
#     forecast = model.predict(ds)
#     return forecast

def to_sequences(data, seq_len):
    d = []

    for index in range(len(data) - seq_len):
        d.append(data[index: index + seq_len])

    return numpy.array(d)

app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
