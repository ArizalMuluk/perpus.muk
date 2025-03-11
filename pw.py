import bcrypt

def generate_password_hash(password):
    """Menghasilkan hash kata sandi menggunakan bcrypt."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

password = "admin"
hashed_password = generate_password_hash(password)
print(hashed_password)