import pandas as pd
import os
import re

INPUT_FILE = "Data/cutoff.csv"
OUTPUT_FILE = "Data/clean_cutoff.csv"

print("Loading CSV...")

df = pd.read_csv(INPUT_FILE)

# -----------------------------
# Clean Column Names
# -----------------------------
df.columns = (
    df.columns
      .str.replace("▲▼", "", regex=False)
      .str.strip()
)

print("Columns:")
print(df.columns.tolist())

# -----------------------------
# Remove Empty Rows
# -----------------------------
df.dropna(how="all", inplace=True)

# -----------------------------
# Remove Duplicates
# -----------------------------
df.drop_duplicates(inplace=True)

# -----------------------------
# Remove Extra Spaces
# -----------------------------
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# -----------------------------
# Convert Rank Columns
# -----------------------------
df["Opening Rank"] = pd.to_numeric(df["Opening Rank"], errors="coerce")
df["Closing Rank"] = pd.to_numeric(df["Closing Rank"], errors="coerce")

# -----------------------------
# Save Clean CSV
# -----------------------------
os.makedirs("Data", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n✅ Cleaning Completed")
print("Total Records:", len(df))
print("Saved:", OUTPUT_FILE)