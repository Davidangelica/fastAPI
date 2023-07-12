# fastAPi
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#funciones
from functions.functions_user import *
from functions.fuctions_employee import *
from functions.fuctions_system import *
# base de datos
from DataBase.db import db_users
from datetime import datetime, timedelta
import sqlite3 as sql
#models
from models.user_system import User,Employee,EmployeeDB,session
#jwt
from jose import jwt, JWTError
from jwt.exceptions import JWTDecodeError
#security
from security.seed import secret_key,ALGORITHM,ACCESS_TOKEN_DURATION
import bcrypt
import secrets



#router
router = APIRouter()


#oauth2
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl='/login/user')
oauth2_scheme_employee = OAuth2PasswordBearer(tokenUrl='/login/employee')



# operacion login
@router.post('/login/user')
async def login(form:OAuth2PasswordRequestForm = Depends()):
    try:
        user = search_users('username',form.username) # buscamos el usuario en la base de datos
        if not user:
           raise Exception # si no existe lanzamos una exepcion
    except:
         return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={'error':'the user is not correct'})
     
    try:
        user_dict = dict(user) # creamos una variable con el usuario de base de datos
        user_pw = user_dict['password'] # obtenemos la clave del usuario
        check_pw = ChekPw(form.password,user_pw)# creamos una variable que verifique la contraseña encriptada
        if not check_pw: 
            raise Exception # si la contraseña no se verifica lanzamos una exepcion
    except:
        return  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={'error':'the password is not correct'})
    
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) # creamos una variable que define el tiempo de expiracion del token, en este caso seria el actual mas un minuto 
    token = {'sub':form.username,  #creamos el token
                     'exp':expire}
    
    token_access = jwt.encode(token,secret_key,algorithm=ALGORITHM)
    
    return {'access_token':token_access, 'token_type':'bearer'}


# funcion para autenticar usuarios
def auth_user (token:str = Depends(oauth2_scheme_user)):
    try:
        username = jwt.decode(token, secret_key ,algorithms=[ALGORITHM]).get('sub') # decodificamos el token para obtener el valor del sub
        
    except JWTDecodeError:
        return {'error':'decoding failed'}
    
    try:
        user = search_users('username',username)
        return user
    
    except UserNotFondError:
        return {'error':'the user not been found'}
    



@router.post('/login/employee')
async def login(form:OAuth2PasswordRequestForm = Depends(), db:Connection = Depends(get_db_sql_connection)):
    conn = sql.connect(db) # conexion a la base de datos
    employee = search_employee(form.username,conn) # buscamos el empleado
    employee_dict = dict(employee) # transformamos la variable en un dict
     
    try:
        pw = employee_dict['password'] #obtenemos la clave 
        chek_pw = ChekPw(form.password,pw) # chequemos que la contraseña se la correcta 
        if not chek_pw: # si no lo es lanzamos una exepcion
            raise Exception 
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='the user cant been find')
   
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) # cremos una variable con la expiracion del token
    token = {'sub':form.username, # creamos el token
             'exp':expire}
    
    
    token_access = jwt.encode(token,secret_key,algorithm=ALGORITHM)  # encriptamos el token
    
    return {'token':token_access,
            'token_type':'bearer'}   #retornamos el token
     

# funcion de autenticacion     
def auth_employee (token:str = Depends(oauth2_scheme_employee), db:Connection = Depends(get_db_sql_connection)):
    conn = sql.connect(db) # conexion a la base de datos
    employee_username = jwt.decode(token,secret_key,algorithms=ALGORITHM).get('sub') # decodificamos el token para obter el valor del sub
    employee = search_employee(employee_username,conn) # buscamos el empleado en la base de datos
    return employee # retornamos el empleado