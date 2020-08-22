from flask import Flask, request, abort, redirect, url_for, render_template, send_file, flash

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField
from wtforms.validators import DataRequired

from werkzeug import secure_filename

import numpy as np
import pandas as pd

import joblib
import os

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField('file', validators=[DataRequired()])


print('Loading model ...')
model = joblib.load('model.pkl')

@app.route('/')
def hello_world():
    return '<h1>Hello my friend!</h1>'


@app.route('/user/<username>')
def show_user_profile(username):
    username = float(username)
    return f'Hello {username * username}'


@app.route('/avg/<nums>')
def avg(nums):
    nums = [float(num) for num in nums.split(',')]
    return f'average is {np.mean(nums)}'


def predict_result(param):
    is_pattern_right = True
    wrong_symbol = None

    for c in param:
        if c is not ',' and not c.isdigit():
            is_pattern_right = False
            wrong_symbol = c
            break
        
    if not is_pattern_right:
        raise f"Wrong pattern! Expect nums and ','.\t\tFind {wrong_symbol}"
    if param[0] == ',':
        raise "Wrong pattern! Should start with num"
    if param[-1] == ',':
        raise "Wrong pattern! Should end with num"

    param = np.array([float(num) for num in param.split(',')]).reshape(1, -1)
    if len(*param) != 4: 
        raise "Expect 4 numbers!"

    print('Predicting ...')
    return model.predict(param)


@app.route('/iris/<param>')
def iris(param):
    
    try:
        predict = predict_result(param)
    except:
        return redirect(url_for('bad_request'))

    results = {
        0: "setosa", 
        1: "virginica",
        2: "versicolor"
    }

    return f'<img src="/static/{results[predict[0]]}.jpg" alt="{predict[0]}">'


@app.route('/bad_request')
def bad_request():
    return abort(400)


@app.route('/iris_post', methods=['POST'])
def add_message():
    content = request.get_json()

    try:
        predict_ = {"class": str(predict_result(content['flower'])[0])}
    except:
        return redirect(url_for('bad_request'))
    
    return (predict_)


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():

        f = form.file.data
        print(f)
        filename = form.name.data + '.csv'
        
        print('Reading ...')
        df = pd.read_csv(f, header=None)
        
        print('Predicting ...')
        predict_ = model.predict(df)

        result = pd.DataFrame(predict_)
        result.to_csv(filename, index=False, header=None)

        return send_file(filename,
                    mimetype='text/csv',
                    attachment_filename=filename,
                    as_attachment=True)

    return render_template('submit.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            result_name = 'result.csv'
            filename = secure_filename(file.filename)
            
            print('Reading ...')
            df = pd.read_csv(file, header=None)
            
            print('Predicting ...')
            predict_ = model.predict(df)

            result = pd.DataFrame(predict_)
            result.to_csv(result_name, index=False, header=None)

            return send_file(result_name,
                    mimetype='text/csv',
                    attachment_filename=result_name,
                    as_attachment=True)
    
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
