from app import datab
from flask_login import UserMixin

class User(UserMixin, datab.Model):
    __tablename__ = "user"
    username = datab.Column(datab.String(250), primary_key=True)
    email = datab.Column(datab.String(250), nullable=False, unique=True)
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

    def get_id(self):
        return self.username

class Door(datab.Model):
    __tablename__ = "door"
    door_id = datab.Column(datab.Integer, primary_key=True)
    serial_number = datab.Column(datab.String(50), nullable=False)
    description = datab.Column(datab.String(1000), nullable=False)
    company = datab.relationship("Company", back_populates="door")
    company_username = datab.Column(datab.Integer, datab.ForeignKey('company.username')) 
    key = datab.relationship("Key", back_populates="door")
    price = datab.Column(datab.Float, nullable=False)
    interval = datab.Column(datab.String(10), datab.CheckConstraint("interval in ('hour', 'day', 'month', 'year')"), nullable=False)
    image_url = datab.Column(datab.String(1000), nullable=False)
    posting_status = datab.Column(datab.String(50), 
    datab.CheckConstraint("posting_status in ('SALE', 'OUT_OF_STOCK', 'UNSOLD', 'WAITING_FOR_APPROVAL', 'REJECTED')"), 
    nullable=False)

class Key(datab.Model):
    __tablename__ = "key"
    door_id = datab.Column(datab.Integer, datab.ForeignKey('door.door_id'), primary_key=True)
    door = datab.relationship("Door", back_populates="key")
    user_username = datab.Column(datab.String(250), datab.ForeignKey('user.username'), primary_key=True)
    user = datab.relationship("User", back_populates="key")
    start_time = datab.Column(datab.Date, primary_key=True)
    end_time = datab.Column(datab.Date, nullable=False)
    duration = datab.column_property(start_time - end_time)

datab.create_all()