import os
from dotenv import load_dotenv
from groq import Groq

# 🔐 Load ENV
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


# 📄 Load Resume
def load_resume(file_path="resume.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        print("❌ Resume file not found.")
        return None


# 📊 Extract Job Descriptions (from Agent 1 output)
def extract_job_descriptions(jobs):
    combined = ""

    for job in jobs[:5]:  # limit
        combined += f"""
        Job Role: {job['title']}
        Description: {job['description']}
        """

    return combined


# 🧠 Career Advisor Agent
def career_advice(resume_text, job_text):

    prompt = f"""
Compare resume with job market and return ONLY:

• Top 5 Missing Skills
• 5 Things to Learn
• 3-Step Roadmap
• 3 Resume Improvements

Rules:
- Bullet points only
- No paragraphs
- Keep it short and crisp

Resume:
{resume_text}

Jobs:
{job_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content


# 🚀 MAIN
def main(jobs):

    print("\n📄 Loading resume...\n")
    resume_text = load_resume()

    if not resume_text:
        return

    print("🧠 Analyzing career path...\n")

    job_text = extract_job_descriptions(jobs)

    advice = career_advice(resume_text, job_text)

    print("\n" + "="*60)
    print("🎯 CAREER ADVISOR OUTPUT")
    print("="*60 + "\n")

    print(advice)


# 🔗 This allows connection with Agent 1
if __name__ == "__main__":
    print("⚠️ This file should be called from Agent 1")