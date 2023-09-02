import hashlib



def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_password(password, hash): # Hash the input password and compare it with the stored hashed password
    if hash_password(password)==hash:
        return True
    
    return False