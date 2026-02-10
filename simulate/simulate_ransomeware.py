from cryptography.fernet import Fernet
import os

key = Fernet.generate_key()
cipher = Fernet(key)

folder = "test_data/files"

for root, _, files in os.walk(folder):
    for file in files:
        path = os.path.join(root, file)
        with open(path, "rb") as f:
            data = f.read()
        encrypted = cipher.encrypt(data)
        with open(path, "wb") as f:
            f.write(encrypted)
print("Simulation complete: files encrypted safely.")
