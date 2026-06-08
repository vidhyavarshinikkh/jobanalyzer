import streamlit as st
import requests
from groq import Groq
from PyPDF2 import PdfReader

# ── API KEYS ──────────────────────────────────────────
GROQ_API_KEY   = "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"
ADZUNA_APP_ID  = "0083ad37"
ADZUNA_APP_KEY = "75984c5939f804550b0532390a4a86c1"

client = Groq(api_key=GROQ_API_KEY)

# ── PAGE CONFIG ───────────────────────────────────────
st.set_page_config(page_title="CareerLens", page_icon="🔭", layout="wide")

# ── INJECT CSS ────────────────────────────────────────
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');

html, body, .stApp {
    background-color: #060b18 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1080px !important;
}

/* Hide default streamlit header */
header[data-testid="stHeader"] { display: none !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background-color: #0b1120 !important;
    border-right: 1px solid #1a2540 !important;
    min-width: 240px !important;
    max-width: 240px !important;
}
section[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
    font-family: 'DM Sans', sans-serif !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f0f4ff !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── TEXT ── */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    color: #f0f4ff !important;
}
p, span, div, li {
    color: #94a3b8 !important;
    font-family: 'DM Sans', sans-serif !important;
}
label {
    color: #475569 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
}
a { color: #06b6d4 !important; }

/* ── INPUTS ── */
.stTextInput > div > div > input {
    background-color: #0f1829 !important;
    color: #f0f4ff !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 10px !important;
    padding: 11px 15px !important;
    font-size: 15px !important;
    font-family: 'DM Sans', sans-serif !important;
    caret-color: #06b6d4;
}
.stTextInput > div > div > input:focus {
    border-color: #06b6d4 !important;
    box-shadow: 0 0 0 2px rgba(6,182,212,0.12) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #2a3a52 !important;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background-color: #0f1829 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 10px !important;
    color: #f0f4ff !important;
}
.stSelectbox svg { fill: #475569 !important; }

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background-color: #0f1829 !important;
    border: 1.5px dashed #1e2d45 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
}
[data-testid="stFileUploader"] * { color: #475569 !important; }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #06b6d4, #2563eb) !important;
    color: #060b18 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    border: none !important;
    border-radius: 12px !important;
    height: 50px !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(6,182,212,0.2) !important;
    transition: all 0.2s !important;
    letter-spacing: 0.03em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(6,182,212,0.35) !important;
}
/* button always enabled - validation done in Python */

/* ── ALERTS ── */
.stSuccess > div {
    background-color: rgba(16,185,129,0.08) !important;
    border: 1px solid rgba(16,185,129,0.25) !important;
    border-radius: 10px !important;
    color: #6ee7b7 !important;
}
.stInfo > div {
    background-color: rgba(6,182,212,0.07) !important;
    border: 1px solid rgba(6,182,212,0.2) !important;
    border-radius: 10px !important;
    color: #67e8f9 !important;
}
.stWarning > div {
    background-color: rgba(245,158,11,0.08) !important;
    border: 1px solid rgba(245,158,11,0.2) !important;
    border-radius: 10px !important;
}
.stError > div {
    background-color: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.2) !important;
    border-radius: 10px !important;
}

/* ── EXPANDERS ── */
[data-testid="stExpander"] {
    background-color: #0d1525 !important;
    border: 1px solid #1a2540 !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(6,182,212,0.4) !important;
}

/* Remove injected "card" prefix ghost text */
[data-testid="stExpander"] details summary::before,
[data-testid="stExpander"] details summary::after {
    display: none !important;
    content: none !important;
}
[data-testid="stExpander"] details summary::-webkit-details-marker {
    display: none !important;
}

/* Summary row layout */
[data-testid="stExpander"] details summary {
    display: flex !important;
    align-items: center !important;
    list-style: none !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    padding: 14px 18px !important;
    cursor: pointer !important;
    gap: 8px !important;
}
[data-testid="stExpander"] details summary:hover {
    color: #06b6d4 !important;
}
[data-testid="stExpander"] details summary svg {
    color: #475569 !important;
    flex-shrink: 0 !important;
    margin-left: auto !important;
}

/* Content text */
[data-testid="stExpander"] p,
[data-testid="stExpander"] span,
[data-testid="stExpander"] li {
    color: #94a3b8 !important;
    font-size: 14px !important;
}

