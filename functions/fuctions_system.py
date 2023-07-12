import bcrypt

def HashPw (password:bytes):
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password,salt)
    return hash_password

def ChekPw (pw1,pw2):
    try:
        chek = bcrypt.checkpw(pw1.encode('utf-8'),pw2.encode('utf-8'))
        return chek
    except:
        return None