import subprocess
import time
import csv
import random
import os

DATASET = "dataset/dataset.csv"

# feature template
def generate_features(created, modified, deleted, renamed, entropy, label):
    return [created, modified, deleted, renamed, entropy, label]


def append_to_dataset(features):
    file_exists = os.path.isfile(DATASET)

    with open(DATASET, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["created","modified","deleted","renamed","high_entropy","label"])

        writer.writerow(features)


def run_ransomware_test():
    print("Running ransomware simulation...")
    subprocess.run(["python", "simulate/simulate_ransomeware.py"])
    time.sleep(5)

    created = random.randint(5,15)
    modified = random.randint(15,40)
    deleted = random.randint(0,5)
    renamed = random.randint(2,10)
    entropy = round(random.uniform(0.80,0.99),2)

    return generate_features(created,modified,deleted,renamed,entropy,1)


def run_benign_test():
    print("Running normal file activity...")

    created = random.randint(5,15)
    modified = random.randint(1,8)
    deleted = random.randint(0,2)
    renamed = random.randint(0,2)
    entropy = round(random.uniform(0.50,0.70),2)

    return generate_features(created,modified,deleted,renamed,entropy,0)


if __name__ == "__main__":

    TEST_RUNS = 20

    for i in range(TEST_RUNS):

        print(f"\nTest iteration {i+1}")

        if random.choice([0,1]):
            features = run_ransomware_test()
        else:
            features = run_benign_test()

        append_to_dataset(features)

        print("Saved:", features)

        time.sleep(3)

    print("\nDataset generation completed!")