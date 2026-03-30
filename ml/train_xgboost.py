import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from xgboost import XGBClassifier

# -------- Load Dataset --------
data = pd.read_csv("dataset/dataset.csv")

X = data.drop("label", axis=1)
y = data["label"]

# -------- Split --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# -------- Train XGBoost Model --------
model = XGBClassifier(
    n_estimators=150,
    max_depth=5,
    learning_rate=0.1,
    eval_metric="logloss",
    use_label_encoder=False
)

model.fit(X_train, y_train)

# -------- Predict --------
y_pred = model.predict(X_test)

# -------- Results --------
print("\n✅ XGBoost Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n📝 Classification Report:\n", classification_report(y_test, y_pred))

# -------- Save Model --------
joblib.dump(model, "ml/xgboost_ransomware_model.pkl")

print("\n✅ XGBoost Model saved successfully!")
