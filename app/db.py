from app import datab
from flask_login import UserMixin

class User(UserMixin, datab.Model):
    __tablename__ = "user"
    username = datab.Column(datab.String(250), primary_key=True)
    email = datab.Column(datab.String(250), nullable=False, unique=True)
    password = datab.Column(datab.String(1000), nullable=False)
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
    description = datab.Column(datab.String(1000), nullable=False)
    company = datab.relationship("Company", back_populates="door")
    company_username = datab.Column(datab.Integer, datab.ForeignKey('company.username'), primary_key=True) 
    key = datab.relationship("Key", back_populates="door")

class Key(datab.Model):
    __tablename__ = "key"
    company_username = datab.Column(datab.Integer, datab.ForeignKey('door.company_username'), primary_key=True)
    door_id = datab.Column(datab.Integer, datab.ForeignKey('door.door_id'), primary_key=True)
    door = datab.relationship("Door", back_populates="key")
    user_username = datab.Column(datab.String(250), datab.ForeignKey('user.username'), primary_key=True)
    user = datab.relationship("User", back_populates="key")
    start_time = datab.Column(datab.Date, primary_key=True)
    end_time = datab.Column(datab.Date, nullable=False)
    duration = datab.column_property(start_time - end_time)

datab.create_all()