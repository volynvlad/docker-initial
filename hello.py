from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    print(3 + 30)
    return '<h1>Hello my friend!</h1>'