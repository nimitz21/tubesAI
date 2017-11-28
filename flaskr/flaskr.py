import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from sklearn.externals import joblib
from sklearn import preprocessing
from sklearn import tree
import numpy as np
import pandas as pd

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
	model_dir_path = os.path.dirname(os.path.realpath('model_id3.pkl'))
	model = tree.DecisionTreeClassifier()
	model = joblib.load(model_dir_path + '\\flaskr\\model_id3.pkl')

	discrete_columns = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'sex']
	label_encoder = preprocessing.LabelEncoder()

	discrete_values = []

	for column in discrete_columns:
		label_encoder.classes_ = numpy.load(column + '.npy')
		discrete_values.append(label_encoder.transform([request.form['age']])[0])

	dataFrame = pd.DataFrame([request.form['age'], discrete_values[0], discrete_values[1], discrete_values[2], discrete_values[3], discrete_values[4], discrete_values[5], request.form['capital-gain'], request.form['capital-loss'], request.form['hours-per-week'], request.form['income']], columns=['age', 'workclass', 'education', 'marital-status', 'occupation', 'relationship', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'income'])
	
	result = model.predict(dataFrame)
	return redirect(url_for('showPage'), result=result)


