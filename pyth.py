import bcrypt

password = "sumaprati@gmail.com"
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print(password_hash)