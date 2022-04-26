import bcrypt
password = b"hidden"

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)

print(salt)
print(hashed)

if bcrypt.checkpw(b"hiden", hashed):
    print("match")
else:
    print ("does not match")