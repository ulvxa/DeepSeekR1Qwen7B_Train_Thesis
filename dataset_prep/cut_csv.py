import csv
import sys

input_file = "train.csv"
output_file = "train_small.csv"

with open(input_file, "r", encoding="utf-8") as f:
    total_lines = sum(1 for _ in f) - 1 # - header

target_rows = total_lines // 3
print(f"Total rows: {total_lines}, keeping: {target_rows}")

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8", newline="") as fout:
    reader = csv.reader(fin)
    writer = csv.writer(fout)
    writer.writerow(next(reader))  # header
    for i, row in enumerate(reader):
        if i >= target_rows:
            break
        writer.writerow(row)

print(f"Done. Output: {output_file}")
