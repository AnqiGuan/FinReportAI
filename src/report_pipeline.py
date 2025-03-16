import pandas as pd
from llama_cpp import Llama

# Load and Summarize CSV Data
df = pd.read_csv("outputs/financial_data.csv")
summary = df.to_string(index=False)

# Construct the Prompt
prompt = (
    "You are a financial analyst. Analyze the following financial data and generate a comprehensive report that includes the following sections:\n"
    "1. Company Overview\n"
    "2. Financial Health Analysis\n"
    "3. Trend Analysis\n"
    "4. Key Financial Ratios and Metrics\n"
    f"{summary}\n\n"
    "Generate the report as bullet points or paragraphs without any extra greetings or questions or 'please'. If you do not know company name, just use 'This company'."
)

# Load the Model
llm = Llama.from_pretrained(
    repo_id="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
    filename="Meta-Llama-3-8B-Instruct.Q2_K.gguf",
    n_ctx=1024
)

# Generate the Report
analysis_report = llm(prompt, max_tokens=2048)

# Extract the generated text from the output dictionary
generated_text = analysis_report["choices"][0]["text"]

print("Generated Report:")
print(generated_text)

# Save the Report to a File
with open("outputs/analysis_report.txt", "w", encoding="utf-8") as f:
    f.write(generated_text)
