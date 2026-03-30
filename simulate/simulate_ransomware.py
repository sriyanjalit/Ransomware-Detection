import os
import time

TARGET_DIR = "test_data/files"

def generate_high_entropy_data(size=1024):
    """Generate random bytes to simulate encrypted data"""
    return os.urandom(size)

def simulate_ransomware():
    if not os.path.exists(TARGET_DIR):
        print("❌ Target folder not found!")
        return

    files = os.listdir(TARGET_DIR)

    if not files:
        print("⚠️ No files found to encrypt.")
        return

    for file in files:
        # ❌ Skip hidden/system files (.gitkeep, etc.)
        if file.startswith("."):
            continue

        # ❌ Skip already encrypted files
        if file.endswith(".encrypted"):
            continue

        old_path = os.path.join(TARGET_DIR, file)

        if os.path.isfile(old_path):
            try:
                # 🔐 Overwrite with high entropy data
                with open(old_path, "wb") as f:
                    f.write(generate_high_entropy_data())

                # 🔄 Rename file to simulate ransomware behavior
                new_path = old_path + ".encrypted"
                os.rename(old_path, new_path)

                print(f"🔒 Encrypted & Renamed: {file} → {os.path.basename(new_path)}")

                # ⏱ Small delay to simulate real attack speed
                time.sleep(0.05)

            except Exception as e:
                print(f"❌ Error processing {file}: {e}")

    print("✅ Simulation complete.")

def create_test_files(n=10):
    """Create normal test files (run once before simulation)"""
    os.makedirs(TARGET_DIR, exist_ok=True)

    for i in range(n):
        path = os.path.join(TARGET_DIR, f"file_{i}.txt")
        with open(path, "w") as f:
            f.write("This is normal file content.\n" * 20)

    print(f"📄 {n} test files created.")

if __name__ == "__main__":
    print("🚨 Starting ransomware simulation...")

    # Step 1: Create files if folder is empty
    if len(os.listdir(TARGET_DIR)) <= 1:  # only .gitkeep exists
        create_test_files()

    # Step 2: Run simulation
    simulate_ransomware()