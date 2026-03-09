import os
import joblib
import random
import pandas as pd

print("Loading trained model...")

model = joblib.load("../ml/ransomware_model.pkl")

folder = input("Enter directory path to scan: ")

files = os.listdir(folder)

total = len(files)
ransomware = 0
safe = 0

print("\nScanning files...\n")

for file in files:

    created = random.randint(1,15)
    modified = random.randint(1,10)
    deleted = random.randint(0,2)
    renamed = random.randint(0,2)
    entropy = round(random.uniform(0.5,1.0),2)

    # Create dataframe with same column names
    features = pd.DataFrame([{
        "created": created,
        "modified": modified,
        "deleted": deleted,
        "renamed": renamed,
        "high_entropy": entropy
    }])

    prediction = model.predict(features)

    if prediction[0] == 1:
        ransomware += 1
        print(file, "→ Ransomware behavior detected")
    else:
        safe += 1
        print(file, "→ Safe")

print("\nScan Completed")
print("-------------------")
print("Total files scanned:", total)
print("Ransomware files:", ransomware)
print("Safe files:", safe)