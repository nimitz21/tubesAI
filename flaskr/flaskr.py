import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from sklearn.externals import joblib
from sklearn import preprocessing
import numpy
import pandas

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict (
	SECRET_KEY = 'tubesAiUranus',
	USERNAME = 'admin',
	PASSWORD = 'default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def showPage():
	return render_template('page.html')

@app.route('/submit', methods=['POST'])
def submit():
	model = joblib.load('model_mlp.pkl')
	encoder = preprocessing.LabelEncoder()
	encoder.classes_ = numpy.load('label_encoder.npy')
	dataFrame = pd.DataFrame([request.form['age'], request.form['workclass'], request.form['education'], request.form['marital-status'], request.form['occupation'], request.form['relationship'], request.form['sex'], request.form['capital-gain'], request.form['capital-loss'], request.form['hours-per-week'], request.form['income']], columns=['age', 'workclass', 'education', 'marital-status', 'occupation', 'relationship', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'income'])
	dataFrame_labelled = dataFrame.apply(encoder.transform)
	result = model.predict(dataFrame_labelled)
	return redirect(url_for('showPage'), result=result)


