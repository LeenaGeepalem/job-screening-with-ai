import pandas as pd
import ollama
import concurrent.futures  # For parallel execution

# Load extracted CV data
df_cv = pd.read_csv("extracted_cv_data.csv")
df_jd = pd.read_csv(r"D:\Data Science\Hackathon\jd_sum.csv")


# Function to match resumes with job descriptions
def match_resume_with_jd(resume_text, job_description):
    prompt = f"""
    Compare the following resume text and job description:

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Provide a matching score (0-100) and highlight key matched & missing skills.
    """
    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error in matching: {str(e)}"


# Function to process a single resume-job pair
def process_match(cv_row, jd_row):
    resume_text = cv_row["Extracted Info"]
    match_result = match_resume_with_jd(resume_text, jd_row["Job Description"])

    # Extract match score (default to 0 if extraction fails)
    try:
        score = int(''.join(filter(str.isdigit, match_result.split("Matching Score:")[-1].split()[0])))
    except:
        score = 0

    if score > 80:  # Only keep high-scoring matches
        return {
            "CV": cv_row["CV"],
            "Job Title": jd_row["Job Title"],
            "Matching Score": score,
            "Matching Result": match_result
        }
    return None


# Perform matching in parallel
df_matches = []
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # Run 4 parallel threads
    futures = []
    for _, cv_row in df_cv.iterrows():
        for _, jd_row in df_jd.iterrows():
            futures.append(executor.submit(process_match, cv_row, jd_row))

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            df_matches.append(result)

# Save filtered matching results
if df_matches:
    pd.DataFrame(df_matches).to_csv("matching_results_filtered.csv", index=False)
    print("✅ Matching Done! Results saved to matching_results_filtered.csv")
else:
    print("❌ No candidates matched above 80%.")