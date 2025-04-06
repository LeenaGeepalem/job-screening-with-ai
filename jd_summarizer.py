import pandas as pd
import ollama

# Load CSV file (use raw string r"" to avoid escape sequence issues in Windows paths)
df = pd.read_csv(r"D:\Data Science\Hackathon\Job Description\[Usecase 5] AI-Powered Job Application Screening System\job_description.csv")

# Function to summarize job descriptions
def summarize_jd(job_description):
    prompt = f"Summarize the following job description, highlighting key responsibilities and qualifications:\n\n{job_description}"
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]  # FIXED: Wrapped in a list
    )
    return response['message']['content']

# Apply summarization to each job description
df["JD_Summary"] = df["Job Description"].apply(summarize_jd)

# Save the updated DataFrame
df.to_csv("jd_sum.csv", index=False)


print("✅ Summarization Done! Results saved to jd_sum.csv")
