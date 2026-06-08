from career_advisor import main as career_advisor
import requests
import os
from dotenv import load_dotenv
from groq import Groq

# 🔐 Load ENV
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🔗 Groq client
client = Groq(api_key=GROQ_API_KEY)


# 🎯 STEP 1: Input
def get_user_input():
    print("\n🎯 JOB MARKET ANALYZER\n")

    role = input("Enter job role (e.g., Data Scientist): ").strip()
    location = input("Enter location (e.g., Chennai): ").strip()
    num_jobs = int(input("Number of jobs (5 / 10 / 20): ").strip())

    return role, location, num_jobs


# 🔌 STEP 2: Fetch Jobs
def fetch_jobs(role, location, num_jobs):

    query = f"{role} in {location}"
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    pages = max(1, num_jobs // 10)
    all_jobs = []

    for page in range(1, pages + 1):
        params = {
            "query": query,
            "page": str(page),
            "num_pages": "1"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print("❌ API Error:", response.text)
            return []

        data = response.json()

        for job in data.get("data", []):
            all_jobs.append({
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "description": job.get("job_description"),
                "link": job.get("job_apply_link"),
                "location": job.get("job_city")
            })

    return all_jobs[:num_jobs]


# 🧠 STEP 3: Market Analysis
def analyze_market(jobs):

    combined_text = ""

    for job in jobs[:5]:
        combined_text += f"""
        Job Title: {job['title']}
        Description: {job['description']}
        """

    prompt = f"""
    You are a professional Job Market Analyzer AI.

    Analyze and provide:

    1. Role Overview
    2. Top Skills Required (8-10)
    3. Market Trends
    4. Salary Insight

    Keep it clean and structured.

    Job Data:
    {combined_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


# 📊 STEP 4: Display
def display_results(jobs, analysis):

    print("\n" + "="*60)
    print("📊 MARKET ANALYSIS")
    print("="*60 + "\n")

    print(analysis)

    print("\n" + "="*60)
    print("💼 JOB LISTINGS")
    print("="*60 + "\n")

    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']} – {job['company']}")
        print(f"   📍 Location: {job['location']}")
        print(f"   🔗 Apply: {job['link']}\n")

        print("   📄 Job Description:\n")

        desc = job["description"] or "No description available"

        print(desc[:1000])

        if len(desc) > 1000:
            print("\n   ...[Description truncated]\n")

        print("-" * 60)


# 🚀 MAIN CONTROLLER
def main():

    role, location, num_jobs = get_user_input()

    print("\n🔍 Fetching jobs...\n")
    jobs = fetch_jobs(role, location, num_jobs)

    if not jobs:
        print("❌ No jobs found.")
        return

    print("🧠 Analyzing market...\n")
    analysis = analyze_market(jobs)

    display_results(jobs, analysis)

    # 🔥 AGENT 2 CALL
    print("\n🚀 Launching Career Advisor...\n")
    career_advisor(jobs)


# ▶ RUN
if __name__ == "__main__":
    main()