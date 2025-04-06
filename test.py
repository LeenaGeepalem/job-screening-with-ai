import ollama

def match_score(resume_text, job_desc):
    prompt = f"""
    Compare the resume text and job description.
    Resume:
    {resume_text}
    Job Description:
    {job_desc}

    - Provide a matching score between 0-100.
    - Highlight key matched skills and missing skills.
    - Structure the response in JSON format with keys: "Matching_score" and "Matched_skills".
    """

    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract the response text
        response_text = response.get("message", {}).get("content", "")

        # Attempt to parse the response if it's in JSON format
        import json
        try:
            parsed_response = json.loads(response_text)
            return parsed_response  # Expected to contain "Matching_score" and "Matched_skills"
        except json.JSONDecodeError:
            return {"error": "Failed to parse response as JSON", "raw_response": response_text}

    except Exception as e:
        return {"error": f"Error in matching: {str(e)}"}


# Example Usage
resume_text = """Email: deepchakumar321@gmail.com, deepak.2201109cs@iiitbh.ac.in
   Education:
      - Indian Institute of Information Technology Bhagalpur (2022–2026) - B.Tech. in Computer Science Engineering with CGPA: 7.72
      - Amar Memorial St. George’s Preparatory School, 12th (2021) - CBSE, Uttar Pradesh - Percentage: 80.8%
      - Amar Memorial St. George’s Preparatory School, 10th (2019) - CBSE, Uttar Pradesh - Percentage: 92%
   Technical Skills and Interests:
      - Programming Languages: C, C++, Python, SQL, HTML, CSS
      - Tools: VS Code, Jupyter Notebook, PyCharm, Git
      - Libraries/Frameworks: NumPy, Pandas, Scikit-Learn, TensorFlow, Keras, Flask, OpenCV
      - Databases: MySQL
      - Concepts: Data Structures, Algorithms, Machine Learning, Deep Learning, Neural Networks
      - Soft Skills: Analytical Thinking, Adaptability, Collaboration, Attention to Detail
      - Topics of Interest: Image Processing, Model Optimization, Artificial Intelligence
   Certifications:
      - Supervised Machine Learning (2024) - Coursera | Andrew Ng
      - Advanced Learning Algorithms (2024) - Coursera | Andrew Ng
      - Unsupervised Learning, Recommenders, Reinforcement Learning (2024) - Coursera | Andrew Ng
   Achievements:
      - Internal Smart India Hackathon Finalist (2024) - Secured 24th rank in the internal round
      - Solved 1150+ Coding Questions Across Multiple Platforms
         - LeetCode: 450+
         - GfG: 250+
         - CodeChef: 350+
      - Knight on LeetCode: Current rating of 1860, best global rank of 1754"""

job_desc = """The job description is for a Software Engineer position. Key responsibilities include:
- Designing, developing, testing, and maintaining software applications using clean, maintainable, and scalable code.
- Collaborating with cross-functional teams to define and implement features.
- Troubleshooting and debugging issues for optimal performance.
- Staying updated with emerging technologies and best practices.

Qualifications:
- Bachelor's degree in Computer Science or a related field.
- Proficiency in programming languages such as Python, Java, or C++.
- Experience with databases, web development, and software frameworks.
- Strong problem-solving skills, attention to detail, and ability to work independently and in a team environment."""

# Get match score
response = match_score(resume_text, job_desc)

# Print results
if "error" in response:
    print("Error:", response["error"])
else:
    print("Matching Score:", response.get("Matching_score", "N/A"))
    print("Matched Skills:", response.get("Matched_skills", "N/A"))