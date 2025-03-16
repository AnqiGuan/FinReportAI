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

# Summarize Financial Trends Using NLP
financial_text = f"""
This company's total assets grew from {df['Total Assets'].iloc[-1]:,} to {df['Total Assets'].iloc[0]:,}.
Total equity increased from {df['Total Equity'].iloc[-1]:,} to {df['Total Equity'].iloc[0]:,}.
Debt remained stable at {df['Total Debt'].iloc[0]:,}, while working capital fluctuated.
"""

# Use a Transformer-based model to summarize financial trends
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1) 
    summary_output = summarizer(financial_text, max_length=100, min_length=30, do_sample=False)
    print("\n📌 Financial Summary:\n", summary_output[0]["summary_text"])
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


save_path = "outputs/financial_analysis.png"  
plt.savefig(save_path)
plt.show()

print(f"\n✅ Visualization Complete! Check '{save_path}'")

# ✅ Print Buy/Sell Decisions
print("\n📌 Buy/Sell Decisions:")
print(df[["Date", "Signal"]])
