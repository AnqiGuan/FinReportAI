import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
import numpy as np

# Load Financial Data
file_path = "outputs/financial_data.csv"  

try:
    df = pd.read_csv(file_path)
    print("✅ File loaded successfully!\n")
except FileNotFoundError:
    print(f"❌ Error: File not found at {file_path}")
    exit()

df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
df.sort_values("Date", inplace=True)

# Summarize Financial Trends Using NLP
financial_text = f"""
This company's total assets grew from {df['Total Assets'].iloc[-1]:,} to {df['Total Assets'].iloc[0]:,}.
Total equity increased from {df['Total Equity'].iloc[-1]:,} to {df['Total Equity'].iloc[0]:,}.
Debt remained stable at {df['Total Debt'].iloc[0]:,}, while working capital fluctuated.
"""

# Use a Transformer-based model to summarize financial trends
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # Force CPU
    summary_output = summarizer(financial_text, max_length=100, min_length=30, do_sample=False)
    financial_summary = summary_output[0]["summary_text"]
    print("\n📌 Financial Summary:\n", financial_summary)
except Exception as e:
    print("❌ Error: Unable to load NLP model. Check installation.")
    print(e)
    exit()

# Generate Buy/Sell Signals
df["Stock Price Change"] = df["Total Equity"].diff()
df["Signal"] = np.where(df["Stock Price Change"] > 0, "BUY", "SELL")

# Data Visualization
plt.figure(figsize=(12, 6))
sns.lineplot(x=df["Date"], y=df["Total Assets"], label="Total Assets", marker="o")
sns.lineplot(x=df["Date"], y=df["Total Equity"], label="Total Equity", marker="s")
sns.lineplot(x=df["Date"], y=df["Total Debt"], label="Total Debt", marker="^")

# Highlight Buy/Sell Signals
for i, row in df.iterrows():
    if row["Signal"] == "BUY":
        plt.scatter(row["Date"], row["Total Equity"], color="green", marker="^", s=100, label="BUY" if i == 0 else "")
    else:
        plt.scatter(row["Date"], row["Total Equity"], color="red", marker="v", s=100, label="SELL" if i == 0 else "")

plt.title("Financial Data Over Time")
plt.xlabel("Date")
plt.ylabel("Value (in Billions)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
save_path = "outputs/financial_analysis.png"  
plt.savefig(save_path)
plt.show()

print(f"\n✅ Visualization Complete! Check '{save_path}'")

# Print Buy/Sell Decisions
buy_sell_decisions = df[["Date", "Signal"]].to_string(index=False)
print("\n📌 Buy/Sell Decisions:")
print(buy_sell_decisions)

# Write final report (summary + buy/sell decisions) to a text file in outputs
final_report_path = "outputs/advice_report.txt"
with open(final_report_path, "w", encoding="utf-8") as f:
    f.write("Financial Summary:\n")
    f.write(financial_summary + "\n\n")
    f.write("Buy/Sell Decisions:\n")
    f.write(buy_sell_decisions + "\n")

print(f"\n✅ Final report saved to '{final_report_path}'")
