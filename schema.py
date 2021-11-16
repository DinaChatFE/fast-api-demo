from typing import List, Optional
from pydantic import BaseModel

'''
schema is just the way we want request body to required
and model the way that we insert and mutate data, also get from db as well
'''


class CreateJob(BaseModel):
    title: str
    description: str


class User(BaseModel):
    username: str
    password: str
    class Config:
        orm_mode = True


class CreateCustomer(BaseModel):
    shop_name: str
    user_id: int
    is_famous: bool

# response model pydantic 
class UserOut(BaseModel):
    id: int 
    username: str
    class Config:
        orm_mode = True
    
class CustomerOut(BaseModel):
    id: int
    shop_name: Optional[str] = ""
    is_famous:  Optional[bool] = False
    user: Optional[UserOut]
    class Config:
        orm_mode =True
    
    
class Product(BaseModel):
    title: str
    price: float
    class Config: 
        orm_mode = True
        
class Client(BaseModel):
    name: str
    phone_number: Optional[str]
    is_verification: bool
    class Config: 
        orm_mode = True
        
class ProductOut(BaseModel):
    title: str
    price: float
    client : Optional[List[Client]]
    class Config:
        orm_mode = True
    
class ClientOut(BaseModel):
    name:  Optional[str]
    phone_number: Optional[str]
    product: Optional[List[ProductOut]]
    class Config:
        orm_mode = True
        