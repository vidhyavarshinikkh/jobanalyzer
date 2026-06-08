# 🎯 Job Market Analyzer & Career Advisor

An AI-powered application that analyzes real-time job market trends and provides personalized career guidance based on a user's resume.

> 🔍 Turn job data into insights
> 🎯 Turn your resume into a roadmap

---

## 📌 Overview

This project fetches real-time job listings and uses AI to:

* Analyze market demand
* Extract in-demand skills
* Compare with user resume
* Generate a personalized career roadmap

👨‍🎓 Designed for students and early professionals who want clarity in their career path.

---

## 🎯 Objective

This project helps students understand:

* Multi-agent AI systems
* LLM-based reasoning
* API integration
* Resume analysis
* Building real-world AI applications

---

## 🚀 Features

* 🔍 Real-time job search (API-based)
* 📊 Market insights (skills, trends, salary)
* 📄 Resume analysis (PDF/TXT)
* 🎯 Career guidance (skill gap + roadmap)
* 💼 Job listings with descriptions
* 🧠 Multi-agent workflow (Market + Career Advisor)

---

## 🧠 Architecture / Workflow

### 🔄 System Flow

1. User inputs:

   * Job role
   * Location
   * Resume

2. System:

   * Fetches job data from API
   * Extracts job descriptions

3. Agent 1: Market Analyzer

   * Identifies key skills
   * Detects market trends

4. Agent 2: Career Advisor

   * Compares resume with market
   * Finds skill gaps
   * Generates roadmap

5. Output:

   * Market insights
   * Job listings
   * Career advice

---

## 🛠 Tech Stack

* **Language:** Python
* **UI:** Streamlit
* **LLM:** Groq (LLaMA 3)
* **API:** RapidAPI (JSearch)
* **LANGCHAIN : Connecting everything
  

### 📦 Libraries Used

* streamlit
* requests
* python-dotenv
* groq
* PyPDF2

---

## 📁 Project Structure

```
job-market-analyzer/
│
├── app.py
├── requirements.txt
├── .env              # (Not uploaded to GitHub)
├── README.md
```

---

## ⚙️ Setup Instructions

### 🔧 Prerequisites

* Python 3.8+
* Git installed
* API Keys:

  * RapidAPI Key
  * Groq API Key

---

## 📦 Installation (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/job-market-analyzer.git
cd job-market-analyzer
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
pip install httpx==0.27.0
pip install streamlit groq python-dotenv requests PyPDF2
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```
RAPIDAPI_KEY=your_rapidapi_key
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Running the Project

```bash
streamlit run app.py
```

Then open:
👉 http://localhost:8501

---

## 💻 How It Works (Code-Level)

### 🔹 fetch_jobs()

* Calls job API
* Retrieves job listings

### 🔹 analyze_market()

* Sends job data to LLM
* Returns skills, trends, salary insights

### 🔹 career_advice()

* Compares resume with job data
* Outputs:

  * Skill gaps
  * Learning roadmap
  * Improvements

### 🔹 extract_resume_text()

* Reads PDF/TXT resume
* Converts into text

---

## 🧪 Example Usage

### Input:

* Role: AI Engineer
* Location: Chennai
* Resume: Uploaded file

### Output:

* 📊 Top Skills: Python, ML, NLP
* 📈 Trends: Growing AI demand
* 🎯 Missing Skills: MLOps, Deployment
* 🛣 Roadmap:

  * Learn ML fundamentals
  * Build projects
  * Deploy models

---

## 🔧 Customization / Extensions

Students can enhance this project by:

* Adding skill match percentage
* Resume scoring system
* Downloadable reports (PDF)
* Chatbot interface
* Dashboard visualization

---

## 🚀 Future Improvements

* Add database integration
* Deploy online (Streamlit Cloud)
* Improve resume parsing
* Add analytics dashboard
* Multi-role comparison

---

## 👨‍💻 Contributors

* Sreshta Sridhar

---

## 💡 Workshop Instructions

To run this project:

```bash
pip install -r requirements.txt
streamlit run app.py
```

⚠️ Important:

* Create `.env` file
* Add API keys
* Use virtual environment (recommended)

---

## 🔥 Final Note

This project demonstrates a **real-world AI system** combining:

* APIs
* LLMs
* Multi-agent architecture

A perfect starting point for **AI Engineering & Career Intelligence Tools** 🚀
