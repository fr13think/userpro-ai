import bcrypt
import logging

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    logging.info("Password hashed")
    return hashed

def check_password(password, hashed_password):
    result = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    logging.info("Password check performed")
    return result