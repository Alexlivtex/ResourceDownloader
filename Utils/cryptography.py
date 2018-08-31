from cryptography.fernet import Fernet
import pickle

def genKey(key_path):
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        pickle.dump(key, f)

def loadKey(key_path):
    with open(key_path, "rb") as f:
        key = pickle.load(f)
        return key

def encryption_str(plain_text, key_path):
    cipher_suite = Fernet(loadKey(key_path))
    cipher_bytes = cipher_suite.encrypt(bytes(plain_text, "utf-8"))
    cipher_text = cipher_bytes.decode("utf-8")
    return cipher_text

def decryption_str(cipher_text, key_path):
    cipher_suite = Fernet(loadKey(key_path))
    plain_bytes = cipher_suite.decrypt(bytes(cipher_text, "utf-8"))
    plain_text = plain_bytes.decode("utf-8")
    return plain_text
