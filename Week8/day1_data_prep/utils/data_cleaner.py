import json
import random
import os
import statistics

# -----------------------------
# SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# GENERATE DATA
# -----------------------------
data = []

# 1. QA DATA
for i in range(400):
    data.append({
        "instruction": "Answer the finance question",
        "input": f"What is GST in case {i}?",
        "output": "GST is an indirect tax applied on goods and services."
    })

# 2. REASONING DATA
for i in range(300):
    amount = random.randint(100, 1000)
    gst = round(amount * 0.18, 2)
    total = round(amount + gst, 2)

    data.append({
        "instruction": "Solve the problem step by step",
        "input": f"If GST is 18% on ₹{amount}, what is total?",
        "output": f"GST = {gst}, Total = {total}"
    })

# 3. EXTRACTION DATA
for i in range(300):
    tax = random.randint(10, 500)

    data.append({
        "instruction": "Extract the tax amount from the sentence",
        "input": f"The GST applied is ₹{tax}",
        "output": f"{tax}"
    })

print(f"Total raw samples: {len(data)}")


# -----------------------------
# CLEANING
# -----------------------------
clean_data = []
seen = set()

for item in data:
    if not item["instruction"] or not item["input"] or not item["output"]:
        continue

    key = item["input"].strip()

    if key in seen:
        continue

    seen.add(key)
    clean_data.append(item)

print(f"Clean samples: {len(clean_data)}")


# -----------------------------
# TOKEN LENGTH ANALYSIS
# -----------------------------
lengths = []

for item in clean_data:
    length = len(item["instruction"].split()) + \
             len(item["input"].split()) + \
             len(item["output"].split())
    lengths.append(length)

avg_len = round(statistics.mean(lengths), 2)
min_len = min(lengths)
max_len = max(lengths)

print(f"Avg length: {avg_len}")
print(f"Min length: {min_len}")
print(f"Max length: {max_len}")


# -----------------------------
# REMOVE OUTLIERS
# -----------------------------
filtered_data = []

LOW = 5
HIGH = 60

for item, l in zip(clean_data, lengths):
    if l < LOW or l > HIGH:
        continue
    filtered_data.append(item)

print(f"After outlier removal: {len(filtered_data)}")


# -----------------------------
# TRAIN / VAL SPLIT
# -----------------------------
random.shuffle(filtered_data)

split_idx = int(0.8 * len(filtered_data))

train_data = filtered_data[:split_idx]
val_data = filtered_data[split_idx:]

print(f"Train samples: {len(train_data)}")
print(f"Validation samples: {len(val_data)}")


# -----------------------------
# SAVE FILES
# -----------------------------
train_path = os.path.join(DATA_DIR, "train.jsonl")
val_path = os.path.join(DATA_DIR, "val.jsonl")

with open(train_path, "w", encoding="utf-8") as f:
    for item in train_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

with open(val_path, "w", encoding="utf-8") as f:
    for item in val_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Files saved successfully!")


# -----------------------------
# SAVE ANALYSIS FILE
# -----------------------------
analysis_path = os.path.join(BASE_DIR, "../DATASET-ANALYSIS.md")

with open(analysis_path, "w") as f:
    f.write("# Dataset Analysis\n\n")
    f.write(f"Total Raw Samples: {len(data)}\n")
    f.write(f"Clean Samples: {len(clean_data)}\n")
    f.write(f"Final Samples: {len(filtered_data)}\n\n")

    f.write(f"Train Samples: {len(train_data)}\n")
    f.write(f"Validation Samples: {len(val_data)}\n\n")

    f.write(f"Average Token Length: {avg_len}\n")
    f.write(f"Min Length: {min_len}\n")
    f.write(f"Max Length: {max_len}\n\n")

    f.write("Data Types:\n")
    f.write("- QA: 400\n")
    f.write("- Reasoning: 300\n")
    f.write("- Extraction: 300\n")

print("Analysis file generated.")