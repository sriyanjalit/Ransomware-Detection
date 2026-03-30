import time
import os
import pandas as pd
import joblib
import csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from features.entropy_calculator import calculate_entropy

# ================= LOAD MODELS =================
rf_model = joblib.load("ml/ransomware_model.pkl")

try:
    xgb_model = joblib.load("ml/xgboost_ransomware_model.pkl")
    use_xgb = True
except:
    print("⚠ XGBoost model not found. Using only Random Forest.")
    use_xgb = False


# ================= FEATURE COUNTERS =================
event_stats = {
    "created": 0,
    "deleted": 0,
    "modified": 0,
    "renamed": 0,
    "high_entropy": 0
}

TIME_WINDOW = 10
DATASET_FILE = "dataset/ransomware_fs_features.csv"


# ================= SAVE DATASET =================
def save_to_dataset(stats, label):
    os.makedirs("dataset", exist_ok=True)

    file_exists = os.path.isfile(DATASET_FILE)

    with open(DATASET_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["created", "modified", "deleted", "renamed", "high_entropy", "label"])

        writer.writerow([
            stats["created"],
            stats["modified"],
            stats["deleted"],
            stats["renamed"],
            stats["high_entropy"],
            label
        ])


# ================= MONITOR =================
class RealTimeMonitor(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            event_stats["created"] += 1

    def on_deleted(self, event):
        if not event.is_directory:
            event_stats["deleted"] += 1

    def on_moved(self, event):
        if not event.is_directory:
            event_stats["renamed"] += 1

    def on_modified(self, event):
        if not event.is_directory and os.path.isfile(event.src_path):
            event_stats["modified"] += 1

            try:
                entropy = calculate_entropy(event.src_path)

                # 🔍 Debug print
                print(f"📈 Entropy: {entropy:.2f} | File: {event.src_path}")

                # 🔥 Correct threshold for encrypted data
                if entropy > 7.2:
                    event_stats["high_entropy"] += 1

            except Exception as e:
                print("Entropy error:", e)


# ================= PREDICTION =================
def predict_activity(stats):

    features = pd.DataFrame([{
        "created": stats["created"],
        "modified": stats["modified"],
        "deleted": stats["deleted"],
        "renamed": stats["renamed"],
        "high_entropy": stats["high_entropy"]
    }])

    print("\n📊 Activity Summary:")
    print(stats)

    # -------- Random Forest --------
    rf_pred = rf_model.predict(features)[0]
    rf_prob = rf_model.predict_proba(features)[0]

    print("\n🌳 Random Forest:")
    print(f"Prediction : {'🚨 Ransomware' if rf_pred else '✅ Normal'}")
    print(f"Confidence : {max(rf_prob)*100:.2f}%")

    # -------- XGBoost --------
    if use_xgb:
        xgb_pred = xgb_model.predict(features)[0]

        print("\n⚡ XGBoost:")
        print(f"Prediction : {'🚨 Ransomware' if xgb_pred else '✅ Normal'}")

        final_pred = 1 if (rf_pred == 1 or xgb_pred == 1) else 0
    else:
        final_pred = rf_pred

    # 🔥 STRONG RULE-BASED DETECTION (FIXED POSITION)
    if stats["high_entropy"] > 5:
        final_pred = 1

    if stats["modified"] > 50 and stats["high_entropy"] > 2:
        final_pred = 1

    # -------- FINAL RESULT --------
    print("\n🚨 FINAL RESULT:")
    if final_pred == 1:
        print("🚨🚨 RANSOMWARE DETECTED! 🚨🚨")
    else:
        print("✅ Normal Activity")

    print("-" * 50)

    return final_pred


# ================= MAIN =================
if __name__ == "__main__":

    path = input("Enter directory path to monitor: ")

    if not os.path.exists(path):
        print("❌ Invalid directory!")
        exit()

    observer = Observer()
    observer.schedule(RealTimeMonitor(), path, recursive=True)
    observer.start()

    print(f"\n🔍 Monitoring started on: {path}")
    print(f"⏱ Time Window: {TIME_WINDOW} seconds\n")

    start_time = time.time()

    try:
        while True:
            time.sleep(1)

            if time.time() - start_time >= TIME_WINDOW:

                result = predict_activity(event_stats)

                save_to_dataset(event_stats, result)
                print("📁 Data saved automatically!")

                # reset stats
                for key in event_stats:
                    event_stats[key] = 0

                start_time = time.time()

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("\n🛑 Monitoring stopped.")