# base de datos
from DataBase.sql import get_db_sql_connection
import sqlite3 as sql
from sqlite3 import Connection
# models
from models.user_system import Employee
# jwt
from jose import jwt, JWTError
# seguridad
import bcrypt
# fastAPI
from fastapi import HTTPException, status
from fastapi import Depends
# errores
from errors.error import *
# funciones
from .fuctions_system import *


# buscar empleados en la base de datos
def search_employee (username:str, db:Connection) -> Employee:
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM employees WHERE employees.username ='{username}'") # realizamos la consulta a la base de datos
    fields = [descripcion[0] for descripcion in cursor.description] #cremos una variable con un bucle for para recolectar los campos del empleado en la base de datos
    records = cursor.fetchall() # obtenemos el valor de los campos
    for record in records: # bucle for en valores de los campos
        result = {} # inicializamos un dict
        for field,value in zip(fields,record): # cremos un bucle for que itere las dos varibles que tenemos: los campos(fields) y los valores (records)
            result[field] = value # indicamos que el campo es igual al valor
        employee = Employee(**result)
        return employee

# actulizar empleados en la base de datos
def update_employee (employee:Employee, db:Connection):   
    cursor = db.cursor() # cursor

    try:
        employee_db = search_employee(employee.username,db) # obtenemos el empleado de la base de datos (no actulizado)
        
    except EmployeeNotFoundError as e:
        return {'error':e}
    
    if employee_db.email != employee.email: # comprobamos que el empleado a actulizar no tenga el mismo email que el ya existente
        try:
            query = "UPDATE employees SET email = ? WHERE employees.username = ?" # realizamos la consulta
            cursor.execute(query, (employee.email,employee_db.username)) # ejecutamos la consulta
            db.commit() # relizamos el commit
            
     
        except Exception :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error':'the employee e could not update'}) 
    
    encode_password_employee = HashPw(employee.password.encode('utf-8')) # codificamos las contraseñas
    encode_password_db = HashPw(employee_db.password.encode('utf-8'))
    
    if not ChekPw(encode_password_db,encode_password_employee): # si las contraseñas del actualizado y el ya existente no coinciden, relizamos la consulta
        try:
            query = "UPDATE employees SET password = ? WHERE employees.username = ?" # consulta
            cursor.execute(query,(encode_password_employee,employee.username)) # ejecutamos la consulta
            db.commit() # hacemos el commit
        
        except:
             return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error':'the employee p could not update'})
         
        
# eliminar empleados      
def delete_employee (username:str , db:Connection):
    cursor = db.cursor() # cursor
    try:
        query = "DELETE FROM employees WHERE employees.username = ?" # consulta
        cursor.execute(query,(username,)) # executamos la consulta
        db.commit()
    
        if cursor.rowcount == 0: # si no se realizo ningun cambio el rowcount va a ser igual a 0, en ese caso lanzamos la exepcion
            raise DeleteError

        return 'deleted employee' # retornamos un mensaje 
        
    except DeleteError as e:
        db.rollback()
        return e # retornamos el error
     
   
    