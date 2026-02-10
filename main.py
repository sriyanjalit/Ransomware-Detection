import joblib
import numpy as np

model = joblib.load("ml/ransomware_model.pkl")

print("Enter feature values:")
created = int(input("Files created: "))
modified = int(input("Files modified: "))
deleted = int(input("Files deleted: "))
renamed = int(input("Files renamed: "))
high_entropy = int(input("High entropy writes: "))

features = np.array([[created, modified, deleted, renamed, high_entropy]])

prediction = model.predict(features)

if prediction[0] == 1:
    print("🚨 Possible ransomware detected!")
else:
    print("✅ Normal behavior")
