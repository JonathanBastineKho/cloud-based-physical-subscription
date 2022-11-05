from flask import render_template, url_for, request, redirect
from app import app, login_manager, bcrypt, datab
from flask_login import login_user, login_required, current_user, logout_user
from app.db import User, Company
from flask import session
from functools import wraps

def company_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and session.get("user_type") == "company":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('complogin'))
    return decorated_function

@login_manager.user_loader
def load_user(username):
    user_type = session["user_type"]
    if user_type == "individual":
        return User.query.get(username)
    elif user_type == "company":
        return Company.query.get(username)

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
            session['user_type'] = 'individual'
            login_user(user)
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user != None and bcrypt.check_password_hash(pw_hash=user.password, password=request.form["password"]):
            session['user_type'] = 'individual'
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/companylogin", methods=["GET", "POST"])
def complogin():
    if request.method == "POST":
        company = Company.query.filter_by(email=request.form["email"]).first()
        if company != None and bcrypt.check_password_hash(pw_hash=company.password, password=request.form["password"]):
            session['user_type'] = 'company'
            login_user(company)
            return redirect(url_for('index'))
    return render_template("complogin.html")

@app.route("/companyregister", methods=["GET", "POST"])
def compregister():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        address = request.form["address"]
        password = request.form["password"]
        if Company.query.filter_by(email=email).first() == None and Company.query.filter_by(username=username).first() == None:
            company = Company(username=username,
            email=email,
            password=bcrypt.generate_password_hash(password, 13, prefix=b"2b"),
            address=address)
            datab.session.add(company)
            datab.session.commit()
            session['user_type'] = 'company'
            login_user(company)
            return redirect(url_for('index'))
    return render_template("compregister.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard")
@company_only
def dashboard():
    return render_template("dashboard.html")

@app.route("/dashboard_content/<path:content>")
@company_only
def content(content):
    return render_template(f"dashboardcomp/{content}.html")