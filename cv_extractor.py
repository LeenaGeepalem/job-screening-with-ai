import fitz
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

#Example Usage
if __name__ == "__main__":
    extracted_text = extract_text_from_pdf(r"D:\Data Science\Hackathon\Job Description\[Usecase 5] AI-Powered Job Application Screening System\CVs1\C1061.pdf")
    print(extracted_text)