from flask import render_template, url_for, request, redirect, jsonify
from app import app, login_manager, bcrypt, datab, product_api, door_api, basedir, publicKey, privateKey, customer_api, order_api, subscription_api, csrf
from flask_login import login_user, login_required, current_user, logout_user
from app.db import User, Company, Door, Key, Sale
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
            if res["success"]:
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
                        imageURL=image_url,
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
    # Get method
    return render_template("dashboard.html")

@app.route("/dashboard_content/<path:content>")
@company_only
def content(content):
    if content == "door":
        doors = Door.query.filter_by(company_username=current_user.username).all()
        return render_template(f"dashboardcomp/{content}.html", doors=doors)
    elif "dashboardindex" in content:
        result = Sale.query.filter_by(company_username=current_user.username).all()
        lst_returned = []
        for sale in result:
            door = Door.query.filter_by(serial_number=sale.serial_number).first()
            lst_returned.append({
                "door_name" : door.door_name,
                "serial_number" : sale.serial_number,
                "category" : door.category,
                "value" : sale.value,
                "transaction_date": sale.date.strftime("%Y-%m-%d")
            })
        if content == "dashboardindexgraph":
            return jsonify(sorted(lst_returned, key=lambda lst:datetime.datetime.strptime(lst["transaction_date"], "%Y-%m-%d")))
        total_sales = sum([i["value"] for i in lst_returned])
        return render_template(f"dashboardcomp/{content}.html", sales=lst_returned, total_sales=total_sales)
        
    return render_template(f"dashboardcomp/{content}.html")

@app.route("/request_qr/<string:serial_num>")
@company_only
def render_qr(serial_num):
    return render_template(f"dashboardcomp/QRmodal.html", serial_num=serial_num)

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
			return jsonify({"success": False, "message": f"Invalid Serial Number Please Try Again"})
		key = Key.query.filter_by(door_sn=door.serial_number, user_username=current_user.username).all()
		if len(key) == 0:
			return jsonify({"success": False, "message": f"User access denied."})
		now = datetime.date.today()

		for k in key:
			if k.start_time <= now:
				if k.end_time != None and k.end_time >= now:
					company = Company.query.get(door.company_username)
					phonepass_id = rsa.decrypt(company.phonepass_id, privateKey)
					phonepass_pw = rsa.decrypt(company.phonepass_pw, privateKey)
					result = door_api.unlock(phonepass_id, phonepass_pw, serial_number, current_user.phone_number)
					return jsonify({"success": True, "message": f"User access granted."})
				status = subscription_api.info(k.key_id)
				if k.end_time == None and status["success"] and status["message"]["status"] == "ACTIVE":
					company = Company.query.get(door.company_username)
					phonepass_id = rsa.decrypt(company.phonepass_id, privateKey)
					phonepass_pw = rsa.decrypt(company.phonepass_pw, privateKey)
					result = door_api.unlock(phonepass_id, phonepass_pw, serial_number, current_user.phone_number)
					return jsonify({"success": True, "message": f"User access granted."})
		return jsonify({"success": False, "message": f"User's key has expired."})

@app.route("/key", methods=["GET", "POST"])
@user_only
# @csrf.exempt
def key():
    if request.method == "POST":
                if request.form["form_type"] == "cancel_subscription":
                    print(request.form)
                    key_id = request.form["key_id"]
                    cancel = subscription_api.cancel(key_id, when="END_OF_PERIOD")
                    if cancel["success"]:
                        return jsonify({"success": True, "message": "Successfully cancelled subscription."})
                    return jsonify({"success": False, "message": "Error! Failed to cancel subscription."})
    keys = Key.query.filter_by(user_username=current_user.username).all()
    key_data = []
    now = datetime.date.today()
    for k in keys:
        door = Door.query.get(k.door_sn)
        company = Company.query.get(door.company_username)
        data = {
            "product_name": door.door_name,
            "company": company.username,
            "category": door.category,
            "start_date":k.start_time,
            "interval": door.interval,
            "status": k.end_time == None or k.end_time >= now,
            "end_time": k.end_time,
            "product_desc": door.description,
            "key_id": k.key_id
        }
        if k.end_time == None:
            data["status"] = "ACTIVE"
        elif k.end_time >= now:
            data["status"] = "PENDING_CANCEL"
        else:
            data["status"] = "CANCELLED"
        key_data.append(data)
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
        return order_api.get_payment_url(order_code,successURL="", errorURL="", cancelURL="")

@app.route("/finishSubscribe-add42645cb668c92f0491e98c5365c3cb8af0b663f6b02431df56bee8baf7a25352b7bd6ccc7c086bd0e2515a91d5cbd032d0b0f11baf7c0a", methods=["POST"])
@csrf.exempt
def finishSubscribe_add42645cb668c92f0491e98c5365c3cb8af0b663f6b02431df56bee8baf7a25352b7bd6ccc7c086bd0e2515a91d5cbd032d0b0f11baf7c0a():
	content = request.json
	result = subscription_api.info(content["id"])
	if result["success"]:
		# When creating new subscription
		if content["status"] == "ACTIVE":
			start_date = datetime.datetime.strptime(result["message"]["start_date"], "%Y-%m-%d")
			door = Door.query.filter_by(door_id=result["message"]["door_id"]).first()
			datab.session.add(
				Key(
					key_id=content["id"],
					door_sn=door.serial_number,
					user_username=result["message"]["customer_username"],
					start_time=start_date
				)
			)
			datab.session.add(
				Sale(
					company_username=door.company_username,
					value=result["message"]["total_price"],
					date=start_date,
                    serial_number=door.serial_number
				)
			)
			datab.session.commit()
			return jsonify({'success':True})
	
		# When cancelled/pending cancel
		else:
			key = Key.query.get(content["id"])
			key.end_time = datetime.datetime.strptime(result["message"]["end_date"], "%Y-%m-%d").date
			datab.session.commit()
			return jsonify({'success':True})

	return jsonify({'success':False})

@app.route("/simulation/<serial_number>")
@company_only
def simulation(serial_number):
    serial_number = serial_number
    door = Door.query.filter_by(serial_number=serial_number,company_username=current_user.username).first()
    phonepass_id = rsa.decrypt(current_user.phonepass_id, privateKey)
    phonepass_pw = rsa.decrypt(current_user.phonepass_pw, privateKey)
    if door != None:
        simulateDoor = door_api.check_status(doorID=serial_number, id=phonepass_id, password=phonepass_pw)
        return render_template("simulation.html", door_info=simulateDoor["result"], serial_num = serial_number)
    return render_template("simulation.html", door_info="Error, door not found", serial_num = serial_number)

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        print(request.form)
    return render_template("tester.html")