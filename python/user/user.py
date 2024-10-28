from flask import render_template, request, redirect, url_for, flash
from python.config import app, db 

@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('auth-signin.html')

@app.route('/signup_page',methods=['GET', 'POST'])
def some_page():
    return render_template('auth-signup.html')

@app.route('/role',methods=['GET', 'POST'])
def role():
    return render_template('user.html')
@app.route('/user',methods=['GET', 'POST'])
def user():
    return render_template('add_user_details.html')

@app.route('/department',methods=['GET', 'POST'])
def department():
    return render_template('department.html')

@app.route('/useracess',methods=['GET', 'POST'])
def useracess():
    return render_template('user_access_control.html')