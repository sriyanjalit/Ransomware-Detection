import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from features.entropy_calculator import calculate_entropy

import time
import csv
import joblib
import numpy as np
import pandas as pd

# ==============================
# Load ML Models
# ==============================
rf_model = joblib.load("ml/ransomware_model.pkl")
xgb_model = joblib.load("ml/xgboost_ransomware_model.pkl")

# ==============================
# Event Stats
# ==============================
event_stats = {
    "created": 0,
    "deleted": 0,
    "modified": 0,
    "renamed": 0,
    "high_entropy": 0
}

TIME_WINDOW = 10


# ==============================
# Alert Logger
# ==============================
def log_alert(message):
    os.makedirs("results", exist_ok=True)
    with open("results/alerts.log", "a") as f:
        f.write(f"{time.ctime()} - {message}\n")


# ==============================
# ML Prediction
# ==============================
def predict_ransomware(features):
    columns = ["created", "modified", "deleted", "renamed", "high_entropy"]
    features_df = pd.DataFrame([features], columns=columns)

    rf_pred = rf_model.predict(features_df)[0]
    xgb_pred = xgb_model.predict(features_df)[0]

    return 1 if (rf_pred == 1 or xgb_pred == 1) else 0


# ==============================
# 🚨 Delete Suspicious File
# ==============================
def delete_suspicious_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            msg = f"🗑️ Deleted suspicious file: {file_path}"
            print(msg)
            log_alert(msg)
    except Exception as e:
        print("Delete error:", e)


# ==============================
# Monitor Class
# ==============================
class RansomwareMonitor(FileSystemEventHandler):

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

                # 🚨 HIGH ENTROPY DETECTION
                if entropy > 7.5:
                    event_stats["high_entropy"] += 1

                    print(f"🚨 High entropy detected: {event.src_path}")

                    # 🔥 AUTO DELETE
                    delete_suspicious_file(event.src_path)

            except Exception:
                pass


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":

    path = "test_data/files"
    os.makedirs(path, exist_ok=True)

    observer = Observer()
    observer.schedule(RansomwareMonitor(), path, recursive=True)
    observer.start()

    print("🔍 Monitoring started...")

    start_time = time.time()

    try:
        while True:
            time.sleep(1)

            if time.time() - start_time >= TIME_WINDOW:

                print("\n📊 Feature Summary:", event_stats)

                features = [
                    event_stats["created"],
                    event_stats["modified"],
                    event_stats["deleted"],
                    event_stats["renamed"],
                    event_stats["high_entropy"]
                ]

                result = predict_ransomware(features)

                if result == 1:
                    alert_msg = "🚨 RANSOMWARE DETECTED!"
                    print(alert_msg)
                    log_alert(alert_msg)
                else:
                    print("✅ Normal behavior")

                # Save dataset
                os.makedirs("dataset", exist_ok=True)

                with open("dataset/ransomware_fs_features.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(features + [result])

                # Reset stats
                for key in event_stats:
                    event_stats[key] = 0

                start_time = time.time()

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("\n🛑 Monitoring stopped.")