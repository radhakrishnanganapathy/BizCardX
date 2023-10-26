# mysql_connection.py
from sqlalchemy import create_engine, Column, String, Integer, Text, Date, Interval, func, extract,ARRAY
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from sqlalchemy.orm import Session
from db import Base
from db import get_db

# Define the database connection
# secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit/secrets.toml")

class Card(Base):
     __tablename__ = 'card'
     id = Column(Integer,primary_key=True)
     name = Column(String(255))
     position = Column(String(255))
     mobile = Column(ARRAY(String))
     email = Column(String(255))
     website = Column(String(255),nullable = False, index = True)
     address = Column(String(255))

     def create_card (db:Session,name,position,mobile,email,website,address):
           db_return = Card(
                 name = name,
                 position = position,
                 mobile = mobile,
                 email = email,
                 website = website,
                 address = address,
           )
           db.add(db_return)
           db.commit()
           db.refresh(db_return)
           return db_return
    