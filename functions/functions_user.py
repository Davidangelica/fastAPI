# base de datos
from DataBase.db import db_users
from DataBase.sql import get_db_sql_connection
import sqlite3 as sql
from sqlite3 import Connection
#models
from models.user_system import User,Employee
# jwt
from jose import jwt, JWTError
# security
from security.seed import secret_key,ACCESS_TOKEN_DURATION,ALGORITHM
import bcrypt
# fastAPI
from fastapi import HTTPException
from fastapi import Depends
# errores
from errors.error import UserNotFondError

#from routers.auth_user import secret, ALGORITHM,oauth2_scheme
#from fastapi import Depends
# funcion para convertir el un objeto de tipo User en un dict
def view_user (user) -> dict:
    return {
        'id' : str(user['_id']),
        'username': user['username'],
        'name':user['name'],
        'email': user['email'],
        'password': user['password']
    }

# funcion para retornar la lista de usuarios totales que hay en la base de datos 
# el parametro users va a ser referecia a todos los usuarios extraidos de la base de datos
def total_users (users) -> list:
    return [view_user(user) for user in users]

def search_users (field, key) -> User:
    try:
        user = db_users.local.users_data_base.find_one({field:key})
        return User(**view_user(user))
    except:
        return UserNotFondError


def search_user_db (field,key) -> dict :
    try:
        user = db_users.local.users_data_base.find_one({field:key})
        return user
    except:
        raise Exception
    

def update_user (field,key,user):
    try:
        user = db_users.local.users_data_base.find_one_and_replace({field:key},user)
        return user
    except:
        return None

def delete_user (field,key):
    try:
        user = db_users.local.users_data_base.find_one_and_delete({field:key})
        return user
    except:
        return None
    
