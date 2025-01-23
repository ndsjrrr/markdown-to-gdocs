from cryptography.fernet import Fernet

def encrypt_auth_file(path):
    with open(path, 'rb') as f:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(f.read())
        with open(path + '.enc', 'wb') as ef:
            ef.write(key + b'\n' + cipher_text)

def decrypt_auth_file(path):
    with open(path, 'rb') as ef:
        key, cipher_text = ef.read().split(b'\n', 1)
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(cipher_text)
        with open(path[:-4], 'wb') as f:
            f.write(plain_text)

# if __name__ == '__main__':
    # encrypt_auth_file('auth.json')
    # decrypt_auth_file('auth.json.enc')
