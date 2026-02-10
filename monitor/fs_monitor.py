from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from features.entropy_calculator import calculate_entropy

import time
import os
import csv

event_stats = {
    "created": 0,
    "deleted": 0,
    "modified": 0,
    "renamed": 0,
    "high_entropy": 0
}

TIME_WINDOW = 10


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
            entropy = calculate_entropy(event.src_path)

            if entropy > 7.5:
                event_stats["high_entropy"] += 1


if __name__ == "__main__":

    path = "test_data/files"

    if not os.path.exists(path):
        print("❌ test_data/files not found!")
        exit()

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

                # Save to dataset
                with open("dataset/ransomware_fs_features.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        event_stats["created"],
                        event_stats["modified"],
                        event_stats["deleted"],
                        event_stats["renamed"],
                        event_stats["high_entropy"],
                        0  # change manually to 1 during simulation
                    ])

                # Reset
                for key in event_stats:
                    event_stats[key] = 0

                start_time = time.time()

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("\n🛑 Monitoring stopped.")