/* ── METRIC CARDS (using st.metric) ── */
[data-testid="stMetric"] {
    background-color: #0d1525 !important;
    border: 1px solid #1a2540 !important;
    border-radius: 12px !important;
    padding: 18px 16px !important;
    text-align: center !important;
}
[data-testid="stMetricValue"] {
    color: #06b6d4 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}
[data-testid="stMetricLabel"] {
    color: #334155 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ── DIVIDER ── */
hr {
    border: none !important;
    border-top: 1px solid #1a2540 !important;
    margin: 18px 0 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #060b18; }
::-webkit-scrollbar-thumb { background: #1a2540; border-radius: 999px; }

/* ── MARKDOWN TEXT COLOR FIX ── */
.stMarkdown p { color: #94a3b8 !important; }
.stMarkdown li { color: #94a3b8 !important; }
.stMarkdown h3 { color: #f0f4ff !important; font-family: 'Syne', sans-serif !important; }
.stMarkdown strong { color: #06b6d4 !important; }
.stMarkdown code {
    background: #0f1829 !important;
    color: #06b6d4 !important;
    border-radius: 4px !important;
    padding: 1px 6px !important;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔭 CareerLens")
    st.markdown("---")
    st.markdown("### What you'll get:")
    st.markdown("""
**📊 Market Insights**
Top skills, trends & salary data from live job listings

**🚨 Skill Gap Report**
Skills missing from your resume vs the market

**📚 Learning Plan**
Exactly what to learn next, in order

**🗺 3-Month Roadmap**
Month-by-month action plan tailored to you

**✅ Resume Improvements**
Specific fixes to make your resume stand out

**💼 Live Job Listings**
Real jobs matching your role & city right now
""")
    st.markdown("---")
    st.caption("Powered by Adzuna + Groq LLaMA 3.3")

# ── HERO ──────────────────────────────────────────────
st.markdown("## 🔭 Job Market Analyzer & Career Advisor")
st.markdown("Enter any job role & city — get live jobs, skill gap analysis, and a personalized roadmap.")
st.markdown("---")

# ── HELPER FUNCTIONS ──────────────────────────────────
def extract_resume(file):
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            return "".join(p.extract_text() or "" for p in reader.pages)
        return file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        st.error(f"Resume read error: {e}")
        return ""

def fetch_jobs(role, location, num_jobs, country_code):
    url = (
        f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
        f"?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
        f"&results_per_page={num_jobs}"
        f"&what={requests.utils.quote(role)}"
        f"&where={requests.utils.quote(location)}"
    )
    try:
        resp = requests.get(url, timeout=12)
        if resp.status_code != 200:
            st.error(f"Adzuna error {resp.status_code}: {resp.text[:200]}")
            return []
        jobs = []
        for j in resp.json().get("results", []):
            s_min = j.get("salary_min")
            s_max = j.get("salary_max")
            sym = "₹" if country_code == "in" else "$"
            salary = (
                f"{sym}{int(s_min):,} – {sym}{int(s_max):,}" if s_min and s_max
                else (f"{sym}{int(s_min):,}+" if s_min else "")
            )
            jobs.append({
                "title":    j.get("title", "N/A"),
                "company":  j.get("company", {}).get("display_name", "N/A"),
                "location": j.get("location", {}).get("display_name", "N/A"),
                "salary":   salary,
                "category": j.get("category", {}).get("label", ""),
                "desc":     j.get("description", ""),
                "link":     j.get("redirect_url", ""),
                "date":     j.get("created", "")[:10],
            })
        return jobs
    except Exception as e:
        st.error(f"Network error: {e}")
        return []

def market_analysis(jobs, role, location):
    data = "\n".join(f"Title:{j['title']}\nDesc:{j['desc'][:300]}" for j in jobs[:8])
    prompt = f"""Analyze these {role} job listings in {location}. Reply with bullet points only.

### 🛠 Top Skills Required
• skill
• skill
• skill
• skill
• skill

### 📈 Market Trends
• trend
• trend
• trend

### 💰 Salary Insight
• observation

### 🔥 Demand Level
• Hot/Moderate/Slow — reason

Job data:
{data}"""
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3, max_tokens=500
    )
    return r.choices[0].message.content

def career_roadmap(resume, jobs, role):
    jdata = "\n".join(f"Title:{j['title']}\nDesc:{j['desc'][:300]}" for j in jobs[:6])
    prompt = f"""Compare this resume with {role} job listings. Reply with bullet points only.

### 🚨 Top 5 Missing Skills
• gap
• gap
• gap
• gap
• gap

### 📚 What to Learn Next
• topic
• topic
• topic

### 🗺 3-Month Roadmap
• Month 1: goal
• Month 2: goal
• Month 3: goal

### ✏️ Resume Improvements
• fix
• fix
• fix

### ✅ Your Strengths
• strength
• strength
• strength

Resume:
{resume[:2500]}

Jobs:
{jdata}"""
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4, max_tokens=700
    )
    return r.choices[0].message.content

# ── INPUTS ────────────────────────────────────────────
c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
with c1:
    role = st.text_input("Job Role", placeholder="e.g. Data Scientist, DevOps Engineer")
with c2:
    location = st.text_input("City", placeholder="e.g. Bangalore, Chennai, Mumbai")
with c3:
    num_jobs = st.selectbox("Results", [5, 10, 15, 20], index=1)
with c4:
    country_map = {"India": "in", "UK": "gb", "USA": "us", "Australia": "au", "Canada": "ca"}
    country = st.selectbox("Country", list(country_map.keys()))
    country_code = country_map[country]

st.markdown("<br>", unsafe_allow_html=True)
resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])
st.markdown("<br>", unsafe_allow_html=True)

# ── ANALYZE BUTTON ────────────────────────────────────
btn_clicked = st.button("🔭 Analyze Now")

if btn_clicked:
    if not role or not location or not resume_file:
        missing = [x for x, v in [("Job Role", role), ("City", location), ("Resume", resume_file)] if not v]
        st.warning(f"⚠️ Please fill in: {', '.join(missing)}")
        st.stop()

    with st.spinner(f"Fetching {role} jobs in {location}..."):
        jobs = fetch_jobs(role, location, num_jobs, country_code)

    if not jobs:
        st.error("No jobs found. Try a different role or city.")
        st.stop()

    with st.spinner("Reading your resume..."):
        resume_text = extract_resume(resume_file)

    if not resume_text.strip():
        st.warning("Could not extract text from resume. Try a text-based PDF.")
        st.stop()

    with st.spinner("Analyzing market trends..."):
        analysis = market_analysis(jobs, role, location)

    with st.spinner("Building your personalized roadmap..."):
        roadmap = career_roadmap(resume_text, jobs, role)

    st.success(f"✅ Analysis complete — {len(jobs)} jobs found for **{role}** in **{location}**")
    st.markdown("---")

    # ── METRICS ───────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Jobs Found", len(jobs))
    with m2:
        st.metric("Companies", len(set(j["company"] for j in jobs if j["company"] != "N/A")))
    with m3:
        st.metric("With Salary", sum(1 for j in jobs if j["salary"]))
    with m4:
        st.metric("Locations", len(set(j["location"] for j in jobs)))

    st.markdown("---")

    # ── MARKET + ROADMAP ──────────────────────────────
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("### 📊 Market Insights")
        st.markdown(analysis)
    with right:
        st.markdown("### 🎯 Career Roadmap")
        st.markdown(roadmap)

    st.markdown("---")

    # ── JOB LISTINGS ──────────────────────────────────
    st.markdown("### 💼 Live Job Listings")
    for i, job in enumerate(jobs):
        # Plain separator between cards
        if i > 0:
            st.markdown("---")

        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.markdown(f"#### {job['title']}")
            st.markdown(f"🏢 **{job['company']}** &nbsp;|&nbsp; 📍 {job['location']}", unsafe_allow_html=True)
            row = []
            if job["salary"]:
                row.append(f"💰 {job['salary']}")
            if job["category"]:
                row.append(f"🏷 {job['category']}")
            if job["date"]:
                row.append(f"📅 {job['date']}")
            if row:
                st.caption("  ·  ".join(row))
        with col_b:
            st.markdown(f"[🔗 Apply →]({job['link']})")

        desc = job["desc"] or "No description available."
        st.write(desc[:500] + ("..." if len(desc) > 500 else ""))

    st.markdown("---")
    st.caption("CareerLens · Groq LLaMA 3.3 + Adzuna API")