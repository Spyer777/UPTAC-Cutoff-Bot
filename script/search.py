import json
import re
import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("Data/clean_cutoff.csv")

# ==========================================
# NORMALIZE FUNCTION
# ==========================================

def normalize(text):
    text = str(text).lower()

    # Common replacements
    text = text.replace("&", "and")

    # Remove punctuation
    text = re.sub(r"[(),.-]", " ", text)

    # Remove extra spaces
    text = " ".join(text.split())

    return text

# ==========================================
# CREATE SEARCH COLUMN
# ==========================================

df["Search"] = df["Institute"].apply(normalize)

# ==========================================
# LOAD ALIAS
# ==========================================

try:
    with open("Data/alias.json", "r", encoding="utf-8") as f:
        aliases = json.load(f)
except:
    aliases = {}

# Normalize aliases too
aliases = {k.lower(): normalize(v) for k, v in aliases.items()}

# ==========================================
# USER INPUT
# ==========================================

print("=" * 50)
print("         UPTAC CUTOFF BOT")
print("=" * 50)

search = input("\nEnter College Name : ").strip().lower()

# Alias search
keyword = aliases.get(search, normalize(search))

print(f"\nSearching for : {keyword}")

# ==========================================
# SEARCH
# ==========================================

result = df[df["Search"].str.contains(keyword, na=False)]

# ==========================================
# NO RESULT
# ==========================================

if result.empty:

    print("\n❌ College Not Found")
    exit()

# ==========================================
# UNIQUE COLLEGES
# ==========================================

colleges = sorted(result["Institute"].drop_duplicates())

print(f"\n✅ {len(colleges)} College(s) Found\n")

for i, college in enumerate(colleges, start=1):
    print(f"{i}. {college}")

# ==========================================
# SELECT COLLEGE
# ==========================================

while True:

    try:

        choice = int(input("\nSelect College : "))

        if 1 <= choice <= len(colleges):
            break

        print("❌ Invalid Choice")

    except ValueError:

        print("❌ Enter a valid number")

selected_college = colleges[choice - 1]

print("\n" + "=" * 50)
print("Selected College")
print("=" * 50)

print(selected_college)

# ==========================================
# FILTER BY SELECTED COLLEGE
# ==========================================

college_data = df[df["Institute"] == selected_college]

# ==========================================
# QUOTA
# ==========================================

quotas = sorted(college_data["Quota"].dropna().unique())

print("\nAvailable Quota\n")

for i, quota in enumerate(quotas, 1):
    print(f"{i}. {quota}")

while True:
    try:
        q = int(input("\nSelect Quota : "))
        if 1 <= q <= len(quotas):
            break
        print("Invalid Choice")
    except:
        print("Enter Number")

selected_quota = quotas[q - 1]

college_data = college_data[college_data["Quota"] == selected_quota]

# ==========================================
# CATEGORY
# ==========================================

categories = sorted(college_data["Category"].dropna().unique())

print("\nAvailable Categories\n")

for i, cat in enumerate(categories, 1):
    print(f"{i}. {cat}")

while True:
    try:
        c = int(input("\nSelect Category : "))
        if 1 <= c <= len(categories):
            break
        print("Invalid Choice")
    except:
        print("Enter Number")

selected_category = categories[c - 1]

college_data = college_data[college_data["Category"] == selected_category]

# ==========================================
# SEAT GENDER
# ==========================================

genders = sorted(college_data["Seat Gender"].dropna().unique())

print("\nAvailable Seat Gender\n")

for i, gender in enumerate(genders, 1):
    print(f"{i}. {gender}")

while True:
    try:
        g = int(input("\nSelect Seat Gender : "))
        if 1 <= g <= len(genders):
            break
        print("Invalid Choice")
    except:
        print("Enter Number")

selected_gender = genders[g - 1]

college_data = college_data[college_data["Seat Gender"] == selected_gender]

# ==========================================
# SHOW ALL PROGRAMS
# ==========================================

programs = sorted(college_data["Program"].unique())

print("\n" + "=" * 70)
print(selected_college)
print("=" * 70)

for program in programs:

    print(f"\n📘 {program}")

    temp = college_data[college_data["Program"] == program]

    rounds = temp.sort_values("Round")

    for _, row in rounds.iterrows():

        print(
            f"{row['Round']:<10}  "
            f"Opening : {int(row['Opening Rank'])}   "
            f"Closing : {int(row['Closing Rank'])}"
        )

    print("-" * 70)