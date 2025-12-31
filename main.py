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
@app.route('/predict',methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(list(data.values())) #output 1‑D array: shape (n_features,)
    print(np.array(list(data.values())).reshape(1,-1)) #because scikit‑learn models expect a 2‑D array shaped (n_samples, n_features)
    new_Data=scaler.transform(np.array(list(data.values())).reshape(1,-1))
    output= regmodel.predict(new_Data)
    print(output[0])
    return jsonify(output[0])

if __name__ == "__main__":
    app.run(debug=True)