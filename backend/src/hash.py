from pwdlib import PasswordHash

def encrypt_password(password):
    hashed_password = PasswordHash.recommended().hash(password)
    return hashed_password
