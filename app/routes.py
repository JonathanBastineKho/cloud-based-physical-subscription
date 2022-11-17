from flask import render_template, url_for, request, redirect, jsonify
from app import app, login_manager, bcrypt, datab, product_api, door_api, basedir, publicKey, privateKey, customer_api, order_api
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
    door = Door.query.all()
    return render_template('index.html', doors=door)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        phone_number = request.form["phonenumber"]
        if User.query.filter_by(email=email).first() == None and User.query.filter_by(username=username).first() == None and User.query.filter_by(phone_number=phone_number):
            res = customer_api.create(name=username, email=email, phone=phone_number)
            customer_id = res["message"]["id"]
            user = User(username=username,
            email=email, 
            password=bcrypt.generate_password_hash(request.form["password"], 13, prefix=b"2b"),
            phone_number=phone_number,
            customer_id=customer_id)
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
        if request.form["form_type"] == "add_product" and current_user.phonepass_id != None and current_user.phonepass_pw != None:
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
                            posting_status='SALE',
                            product_code=result["message"]["code"],
                            price_code=result["message"]["prices"]["code"]
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

@app.route("/door/<int:door_id>")
def door(door_id):
    door = Door.query.filter_by(door_id=door_id).first()
    return render_template("product.html", door=door)

@app.route("/access", methods=["POST"])
@user_only
def access():
	if request.method == "POST":
		serial_number = request.form["serial_number"]
		door = Door.query.filter_by(serial_number=serial_number).first()
		if door == None:
			return {"success": False, "message": f"Invalid Serial Number Please Try Again"}
		key = Key.query.filter_by(door_sn=door.serial_number, user_username=current_user.username).all()
		if len(key) == 0:
			return jsonify({"success": False, "message": f"User access denied."})

		now = datetime.date.today()
		for k in key:
			if k.start_time <= now and (k.end_time >= now or k.end_time == None):
				company = Company.query.get(door.company_username)
				phonepass_id = rsa.decrypt(company.phonepass_id, privateKey)
				phonepass_pw = rsa.decrypt(company.phonepass_pw, privateKey)
				result = door_api.unlock(phonepass_id, phonepass_pw, serial_number, current_user.phone_number)
				return {"success": True, "message": f"User access granted."}
		return jsonify({"success": False, "message": f"User's key has expired."})

@app.route("/key")
@user_only
def key():
	keys = Key.query.filter_by(user_username=current_user.username).all()
	key_data = []
	now = datetime.date.today()
	for k in keys:
		door = Door.query.get(k.door_sn)
		company = Company.query.get(door.company_username)
		key_data.append({
			"product_name": door.door_name,
			"company": company.username,
			"category": door.category,
			"start_date":k.start_time,
			"interval": door.interval,
			"status": k.end_time == None or k.end_time >= now,
			"end_time": k.end_time,
			"product_desc": door.description
		})
	return render_template("key.html", keys=key_data)

@app.route("/subscribe", methods=["POST"])
@user_only
def subscribe():
    door_id = request.form["door_id"]
    door = Door.query.filter_by(door_id=door_id).first()
    result = order_api.create(
        customerID=current_user.customer_id,
        productCode=door.product_code,
        priceCode=door.price_code
    )
    if result["success"]:
        print(result)
        order_code = result["message"]["orderCode"]
        return f"https://api.steppay.kr/api/public/orders/{order_code}/pay?successUrl=https://your-site.com&errorUrl=https://your-site.com&cancelUrl=https://your-site.com"

@app.route("/finishPayment-add42645cb668c92f0491e98c5365c3cb8af0b663f6b02431df56bee8baf7a25352b7bd6ccc7c086bd0e2515a91d5cbd032d0b0f11baf7c0a3f6d70f1b02b67fee7150bb364d72b8f87951ab0cf25016e27c909a23f539cb54de1299d1fb1a577d39a40941e2ba2a78e7ebf0d11b5c180fcd5f0173adcc8201b363739a2e025bcfcdbbd2c2cd538be640691fb944290f599583f432e74a1be71bb014cd1e32b38df69272718d9b7674a2c376072178e2431395081b27e72f13040d136e548c6430359f14cd99af33f2bf64c7fb8f96cf0d26be1d2225c728c9630376ed0aafa7aa7b77c2ae30b1dcd788354ce685b5aaa3f03727c5155be3422ded23801ac47a34d7c079685f50e81ed2f6cf240a45bcc399c5c31ce6dd5738e221f19a76d4f41ff8bac489e4c07456382cceedc5a453255b86128f83b5c73275eefb142ba115", methods=["POST"])
def finishPayment():
    pass

@app.route("/test-webhook", methods=["POST"])
def test_webhook():
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")
    print("test")