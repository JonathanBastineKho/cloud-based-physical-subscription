from flask import render_template, url_for, request, redirect
from app import app, login_manager, bcrypt, datab
from flask_login import login_user, login_required, current_user, logout_user
from app.db import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        if User.query.filter_by(email=email).first() == None and User.query.filter_by(username=username).first() == None:
            user = User(username=username,
            email=email, 
            password=bcrypt.generate_password_hash(request.form["password"], 13, prefix=b"2b"))
            datab.session.add(user)
            datab.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route("/login")
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"])
        if user != None and bcrypt.check_password_hash(pw_hash=user.password, password=request.form["password"]):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))