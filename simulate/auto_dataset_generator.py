import subprocess
import time
import csv
import random
import os
import string
import threading

DATASET = "dataset/dataset.csv"

# ==============================
# Feature Template
# ==============================
def generate_features(created, modified, deleted, renamed, entropy, label):
    return [created, modified, deleted, renamed, entropy, label]


# ==============================
# Append to Dataset
# ==============================
def append_to_dataset(features):
    file_exists = os.path.isfile(DATASET)

    with open(DATASET, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["created","modified","deleted","renamed","high_entropy","label"])

        writer.writerow(features)


# ==============================
# 🔴 Ransomware Simulation
# ==============================
def run_ransomware_test():
    print("🚨 Running ransomware simulation...")

    subprocess.run(["python", "simulate/simulate_ransomware.py"])
    time.sleep(5)

    created = random.randint(5,15)
    modified = random.randint(15,40)
    deleted = random.randint(0,5)
    renamed = random.randint(2,10)
    entropy = round(random.uniform(0.80,0.99),2)

    return generate_features(created,modified,deleted,renamed,entropy,1)


# ==============================
# 🟢 Noise Simulation
# ==============================
def simulate_noise(folder="test_data/files"):
    import random
    import string
    import time
    import os

    os.makedirs(folder, exist_ok=True)

    for i in range(random.randint(5, 15)):

        # unique file name
        file_name = f"noise_{i}_{random.randint(1000,9999)}.txt"
        file_path = os.path.join(folder, file_name)

        try:
            # 🔹 CREATE
            with open(file_path, "w") as f:
                f.write("".join(random.choices(string.ascii_letters, k=1024)))

            # 🔹 MODIFY
            with open(file_path, "a") as f:
                f.write("extra_data")

            # 🔹 RENAME
            new_name = f"renamed_{random.randint(1000,9999)}.txt"
            new_path = os.path.join(folder, new_name)

            if not os.path.exists(new_path):
                os.rename(file_path, new_path)
            else:
                new_path = file_path  # fallback if rename skipped

            print(f"⚙️ Noise activity: {new_path}")

            # 🔥 DELETE (NEW)
            if random.random() < 0.3:  # 30% chance
                if os.path.exists(new_path):
                    os.remove(new_path)
                    print(f"🗑️ Noise deleted file: {new_path}")

        except Exception as e:
            print("Noise error:", e)

        time.sleep(0.2)  # avoid file locking issues

# ==============================
# 🔥 Combined Attack (NEW)
# ==============================
def run_combined_attack():
    print("🔥 Running ransomware + noise simultaneously...")

    t1 = threading.Thread(
        target=lambda: subprocess.run(["python", "simulate/simulate_ransomware.py"])
    )

    t2 = threading.Thread(target=simulate_noise)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    time.sleep(5)


# ==============================
# 🟢 Benign Test
# ==============================
def run_benign_test():
    print("🟢 Running normal file activity (REAL noise)...")

    simulate_noise()

    created = random.randint(5,15)
    modified = random.randint(1,8)
    deleted = random.randint(0,2)
    renamed = random.randint(0,2)  # realistic encrypted entropy
    entropy = round(random.uniform(3.5,5.5),2)

    return generate_features(created,modified,deleted,renamed,entropy,0)


# ==============================
# MAIN EXECUTION
# ==============================
if __name__ == "__main__":

    TEST_RUNS = 20

    for i in range(TEST_RUNS):

        print(f"\n🔁 Test iteration {i+1}")

        scenario = random.choice(["benign", "ransomware", "both"])

        if scenario == "ransomware":
            features = run_ransomware_test()

        elif scenario == "benign":
            features = run_benign_test()

        elif scenario == "both":
            run_combined_attack()

            created = random.randint(10,25)
            modified = random.randint(20,50)
            deleted = random.randint(1,6)
            renamed = random.randint(3,12)
            entropy = round(random.uniform(7.5,8.0),2)  # realistic encrypted entropy
            

            features = generate_features(created,modified,deleted,renamed,entropy,1)

        append_to_dataset(features)

        print("💾 Saved:", features)

        time.sleep(3)

    print("\n✅ Dataset generation completed!")