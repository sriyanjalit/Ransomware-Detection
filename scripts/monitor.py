import os
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# -------- Load trained model --------
base_dir = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(base_dir, "ml", "ransomware_model.pkl")
model = joblib.load(model_path)

print("Model loaded. Ready to start monitoring...")

# -------- Monitoring logic --------
monitoring_data = []

def start_monitoring():
    print("\nMonitoring started. Enter feature rows (or type 'stop' to end):")
    while True:
        try:
            user_input = input("Enter comma-separated features (or 'stop'): ")
            if user_input.strip().lower() == "stop":
                break
            # Convert input into a list of floats
            features = [float(x) for x in user_input.strip().split(",")]
            monitoring_data.append(features)
        except Exception as e:
            print("Invalid input, try again.", e)

def stop_monitoring_and_evaluate():
    if not monitoring_data:
        print("No data collected.")
        return

    # Convert to DataFrame
    # Assuming your feature names match training features
    data_path = os.path.join(base_dir, "dataset", "ransomware_fs_features.csv")
    feature_names = pd.read_csv(data_path).drop("label", axis=1).columns
    df = pd.DataFrame(monitoring_data, columns=feature_names)

    # Predictions
    predictions = model.predict(df)
    
    # Ask user for actual labels to compute metrics
    print("\nEnter actual labels for collected data (comma-separated 0/1):")
    y_true_input = input()
    y_true = [int(x) for x in y_true_input.strip().split(",")]

    # Compute metrics
    accuracy = accuracy_score(y_true, predictions)
    precision = precision_score(y_true, predictions, zero_division=0)
    recall = recall_score(y_true, predictions, zero_division=0)
    f1 = f1_score(y_true, predictions, zero_division=0)

    # Print table
    results = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1 Score"],
        "Score": [accuracy, precision, recall, f1]
    })
    print("\nMonitoring Performance Table")
    print(results)

# -------- Main --------
start_monitoring()
stop_monitoring_and_evaluate()