from app import datab
from flask_login import UserMixin

class User(UserMixin, datab.Model):
    __tablename__ = "user"
    username = datab.Column(datab.String(250), primary_key=True)
    email = datab.Column(datab.String(250), nullable=False, unique=True)
    customer_id = datab.Column(datab.Integer, nullable=False, unique=True)
    password = datab.Column(datab.String(1000), nullable=False)
    phone_number = datab.Column(datab.String(24), nullable=False)
    key = datab.relationship("Key", back_populates="user")
    
    def get_id(self):
        return self.username

class Company(UserMixin, datab.Model):
    __tablename__ = "company"
    username = datab.Column(datab.String(250), primary_key=True)
    email = datab.Column(datab.String(250), nullable=False, unique=True)
    password = datab.Column(datab.String(1000), nullable=False)
    address = datab.Column(datab.String(250), nullable=False)
    door = datab.relationship("Door", back_populates="company")
    sale = datab.relationship("Sale", back_populates="company")
    phonepass_id = datab.Column(datab.LargeBinary(100000))
    phonepass_pw = datab.Column(datab.LargeBinary(100000))

    def get_id(self):
        return self.username

class Door(datab.Model):
    __tablename__ = "door"
    door_id = datab.Column(datab.Integer)
    product_code = datab.Column(datab.String(250), nullable=False)
    door_name = datab.Column(datab.String(50))
    serial_number = datab.Column(datab.String(50), primary_key=True)
    category = datab.Column(datab.String(50))
    description = datab.Column(datab.String(1000))
    company = datab.relationship("Company", back_populates="door")
    company_username = datab.Column(datab.String(250), datab.ForeignKey('company.username')) 
    key = datab.relationship("Key", back_populates="door")
    price = datab.Column(datab.Float)
    price_code = datab.Column(datab.String(250), nullable=False)
    interval = datab.Column(datab.String(10), datab.CheckConstraint("interval in ('hour', 'day', 'month', 'year')"))
    image_url = datab.Column(datab.String(1000))
    sale = datab.relationship("Sale", back_populates="door")
    posting_status = datab.Column(datab.String(50), 
    datab.CheckConstraint("posting_status in ('SALE', 'OUT_OF_STOCK', 'UNSOLD', 'WAITING_FOR_APPROVAL', 'REJECTED')"), 
    nullable=False)

class Key(datab.Model):
	__tablename__ = "key"
	key_id = datab.Column(datab.Integer, nullable=False, primary_key=True)
	door_sn = datab.Column(datab.String(250), datab.ForeignKey('door.serial_number'), nullable=False)
	door = datab.relationship("Door", back_populates="key")
	user_username = datab.Column(datab.String(250), datab.ForeignKey('user.username'))
	user = datab.relationship("User", back_populates="key")
	start_time = datab.Column(datab.Date, nullable=False)
	end_time = datab.Column(datab.Date)
	duration = datab.column_property(start_time - end_time)

class Sale(datab.Model):
    __tablename__ = "sale"
    sale_id = datab.Column(datab.Integer, nullable=False, primary_key=True)
    door = datab.relationship("Door", back_populates="sale")
    serial_number = datab.Column(datab.String(250), datab.ForeignKey('door.serial_number'), nullable=False)
    company = datab.relationship("Company", back_populates="sale")
    company_username = datab.Column(datab.String(250), datab.ForeignKey('company.username'), nullable=False)
    value = datab.Column(datab.Float, nullable=False)
    date = datab.Column(datab.Date, nullable=False)

datab.create_all()