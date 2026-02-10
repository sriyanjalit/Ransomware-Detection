import time
import os
import numpy as np
import joblib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from features.entropy_calculator import calculate_entropy

# -------- Load Trained XGBoost Model --------
model = joblib.load("ml/xgboost_ransomware_model.pkl")

# -------- Feature Counters --------
event_stats = {
    "created": 0,
    "deleted": 0,
    "modified": 0,
    "renamed": 0,
    "high_entropy": 0
}

TIME_WINDOW = 10  # seconds


# -------- Monitor Class --------
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
            entropy = calculate_entropy(event.src_path)

            if entropy > 7.5:
                event_stats["high_entropy"] += 1


# -------- Main Execution --------
if __name__ == "__main__":

    path = input("📂 Enter directory path to monitor: ")

    if not os.path.exists(path):
        print("❌ Invalid directory!")
        exit()

    observer = Observer()
    observer.schedule(RealTimeMonitor(), path, recursive=True)
    observer.start()

    print(f"\n🔍 Monitoring started on: {path}")
    start_time = time.time()

    try:
        while True:
            time.sleep(1)

            if time.time() - start_time >= TIME_WINDOW:

                print("\n📊 Activity Summary (Last 10 sec):")
                print(event_stats)

                # Convert features to numpy array
                features = np.array([[
                    event_stats["created"],
                    event_stats["modified"],
                    event_stats["deleted"],
                    event_stats["renamed"],
                    event_stats["high_entropy"]
                ]])

                prediction = model.predict(features)

                if prediction[0] == 1:
                    print("🚨🚨 RANSOMWARE DETECTED 🚨🚨")
                else:
                    print("✅ Normal Behavior")

                # Reset counters
                for key in event_stats:
                    event_stats[key] = 0

                start_time = time.time()

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("\n🛑 Monitoring stopped.")
