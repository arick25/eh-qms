from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    version = Column(String)
    owner = Column(String)
    date_created = Column(Date)
    file_path = Column(String)

class Audit(Base):
    __tablename__ = 'audits'
    id = Column(Integer, primary_key=True)
    area = Column(String)
    auditor = Column(String)
    findings = Column(String)
    corrective_action = Column(String)
    date = Column(Date)
    status = Column(String)

class CAPA(Base):
    __tablename__ = 'capa'
    id = Column(Integer, primary_key=True)
    issue = Column(String)
    root_cause = Column(String)
    corrective_action = Column(String)
    preventive_action = Column(String)
    owner = Column(String)
    date_created = Column(Date)
    status = Column(String)
    effectiveness_review = Column(String)

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True)
    type = Column(String)               # e.g. "Mild Steel", "Stainless"
    gauge = Column(String)             # e.g. "14ga", "11ga"
    thickness = Column(String)         # e.g. "0.075 in"
    length = Column(String)            # e.g. "96 in"
    width = Column(String)             # e.g. "48 in"
    quantity = Column(Integer)         # Number of sheets

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    department = Column(String)
    status = Column(String)           # e.g. Active, On Leave, Terminated
    pay_rate = Column(String)         # e.g. "$22/hr", "$55,000/yr"
    hire_date = Column(Date)
    contact = Column(String)          # optional: phone or email

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    customer = Column(String)
    quoted_price = Column(String)
    estimated_time = Column(String)       # e.g. "3 days", "40 hours"
    actual_time = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    final_report = Column(String)
