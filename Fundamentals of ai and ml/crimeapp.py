import pandas as pd

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("crime.csv")

# Show columns
print("\nColumns in dataset:", df.columns)

# -------------------------
# Take user input
# -------------------------
city_input = input("\nEnter state name: ").strip().lower()

# -------------------------
# Find correct column
# -------------------------
city_col = None
for col in df.columns:
    if "state" in col.lower() or "city" in col.lower():
        city_col = col   # ✅ FIXED
        break

if city_col is None:
    print("City/State column not found in dataset. Check column names above.")
    exit()

# -------------------------
# Filter data
# -------------------------
city_data = df[df[city_col].astype(str).str.lower() == city_input]

# -------------------------
# Output results
# -------------------------
if city_data.empty:
    print(f"\n❌ No data found for '{city_input}'")
else:
    print(f"\n📊 Crime Data for {city_input.title()}:\n")

    for i, row in city_data.iterrows():
        output_line = ""
        for col in df.columns:
            output_line += f"{col}: {row[col]} | "
        print(output_line)

    # -------------------------
    # Summary
    # -------------------------
    print("\n🔎 Summary:")

    for col in df.columns:
        if "crime" in col.lower() or "total" in col.lower():
            print(f"➡ {col}:", city_data[col].values)

    for col in df.columns:
        if "rate" in col.lower():
            print(f"➡ {col}:", city_data[col].values)