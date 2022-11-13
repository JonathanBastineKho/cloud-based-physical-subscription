from flask import render_template, url_for, request, redirect
from app import app, login_manager, bcrypt, datab, product_api, door_api, basedir, publicKey, privateKey
from flask_login import login_user, login_required, current_user, logout_user
from app.db import User, Company, Door, Key
from flask import session
from functools import wraps
import rsa
from werkzeug.utils import secure_filename
import os
import datetime

ALLOWED_EXTENSIONS = {'heic', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def company_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and session.get("user_type") == "company":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('complogin'))
    return decorated_function

def user_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and session.get("user_type") == "individual":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
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
        phone_number = request.form["phonenumber"]
        if User.query.filter_by(email=email).first() == None and User.query.filter_by(username=username).first() == None and User.query.filter_by(phone_number=phone_number):
            user = User(username=username,
            email=email, 
            password=bcrypt.generate_password_hash(request.form["password"], 13, prefix=b"2b"),
            phone_number=phone_number)
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

@app.route("/dashboard", methods=["GET", "POST"])
@company_only
def dashboard():
    if request.method == "POST":
        if request.form["form_type"] == "add_product":
            file = request.files['file']
            interval = request.form["interval"]
            product_name = request.form["product_name"]
            desc = request.form["product-details"]
            price = float(request.form["price"])
            category = request.form["category"]
            serial_number = request.form["serial_number"]
            result_door = door_api.check_status(doorID=serial_number, 
            id=rsa.decrypt(current_user.phonepass_id, privateKey).decode('utf8'),
            password=rsa.decrypt(current_user.phonepass_pw, privateKey).decode('utf8'))

            if result_door["success"] and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename) # might be different for other OS
                file.save(os.path.join(basedir, image_url))
                if interval.lower() == "hour":
                    result = product_api.create_complete(
                        name=product_name,
                        imageURL=image_url,
                        description=desc,
                        price=price,
                        recurring=False
                    )
                else:
                    result = product_api.create_complete(
                        name=product_name,
                        image_url=image_url,
                        description=desc,
                        price=price,
                        recurring=True,
                        interval=interval.upper()
                    )
                print(result)
                # Add door to database
                if result["success"]:
                    datab.session.add(
                        Door(
                            door_id=result["message"]["id"],
                            door_name=product_name,
                            serial_number=serial_number,
                            category=category,
                            description=desc,
                            company_username=current_user.username,
                            price=price,
                            interval=interval,
                            image_url=image_url,
                            posting_status='SALE'
                        )
                    )
                    datab.session.commit()
        elif request.form["form_type"] == "phonepass_id":
            pp_id = request.form["pp_id"].encode('utf8')
            current_user.phonepass_id = rsa.encrypt(pp_id, publicKey)
            datab.session.commit()
        elif request.form["form_type"] == "phonepass_pw":
            pp_pw = request.form["pp_password"].encode('utf8')
            current_user.phonepass_pw = rsa.encrypt(pp_pw, publicKey)
            datab.session.commit()

    return render_template("dashboard.html")

@app.route("/dashboard_content/<path:content>")
@company_only
def content(content):
    if content == "door":
        doors = Door.query.filter_by(company_username=current_user.username).all()
        return render_template(f"dashboardcomp/{content}.html", doors=doors)
    return render_template(f"dashboardcomp/{content}.html")

@app.route("/index_content/<path:content>")
def index_content(content):
    return render_template(f"{content}.html")

@app.route("/door")
def door():
    return render_template("product.html")

@app.route("/access/<serial_number>", methods=["POST"])
@user_only
def access(serial_number):
	if request.method == "POST":
		door = Door.query.filter_by(serial_number=serial_number).first()
		if door == None:
			return {"success": False, "message": f"Door {serial_number} not found."}
		key = Key.query.filter_by(door_sn=door.serial_number, user_username=current_user.username).all()
		if len(key) == 0:
			return {"success": False, "message": f"User access denied."}

		now = datetime.date.today()
		for k in key:
			if k.start_time <= now and (k.end_time >= now or k.end_time == None):
				company = Company.query.get(door.company_username)
				phonepass_id = rsa.decrypt(company.phonepass_id, privateKey)
				phonepass_pw = rsa.decrypt(company.phonepass_pw, privateKey)
				result = door_api.unlock(phonepass_id, phonepass_pw, serial_number, current_user.phone_number)
				return {"success": True, "message": f"User access granted."}
		return {"success": False, "message": f"User's key has expired."}
