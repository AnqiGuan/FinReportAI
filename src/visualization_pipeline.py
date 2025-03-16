import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("outputs/financial_data.csv")

# Convert the Date column to datetime objects (format is MM/DD/YYYY)
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")

# Ensure the DataFrame is sorted by Date
df.sort_values("Date", inplace=True)

# Plot key financial metrics over time
plt.figure(figsize=(10, 6))
plt.plot(df["Date"], df["Total Assets"], marker="o", label="Total Assets")
plt.plot(df["Date"], df["Total Liabilities"], marker="o", label="Total Liabilities")
plt.plot(df["Date"], df["Total Equity"], marker="o", label="Total Equity")
plt.title("Financial Metrics Over Time")
plt.xlabel("Date")
plt.ylabel("Amount")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/financial_metrics_trend.png")
plt.show()

# Compute a financial ratio 
# Debt-to-Equity = Total Debt / Total Equity
df["Debt_to_Equity"] = df["Total Debt"] / df["Total Equity"]

plt.figure(figsize=(10, 6))
plt.plot(df["Date"], df["Debt_to_Equity"], marker="o", color="red", label="Debt-to-Equity Ratio")
plt.title("Debt-to-Equity Ratio Over Time")
plt.xlabel("Date")
plt.ylabel("Debt-to-Equity Ratio")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/debt_to_equity_trend.png")
plt.show()

# Save the updated DataFrame to a new CSV file
df.to_csv("outputs/financial_data_with_ratios.csv", index=False)
