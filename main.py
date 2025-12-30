from flask import Flask,request,jsonify,url_for,render_template
import pickle
import numpy as np
import pandas as pd

app=Flask(__name__)
redmodel=pickle.load(open('regmodel.pkl','rb'))'))
scaler=pickle.load(open('scaler.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/predict',methods=['POST'])
def predict_api():
    data=request.json['data']
    


