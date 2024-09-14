import secrets

# Generate a new secret key
new_secret_key = secrets.token_hex(32)
print(new_secret_key)

