# -*- coding: utf-8 -*-
from flask import render_template
from app import app 

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('information.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/case', methods=['GET', 'POST'])
def case():
    return render_template('case.html')