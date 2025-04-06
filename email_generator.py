import pandas as pd
import ollama
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load matching results
df_matches = pd.read_csv("matching_results.csv")

# Filter candidates with a matching score above 80
candidates_to_email = df_matches[df_matches["Matching Score"] > 80]


# Function to generate personalized email using Ollama
def generate_email_content(job_title, resume_text):
    prompt = f"""
    Generate a professional email informing the candidate that their resume matches the following job opportunity:

    Job Title: {job_title}

    Here is the resume content:
    {resume_text}

    The email should be professional and encourage the candidate to respond if interested.
    """

    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error generating email: {str(e)}"


# Send emails to qualified candidates
def send_email(to_email, email_body):
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"
    subject = "Job Opportunity Matching Your Profile"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(email_body, "plain"))

    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {str(e)}")


# Send emails
for _, candidate in candidates_to_email.iterrows():
    email_content = generate_email_content(candidate["Job Title"], candidate["Matching Result"])
    send_email(candidate["Email"], email_content)

print("✅ All qualified candidates have been notified via email.")