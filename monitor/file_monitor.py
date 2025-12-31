from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import math
import os

# --------- Global Feature Counters -----------11
event_stats = {
    "created": 0,
    "deleted": 0,
    "modified": 0,
    "renamed": 0,
    "high_entropy": 0
}

START_TIME = time.time()
TIME_WINDOW = 10   # seconds


# --------- Entropy Calculation Function ----------
def calculate_entropy(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        if not data:
            return 0.0

        freq = {}
        for byte in data:
            freq[byte] = freq.get(byte, 0) + 1

        entropy = 0.0
        for count in freq.values():
            p = count / len(data)
            entropy -= p * math.log2(p)

        return entropy

    except Exception:
        return 0.0


# --------- File System Monitor ----------
class RansomwareMonitor(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            event_stats["created"] += 1
            print(f"[CREATED] {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            event_stats["deleted"] += 1
            print(f"[DELETED] {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            event_stats["renamed"] += 1
            print(f"[RENAMED] {event.src_path} -> {event.dest_path}")

    def on_modified(self, event):
        if not event.is_directory and os.path.isfile(event.src_path):
            event_stats["modified"] += 1
            entropy = calculate_entropy(event.src_path)

            print(f"[MODIFIED] {event.src_path} | Entropy: {entropy:.2f}")

            if entropy > 7.5:
                event_stats["high_entropy"] += 1
                print("🚨 High entropy write detected!")


# --------- Main Program ----------
if __name__ == "__main__":
    path = "test_folder"

    if not os.path.exists(path):
        print("❌ test_folder not found!")
        exit()

    event_handler = RansomwareMonitor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print("🔍 Monitoring started on test_folder...")

    try:
        while True:
            time.sleep(1)

            # ---- Time Window Analysis ----
            if time.time() - START_TIME >= TIME_WINDOW:
                print("\n📊 Feature Summary (Last 10 seconds)")
                print(event_stats)

                # ---- Rule-Based Detection ----
                if (
                    event_stats["modified"] > 10 and
                    event_stats["high_entropy"] > 3
                ):
                    print("🚨🚨 POSSIBLE RANSOMWARE ACTIVITY DETECTED 🚨🚨")

                # Reset counters
                for key in event_stats:
                    event_stats[key] = 0

                START_TIME = time.time()

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("\n🛑 Monitoring stopped.")
