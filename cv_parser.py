import os
import pandas as pd
import ollama
from cv_extractor import extract_text_from_pdf

# Function to extract structured data from a resume
def extract_candidate_data(resume_text):
    prompt = f"""
    Extract structured details from this resume text:

    {resume_text}

    Format output as:
    Email:
    Education:
    Experience:
    Skills:
    Certifications:
    """
    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error extracting data: {str(e)}"

# Process multiple CVs
cv_folder = r"D:\Data Science\Hackathon\CV_Testing"
cvs = [os.path.join(cv_folder, f) for f in os.listdir(cv_folder) if f.endswith(".pdf")]

results = []
for cv_path in cvs:
    print(f"Processing: {cv_path}")
    resume_text = extract_text_from_pdf(cv_path)
    extracted_info = extract_candidate_data(resume_text)
    results.append({"CV": os.path.basename(cv_path), "Extracted Info": extracted_info})

# Save results
df = pd.DataFrame(results)
df.to_csv("extracted_cv_data.csv", index=False)
print("✅ CV Processing Done! Results saved to extracted_cv_data.csv")