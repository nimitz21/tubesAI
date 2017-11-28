import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug.wrappers import Response
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
	for form in request.form:
		print(form)

	model_dir_path = os.path.dirname(os.path.realpath('model_id3.pkl'))
	model = tree.DecisionTreeClassifier()
	model = joblib.load(model_dir_path + '\\flaskr\\model_id3.pkl')

	discrete_columns = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'sex']
	label_encoder = preprocessing.LabelEncoder()

	discrete_values = []

	for column in discrete_columns:
		label_encoder.classes_ = np.load(model_dir_path + '\\flaskr\\' + column + '.npy')
		discrete_values.append(label_encoder.transform([request.form[column]]).astype(int)[0])
		print(label_encoder.transform([request.form[column]])[0])

	print('TEST')
	print(discrete_values[0])

	dataFrame = pd.DataFrame([[request.form['age'], discrete_values[0], discrete_values[1], request.form['education-num'], discrete_values[2], discrete_values[3], discrete_values[4], discrete_values[5], request.form['capital-gain'], request.form['capital-loss'], request.form['hours-per-week']]], columns=['age', 'workclass', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week'])
	test_data = np.array(dataFrame)
	print(dataFrame)

	result = model.predict(test_data)
	label_encoder.classes_ = np.load(model_dir_path + '\\flaskr\\income.npy')
	print(label_encoder.inverse_transform(result)[0])
	transform_result = label_encoder.inverse_transform(result)[0]
	return render_template('page.html', result=transform_result)


