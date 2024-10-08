from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application=Flask(__name__)

app=application

@app.route('/')
def index():
    return render_template('index.html')

# AGE, GENDER, VETERAN,INCOME, NIGHTS, substanceabuse, completed, probation
@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            age=float(request.form.get('age')),
            substanceabuse=request.form.get('substanceabuse'),
            veteran=request.form.get('veteran'),
            probation=request.form.get('probation'),
            completed=request.form.get('completed'),
            income=float(request.form.get('income'))
        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        return render_template('home.html',results=results[0])
# test
if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
