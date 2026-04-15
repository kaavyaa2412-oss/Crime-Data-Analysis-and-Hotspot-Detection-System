import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from difflib import get_close_matches

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("crime.csv")

print("\nColumns in dataset:\n", df.columns)

# -------------------------
# Find State/City column
# -------------------------
city_col = None
for col in df.columns:
    if "state" in col.lower() or "city" in col.lower():
        city_col = col
        break

if city_col is None:
    print("City/State column not found.")
    exit()

# -------------------------
# AI Smart Input (Fuzzy Matching)
# -------------------------
user_input = input("\nEnter state/city name: ").strip().lower()

cities = df[city_col].astype(str).unique()
match = get_close_matches(user_input, cities, n=1)

if match:
    city_input = match[0]
    print(f"Interpreted as: {city_input}")
else:
    print("No close match found.")
    exit()

# -------------------------
# Filter Data
# -------------------------
city_data = df[df[city_col] == city_input]

if city_data.empty:
    print("No data found.")
    exit()

# -------------------------
# Display Data
# -------------------------
print(f"\n Crime Data for {city_input}:\n")
print(city_data.to_string(index=False))

# -------------------------
# FIX: Select Year Columns as Crime Data
# -------------------------
crime_cols = [col for col in df.columns if col.strip().isdigit()]

# -------------------------
# Summary
# -------------------------
print("\n Summary:")

if len(crime_cols) == 0:
    print(" No crime columns found.")
else:
    for col in crime_cols:
        total = city_data[col].sum()
        print(f" {col}: {total}")

# -------------------------
# ML: Prediction (Using Years)
# -------------------------
if len(crime_cols) >= 2:
    try:
        years = np.array([int(col) for col in crime_cols]).reshape(-1, 1)
        values = city_data[crime_cols].values.flatten()

        model = LinearRegression()
        model.fit(years, values)

        next_year = max(years)[0] + 1
        prediction = model.predict([[next_year]])

        print(f"\n Predicted crime for {next_year}: {prediction[0]:.2f}")
    except:
        print("Prediction not possible.")

# -------------------------
# ML: Clustering
# -------------------------
if len(crime_cols) >= 2:
    try:
        kmeans = KMeans(n_clusters=3, random_state=0)
        df["Crime_Level"] = kmeans.fit_predict(df[crime_cols])
        print("\n Crime Clustering Added (0=Low, 1=Medium, 2=High)")
    except:
        print("Clustering not possible.")

# -------------------------
# Insights
# -------------------------
if len(crime_cols) > 0:
    total_crime = df[crime_cols].sum(axis=1)

    most_dangerous = df.loc[total_crime.idxmax()]
    print(f"\nMost Dangerous Area: {most_dangerous[city_col]}")

# -------------------------
# Visualization (FIXED)
# -------------------------
try:
    if len(crime_cols) > 0:
        crime_sum = city_data[crime_cols].sum()

        crime_sum.plot(kind='bar')
        plt.title(f"Crime Trend for {city_input}")
        plt.xlabel("Year")
        plt.ylabel("Total Crimes")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No data to plot.")
except:
    print("Visualization error.")

# -------------------------
# Query System (FIXED)
# -------------------------
query = input("\n Ask something (highest / lowest): ").lower()

if len(crime_cols) == 0:
    print(" No data available for query.")

else:
    total_crime = df[crime_cols].sum(axis=1)

    if "highest" in query:
        highest = df.loc[total_crime.idxmax()]
        print(f" Highest crime in: {highest[city_col]}")

    elif "lowest" in query:
        lowest = df.loc[total_crime.idxmin()]
        print(f" Lowest crime in: {lowest[city_col]}")

    else:
        print("Query not understood.")