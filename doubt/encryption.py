from cryptography.fernet import Fernet

# print(Fernet.generate_key())

SECRET_KEY = b'H3VDE2snbngf05rBDtNqzgHGWVWaqy7uOw9eXdlCcgI='
fernet = Fernet(SECRET_KEY)

def encrypt_text(text):
    if text:
        return fernet.encrypt(text.encode()).decode()
    return None

def decrypt_text(text):
    if text:
        return fernet.decrypt(text.encode()).decode()
    return None


    
