from flask import Flask,request,jsonify,url_for,render_template
import pickle
import numpy as np
import pandas as pd

app=Flask(__name__)
regmodel=pickle.load(open('regmodel.pkl','rb'))
scaler=pickle.load(open('scaler.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict_api():
    # accept either {"data": {...}} or plain feature dict  else in postmn we should give data wrapper too
    payload = request.get_json(force=True)
    if isinstance(payload, dict) and 'data' in payload:
        data = payload['data']
    else:
        data = payload

    if data is None:
        return jsonify({'error': 'no input provided'}), 400

    print(data)
    print(list(data.values()))  # 1-D array: shape (n_features,)
    print(np.array(list(data.values())).reshape(1, -1))  # convert to 2-D
    new_Data = scaler.transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(new_Data)
    print(output[0])
    return jsonify({'prediction': float(output[0])})
if __name__ == "__main__":
    app.run(debug=True)