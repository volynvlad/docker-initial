from flask import Flask
import numpy as np

app = Flask(__name__)

import joblib
knn = joblib.load('knn.pkl')

@app.route('/')
def hello_world():
    print(3 + 30)
    return '<h1>Hello my friend!</h1>'


@app.route('/user/<username>')
def show_user_profile(username):
    username = float(username)
    return f'Hello {username * username}'


@app.route('/avg/<nums>')
def avg(nums):
    nums = [float(num) for num in nums.split(',')]
    return f'average is {np.mean(nums)}'

@app.route('/iris/<param>')
def iris(param):
    param = np.array([float(num) for num in param.split(',')]).reshape(1, -1)
    assert len(*param) == 4

    return f"input - {param}, output - {knn.predict(param)}"
    # return str(knn.predict(iris_X_test))
