from datetime import datetime
from python.config import db  # Updated import
from sqlalchemy.dialects.postgresql import JSON

class Statutory(db.Model):
    __tablename__ = 'statutory'
    id = db.Column(db.Integer, primary_key=True)
    statutory_name = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    compliances = db.relationship('Compliance', backref='statutory_relation', lazy=True)

class Compliance(db.Model):
    __tablename__ = 'compliance'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    statutory_id = db.Column(db.Integer, db.ForeignKey('statutory.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    statutory = db.relationship('Statutory', back_populates='compliances', overlaps="statutory_relation")

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    answer_type = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    deptname = db.Column(db.String(500), nullable=False)

    # Define the relationship with ScreenData
    screens = db.relationship('ScreenData', back_populates='department', lazy=True)



class ScreenData(db.Model):
    __tablename__ = 'table_data'
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    screen_name = db.Column(db.String(255), nullable=False)  # Name of the table
    columns = db.Column(JSON, nullable=False)  # Columns stored as JSON
    row_data = db.Column(JSON, nullable=True)  # Row data stored as JSON (can be nullable)

    # Foreign key column to link to Department
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    # Define the relationship with Department
    department = db.relationship('Department', back_populates='screens')