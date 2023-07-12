# fastAPI
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# seguridad
import bcrypt
from security.seed import secret_key
from security.auth_user import oauth2_scheme_employee, auth_employee
#models
from models.user_system import Employee,EmployeeDB , session
# funciones
from functions.fuctions_employee import *
from functions.fuctions_system import *
# administrador de contexto
from contextlib import contextmanager
# base de datos
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
# jwt
from jose import jwt, JWTError

router = APIRouter(tags=['employee'],responses={status.HTTP_404_NOT_FOUND:{'message':'not found'}})

#administrador de contexto
@contextmanager
def session_scope ():
    try:
        yield session
        session.commit()
        
    except:
        session.rollback()
        raise Exception
    
    finally:
        session.close()

@router.post('/SignUp/employee', response_model=Employee)
async def employee(employee:Employee):
    employee_dict = dict(employee) #transformamos el parametro en una variable de tipo dict
    #password = bcrypt.hashpw(employee.password.encode('utf-8'),secret) # creamos una variable para encriptar la contraseña del empleado
    password = HashPw(employee.password.encode('utf-8'))
    employee_dict['password'] = password # replazamos el valor del campo "password" con el valor encriptado 
    new_employee = EmployeeDB(**employee_dict) # creamos una variable para convertir el dicionario en un empleado de base de datos
    new_employee.creation_date = datetime.now() #le añadimos la fecha de cracion al campo creation_date
    
    with session_scope() as func_session: #abrimos el administrador de contexto
        func_session.add(new_employee) # añadimos el empleado a la base de datos
    
    employee_db = session.query(EmployeeDB).filter(EmployeeDB.email == employee.email).one() # creamos una variable que busca el empleado añadido en la base de datos
    employee_response = Employee(id=employee_db.id,username=employee_db.username, name=employee_db.name, last_name=employee_db.last_name, email=employee_db.email, password=employee_db.password, creation_date=employee_db.creation_date) # creamos una variable de tipo employee con los daots obtenidos de la base de datos
    employee_response.dict() # transformamos dicha variable en un dicionario
    session.close()
    
    return employee_response # devolvemos el empleado con todos sus atributos



    
# ver los datos del empleaado utiliziando la autenticacion que se obtiene mediante el token de acceso 
@router.get('/data/employee')
async def employee(employee:Employee = Depends(auth_employee)):
    return employee

# actualizar empleados utilizando la autenticacion que se obtiene mediente el token de acceso
@router.put('/employee/update')
async def employee(employee:Employee, token:str = Depends(auth_employee), db:Connection = Depends(get_db_sql_connection)):
    try:
        conn = sql.connect(db) #conexion a la base de datos
        
    except sql.Error as e:
        return {'conection error':e}
    
    try:
        update_employee(employee,conn) # utilizamos nustra funcion para actulizar al empleado
        conn.commit()
        
    except:
        conn.rollback()
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={'error':'the update be failed'})

    

    update = search_employee(employee.username,conn) # buscamos el usuario actulizado en la base de datos
    conn.close()
    return update # retornamos el usuario 

# eliminar a un empleado
@router.delete('/employee/delete')
async def employee(employee:Employee = Depends(auth_employee), db:Connection = Depends(get_db_sql_connection)):
    try:
        conn = sql.connect(db) # conexion
    
    except sql.Error as e:
        return {'conection error':e}
    
    try:
        username = employee.username # obtenemos el nombre de usuario
        delete = delete_employee(username,conn) # utilizamos nustra funcion para eliminar empleados
        conn.close()
        
    except Exception:
        return {'error':'the action could not be performed'}
    
    return delete # retornamos la funcion 



