import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import os

# ===== Dataset loading and validation =====
dataset_path = "dataset.csv"

if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"{dataset_path} not found. Make sure the file is in the correct path.")

data = pd.read_csv(dataset_path)
print("Dataset shape:", data.shape)  # Check rows and columns

if data.shape[0] == 0:
    raise ValueError("The dataset is empty. Please provide a valid dataset.")

required_columns = ["created","modified","deleted","renamed","high_entropy","label"]
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"The dataset does not contain a required column: '{col}'")
# Load dataset to project
data = pd.read_csv("dataset.csv")

# Features and label
X = data.drop("label", axis=1)
y = data["label"]

# ===== Split dataset =====
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ===== Train model =====
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ===== Test model =====
y_pred = model.predict(X_test)

# ===== Results =====
print("\n✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n📝 Classification Report:\n", classification_report(y_test, y_pred))
