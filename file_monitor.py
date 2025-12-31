from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import math
import os

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
            print(f"[CREATED] {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[DELETED] {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"[RENAMED] {event.src_path} -> {event.dest_path}")

    def on_modified(self, event):
        if not event.is_directory and os.path.isfile(event.src_path):
            entropy = calculate_entropy(event.src_path)
            print(f"[MODIFIED] {event.src_path} | Entropy: {entropy:.2f}")

            if entropy > 7.5:
                print("🚨 POSSIBLE RANSOMWARE DETECTED (High Entropy)!")


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
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
