import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

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