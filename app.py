from flask import Flask, render_template, url_for
import os

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/registration.html')
def registration():
    return render_template('registration.html')

@app.route('/questions.html')
def questions():
    return render_template('questions.html')

@app.route('/quiz.html')
def quiz():
    return render_template('quiz.html')

@app.route('/reset password.html')
def reset():
    return render_template('reset password.html')

@app.route('/about-us.html')
def about():
    return render_template('about-us.html')

@app.route('/contact-us.html')
def contact():
    return render_template('contact-us.html')

@app.route('/features.html')
def features():
    return render_template('features.html')

@app.route('/forgot password.html')
def forgot():
    return render_template('forgot password.html')


if __name__=="__main__":
    app.run(debug=True)