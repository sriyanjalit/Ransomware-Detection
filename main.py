import time
import os
import numpy as np
import joblib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from features.entropy_calculator import calculate_entropy

# Load trained model
rf_model = joblib.load("ml/ransomware_model.pkl")

event_stats = {
    "created": 0,
    "deleted": 0,
    "modified": 0,
    "renamed": 0,
    "high_entropy": 0
}

TIME_WINDOW = 10


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
                if entropy > 7.5:
                    event_stats["high_entropy"] += 1
            except:
                pass


if __name__ == "__main__":

    path = input("Enter directory path to monitor: ")

    if not os.path.exists(path):
        print("Invalid directory!")
        exit()

    observer = Observer()
    observer.schedule(RealTimeMonitor(), path, recursive=True)
    observer.start()

    print("Monitoring started on:", path)

    start_time = time.time()

    try:
        while True:
            time.sleep(1)

            if time.time() - start_time >= TIME_WINDOW:

                print("\nActivity Summary:")
                print(event_stats)

                features = np.array([[
                    event_stats["created"],
                    event_stats["modified"],
                    event_stats["deleted"],
                    event_stats["renamed"],
                    event_stats["high_entropy"]
                ]])

                prediction = rf_model.predict(features)[0]

                if prediction == 1:
                    print("🚨 Ransomware Activity Detected!")
                else:
                    print("✅ Normal Activity")

                for key in event_stats:
                    event_stats[key] = 0

                start_time = time.time()

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("Monitoring stopped.")