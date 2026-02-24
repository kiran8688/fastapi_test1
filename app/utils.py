from pwdlib import PasswordHash # import the password hash from pwdlib

password_hash = PasswordHash.recommended() # create the password hash using the recommended algorithm


def hash_password(password: str) -> str: # create the hash password function
    return password_hash.hash(password) # hash the password

def verify_password(plain_password: str, hashed_password: str) ->bool: # create the verify password function
    return password_hash.verify(plain_password, hashed_password) # verify the password