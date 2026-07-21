from auth import Auth

auth = Auth()

print(auth.register("john", "secret123"))

print(auth.login("john", "secret123"))

print(auth.login("john", "wrongpassword"))

print(auth.list_users())

auth.close()