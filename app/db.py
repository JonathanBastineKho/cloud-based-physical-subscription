from app import datab as db

class User(db.Model):
    __tablename__ = "user"
    # Attributes
    username = db.Column("username", db.String(250))
    email = db.Column("email", db.String(250), nullable=False)
    password = db.Column("password", db.String(1000), nullable=False)
    # Constraints
    primary_key = db.PrimaryKeyConstraint("username", name="userPK")
    candidate_key1 = db.UniqueConstraint("email", name="userCK1")

class Company(db.Model):
    __tablename__ = "company"
    # Attributes
    username = db.Column("username", db.String(250))
    email = db.Column("email", db.String(250), nullable=False)
    password = db.Column("password", db.String(1000), nullable=False)
    company_name = db.Column("company_name", db.String(250), nullable=False)
    address = db.Column("address", db.String(250), nullable=False)
    # Constraints
    primary_key = db.PrimaryKeyConstraint("username", name="companyPK")
    candidate_key1 = db.UniqueConstraint("email", name="companyCK1")
    candidate_key2 = db.UniqueConstraint("company_name", "address", name="companyCK2")

class Door(db.Model):
    __tablename__ = "door"
    # Attributes
    company = db.Column("company", db.String(250))
    door_id = db.Column("door_id", db.Integer)
    description = db.Column("description", db.String(1000), nullable=False)
    # Constraints
    primary_key = db.PrimaryKeyConstraint("company", "door_id", name="doorPK")
    foreign_key1 = db.ForeignKeyConstraint(["company"], ["company.username"])
    
class Key(db.Model):
    __tablename__ = "key"
    # Attributes
    company = db.Column("company", db.String(250))
    door_id = db.Column("door_id", db.Integer)
    user = db.Column("user", db.String(250))
    start_date = db.Column("start_date", db.Date)
    end_date = db.Column("end_date", db.Date)
    duration = end_date - start_date # How to make computed column idk?
    # Constraints
    primary_key = db.PrimaryKeyConstraint("company", "door_id", "username", name="keyPK")
    foreign_key1 = db.ForeignKeyConstraint(["company", "door_id"], ["door.company", "door.door_id"])
    foreign_key2 = db.ForeignKeyConstraint(["user"], ["user.username"])
    check1 = db.CheckConstraint("end_date > start_date", name="check1") # Not sure on this
