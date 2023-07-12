# fastAPI
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# seguridad
import bcrypt
from security.auth_user import oauth2_scheme_user,auth_user
from security.seed import secret_key,ALGORITHM
# jwt
from jose import jwt, JWTError
# models
from models.user_system import User
# base de datos
from DataBase.db import db_users
# funciones
from functions.functions_user import *
from functions.fuctions_employee import *
from functions.fuctions_system import *



# router S
router = APIRouter(tags=['users'],responses={status.HTTP_404_NOT_FOUND:{'message':'not found'}})

# visualizar los datos de un usuario
@router.get('/user')
async def user(user : User = Depends(auth_user)):
    return user


#añadir usuarios a la base de datos
@router.post('/SignUp/user',status_code=status.HTTP_201_CREATED)
async def user(user:User):
    
 email = search_users('email',user.email) # buscamos usuario por email
 username = search_users('username',user.username) # buscamos usuario por username
 
 
 if email == User or username == User: # comprobamos si el usuario ya existe 
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error':'the email or username already exist'})
    
 encode_password = user.password.encode('utf-8')
 password = HashPw(encode_password) # encriptamos la contraseña 
                                                            
 user_dict = dict(user) # convertimos el usuario a un dict para alamacenarlo como un json 
 del user_dict['id'] # eliminamos el id porque este se geneara en la base de datos
 user_dict['password'] = password # remplazamos el valor de la contraseña original por el valor encriptado
    
 id = db_users.local.users_data_base.insert_one(user_dict).inserted_id # insertamos el usuario en base de datos y le añadimos un id
 new_user = view_user(db_users.local.users_data_base.find_one({'_id':id})) # buscamos en la base de datos el usuario que añadimos
 return User(**new_user) # retornamos el usuario añadido 



def token_auth (token : str = Depends(oauth2_scheme_user)):
    username = jwt.decode(token, secret_key ,algorithms=[ALGORITHM]).get('sub')
    if not username:
        raise JWTError
    
# actualizar usuarios de la base de datos
@router.put('/user/update')
async def user(user:User, token = Depends(token_auth)):
    user_dict = dict(user) # lo convertimos en dict para trabajarlo como un json
    del user_dict['id'] # le borramos el campo id ya que este esta en la base de datos
    userdb = search_users('_id',ObjectId(user.id)) # creamos una variable con el usuario de la base de datos que vamos a modificar
    
    password = HashPw(user.password) # encriptamos la contraseña 
    user_dict['password'] = password # remplazamos la contraseña por la encriptada
    
    chek_pw = ChekPw(user.password,userdb.password) # creamos una variable para chequear las contraseñas encriptadas
    
    try:
        if userdb.username == user.username and userdb.email == user.email: # comprobamos  si el usuario y email son iguales
            if chek_pw: # en el caso de ser igual comprobamos si la contraseña tambien lo es, si lo es todos los atributos son igual y lanzamos un error
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='the user cant be the same')
            else:
                update_user('_id',ObjectId(user.id),user_dict)
        else:
            update_user('_id',ObjectId(user.id),user_dict) #remplazamos el usuario de la base de datos con el id que coinicida con el nuevo usuario 
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='the user hasnt been updated')
    
    return search_users('_id',ObjectId(user.id)) # retornamos el nuevo usuario

#eliminar usuarios 
@router.delete('/user/delete')
async def user(user:User = Depends(auth_user)):
    id = user.id
    user_delete = search_users('_id',ObjectId(id)) #creamos una variable con el usuario que vamos a eliminar
    try:
        delete_user('_id',ObjectId(id)) #eliminamos el usuario de la base de datos mediante el id
        return user_delete # retornamos el usuario eliminado para saber que la operacion fue exitosa
    except:
       return HTTPException (status_code=status.HTTP_412_PRECONDITION_FAILED, detail={'error':'the user could not been delete'}) # si falla retornamos esta exepción
    