import pandas as pd
from gpt4all import GPT4All

# Load and Summarize CSV Data
df = pd.read_csv("outputs/financial_data.csv")

summary = df.to_string(index=False)

# Step 2: Construct the Prompt
prompt = (
    "You are a financial analyst. Based on the following financial data, please provide a detailed analysis "
    "of the company's financial health, trends, and any potential concerns:\n\n"
    f"{summary}\n\n"
    "Please generate a comprehensive report with bullet points and a final summary."
)

# Load the GPT4All Model and Generate the Report
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

with model.chat_session():
    analysis_report = model.generate(prompt, max_tokens=1024)
    print("Generated Report:")
    print(analysis_report)

# Step 4: Save the Report to a File
with open("outputs/analysis_report.txt", "w", encoding="utf-8") as f:
    f.write(analysis_report)
