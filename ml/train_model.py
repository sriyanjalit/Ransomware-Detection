import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# -------- Load Dataset --------
data = pd.read_csv("dataset/ransomware_fs_features.csv")

X = data.drop("label", axis=1)
y = data["label"]

# -------- Split --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# -------- Train Model --------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------- Predict --------
y_pred = model.predict(X_test)

# -------- Results --------
print("\n✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n📝 Classification Report:\n", classification_report(y_test, y_pred))

# -------- Save Model --------
joblib.dump(model, "ml/ransomware_model.pkl")

print("\n✅ Model saved successfully!")
