from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

def hash_password(password):
    hashed_password = password_hasher.hash(password)
    return hashed_password

def verify_password(user_password, db_password):
    verification = password_hasher.verify(user_password, db_password)
    return verification