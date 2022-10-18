from app import datab

class User(datab.Model):
    __tablename__ = "user"
    id = datab.Column(datab.Integer, primary_key=True)
    email = datab.Column(datab.String(250), nullable=False)
    username = datab.Column(datab.String(250), nullable=False)
    password = datab.Column(datab.String(1000), nullable=False)

class Company(datab.Model):
    __tablename__ = "company"
    id = datab.Column(datab.Integer, primary_key=True)
    email = datab.Column(datab.String(250), nullable=False)
    username = datab.Column(datab.String(250), nullable=False)
    password = datab.Column(datab.String(1000), nullable=False)