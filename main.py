from math import prod
from typing import List
from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user
from database import get_db
from helper.file_upload import UploadFileSteam
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from auth import AuthHandler
from schema import ClientOut, CreateJob, CreateCustomer, CustomerOut, ProductOut, User, Client, Product
from model import User as UserModel, Product as ProductModel,Customer, Job, Client as ClientModel
from fastapi.staticfiles import StaticFiles
from faker import Faker
import random

app = FastAPI(debug=True)
fake = Faker()


''' Mounted static file access public '''
app.mount("/static", StaticFiles(directory="static"), name="static")

''' Upload file in fast api '''
@app.post('/uploads')
def upload_file(file: UploadFile = File(...)):
    file_upload = UploadFileSteam(file)
    file_name_response = file_upload.upload()
    return {'file_name': file_name_response}

@app.get("/")
def main():
    return {"message": "successfully running"}


@app.post('/jobs')
def jobs(details: CreateJob, db: Session = Depends(get_db)):
    job_obj = Job(
        title=details.title,
        description=details.description
    )
    db.add(job_obj)
    db.commit()
    return {
        "success": True,
        "details": details
    }


@app.get('/jobs/{id}')
def get_jobs(id: int, db: Session = Depends(get_db)):
    result = db.query(Job).filter(Job.id == id).first()
    if not result:
        raise HTTPException(
            status_code=404, detail="Jobs doesn't found in the data tables")
    return result


#  login authorization for jwt token
"""this is the starting point of using jwt token in the project"""

auth_handler = AuthHandler()
users = []


@app.post('/register', status_code=201)
def register(auth_details: User):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password
    })
    return


@app.post('/login')
def login(auth_details: User):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return {'token': token}


@app.get('/unprotected')
def unprotected():
    return {'hello': 'world'}


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}


# relationsship users with users


@app.post('/customer')
def customers(customer_detail: CreateCustomer, db: Session = Depends(get_db)):
    details = Customer(
        shop_name=customer_detail.shop_name,
        is_famous = customer_detail.is_famous,
        user_id=customer_detail.user_id
    )
    db.add(details)
    db.commit()
    return {
        "success": True,
        "details": customer_detail
    }
    
"""
Demo of responding one to one relationships, 
customer to user relationship , response model, traditional ways of response looping
"""
@app.get('/customer', response_model=List[CustomerOut])
def get_customer( db: Session = Depends(get_db)):
    """Response with response mode a bit of advance responding class"""
    db =   db.query(Customer).all()
    # if using joinload must be create inner class Config orm = True inside model or pydantic responding 
    return db    
    """Traditional ways of responding via loop"""
    # result = list()
    # for d in db:
    #     love = { "shop_owner": d.shop_name }
    #     if d.user:
    #         love['user'] = {"id": d.user.username, "username": d.user.username}
    #     result.append(love)
    # return result
    # return db
    # result =  db.query(Customer, UserModel).join(UserModel).all()
    
"""Demo of responsing many to many relationships tables"""

@app.post("/clients")
def post_client(client_detail: Product , db: Session = Depends(get_db)):
    students = list()
    for _ in range(1 , 40):
        students.append(ClientModel(name = fake.name(), phone_number = fake.country_calling_code() + fake.msisdn(), is_verification = False))
    
    details = ProductModel(title = fake.bs() , price = random.randint(100, 1000) )
    ''' append use for insert client many to many relations with product '''
    for student in students:
        details.user.append(student)
    ''' insert and commit ot databases '''
    db.add(details)
    db.commit()
    return {"status": True}

@app.post('/client/product')
def client_product( client_id : int, detail: Product, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Could not find client")
    product = ProductModel(title= detail.title, price = detail.price)
    product.user.append(client)
    db.add(product)
    db.commit()
    return detail
    
    
@app.get('/clients', response_model=List[ClientOut])
def get_clients(db: Session = Depends(get_db)):
    dbs=  db.query(ClientModel).all()
    return dbs


@app.get('/prodcut/{id}', response_model=ProductOut)
def get_product( id: int ,db: Session = Depends(get_db)):
    response = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not response:
        raise HTTPException(status_code= 404, detail="We can not preserve to attemping")
    return response
