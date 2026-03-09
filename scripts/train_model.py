import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print("Loading dataset...")

# Get project root directory

base_dir = os.path.dirname(os.path.dirname(__file__))

# Dataset path

data_path = os.path.join(base_dir, "dataset", "ransomware_fs_features.csv")

# Load dataset

data = pd.read_csv(data_path)

# Features

X = data.drop("label", axis=1)

# Target

y = data["label"]

print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.3,
random_state=42,
stratify=y
)

print("Training model...")

model = RandomForestClassifier(n_estimators=100, random_state=42)

model.fit(X_train, y_train)

print("Testing model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, zero_division=0)
recall = recall_score(y_test, predictions, zero_division=0)
f1 = f1_score(y_test, predictions, zero_division=0)

print("\nModel Performance")
print("-------------------")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

# Save model

model_path = os.path.join(base_dir, "ml", "ransomware_model.pkl")

joblib.dump(model, model_path)

print("\nModel saved successfully in ml folder")
