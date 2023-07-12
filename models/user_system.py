from pydantic import BaseModel
from datetime import datetime,date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker
import json
from typing import List, Optional

# clase del usuario
class User(BaseModel):
    id : str | None
    username : str
    name : str
    email : str
    password : str


class Employee (BaseModel):
    id : int | None
    username : str
    name : str
    last_name : str
    email : str
    password : str
    creation_date : datetime | None


db_url = "sqlite:///C:/proyecto_FastAPI/DataBase/employees.db"
engine = create_engine(db_url)
Base = declarative_base()

class EmployeeDB(Base):
    __tablename__ = 'employees'
    id = Column(Integer(), primary_key=True)
    username = Column(String(),unique=True)
    name = Column(String(), nullable=False, unique=False)
    last_name = Column(String(), nullable=False, unique=False)
    email = Column(String(), nullable=False,unique=False)
    password = Column(String(), nullable=False,unique=False)
    creation_date = Column(DateTime(),nullable=False)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

