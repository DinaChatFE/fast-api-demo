from typing import Optional
from fastapi.datastructures import Default
from sqlalchemy import Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, Float
from database import Base


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description= Column(String, nullable=False)
    
class User(Base):
    __tablename__= "users"
    id = Column(Integer , primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String , nullable=False)
    
    
class Customer(Base):
    __tablename__  = "customers"
    id =  Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shop_name= Column(String, nullable=True)
    is_famous= Column(Boolean, nullable=True)
    user = relationship("User")
    class Config:
        orm_mode = True
        
"""Relatonsip highly recommendations clients and customers"""
        
client_product = Table(
    'client_product',
    Base.metadata,
    Column("client_id", Integer, ForeignKey('clients.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)
      
class Product(Base):
    __tablename__ = "products"
    id =  Column(Integer, primary_key=True)
    title =  Column(String, nullable=False)
    price =  Column(Float, default=0.0)
    client = relationship('Client', secondary="client_product", backref="produce")
    class Config:
        orm_mode = True


class Client(Base): 
    __tablename__ = "clients"
    id =  Column(Integer, primary_key=True)
    name =  Column(String, nullable=False)
    phone_number =  Column(String, nullable=True)
    is_verification =  Column(String, default=False)
    product = relationship('Product', secondary="client_product", backref="user")
    class Config:
        orm_mode = True

