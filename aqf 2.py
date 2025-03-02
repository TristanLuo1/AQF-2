import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define file path
file_path = "data"

# Define column widths based on dataset description
column_widths = [3, 1, 2, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]

# Define column names
column_names = [
    "STATE-CODE", "DIVISION-NUMBER", "ELEMENT-CODE", "YEAR",
    "JAN-VALUE", "FEB-VALUE", "MAR-VALUE", "APR-VALUE", "MAY-VALUE",
    "JUNE-VALUE", "JULY-VALUE", "AUG-VALUE", "SEPT-VALUE", "OCT-VALUE",
    "NOV-VALUE", "DEC-VALUE"
]

# Read dataset
df = pd.read_fwf(file_path, widths=column_widths, names=column_names, header=None)

# Convert numeric columns properly
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")

# Filter for Washington
washington_state_code = "045"  # Confirmed state code
df["STATE-CODE"] = df["STATE-CODE"].astype(str).str.zfill(3)
df = df[df["STATE-CODE"] == washington_state_code]

# Print unique years for debugging
print("Unique years in dataset:", df["YEAR"].unique())

# Exclude years beyond 2022
df = df[df["YEAR"] < 2023]  # Ensure 2025 does not affect calculations

# Replace -9999 values with NaN, then fill missing values using rolling mean
df.replace(-9999, np.nan, inplace=True)
df.fillna(df.rolling(5, min_periods=1).mean(), inplace=True)

# Compute winter accumulative HDD
df["WINTER-YEAR"] = df["YEAR"] + 1
df["WINTER-HDD"] = df["NOV-VALUE"] + df["DEC-VALUE"] + df["JAN-VALUE"].shift(-1) + df["FEB-VALUE"].shift(-1) + df["MAR-VALUE"].shift(-1)

# Drop NaN values introduced by shifting
df = df.dropna(subset=["WINTER-HDD"])

# Save to Excel
df[["WINTER-YEAR", "WINTER-HDD"]].to_excel("Winter_HDD_Washington_1895_2022.xlsx", index=False)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df["WINTER-YEAR"], df["WINTER-HDD"], marker="o", linestyle="-", color="b", label="Winter HDD")

# Fit a trendline
z = np.polyfit(df["WINTER-YEAR"], df["WINTER-HDD"], 1)
p = np.poly1d(z)
plt.plot(df["WINTER-YEAR"], p(df["WINTER-YEAR"]), "r--", label="Trend Line")

plt.xlabel("Year")
plt.ylabel("Winter Accumulative HDD")
plt.title("Trend of Winter HDD in Washington (1895 - 2022)")
plt.legend()
plt.grid()
plt.show()


# Analyze trend
trend_slope = z[0]
if trend_slope < 0:
    print("HDD is decreasing over the past century, indicating warming winters.")
elif trend_slope > 0:
    print("HDD is increasing over the past century, indicating colder winters.")
else:
    print("HDD trend is relatively flat over the past century.")


