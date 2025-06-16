from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        return generate_key()

def encrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_name, "wb") as file:
        file.write(encrypted_data)

key = load_key()  
encrypt_file("data/data.csv", key)

print("Guarda esta clave en .streamlit/secrets.toml bajo la clave 'encryption_key':")
print(key.decode())