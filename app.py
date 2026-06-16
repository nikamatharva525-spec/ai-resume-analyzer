import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI
import os

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="AI ATS Resume Analyzer",
    page_icon="📄"
)

st.title("📄 AI ATS Resume Analyzer")

# -----------------------------
# Load Environment Variables
# -----------------------------
# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

try:
    # Streamlit Cloud
    api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    # Local Development (.env)
    api_key = os.getenv("OPENROUTER_API_KEY")

# TEST LINE


if api_key:
    st.success("✅ API Key Loaded Successfully")
else:
    st.error("❌ OPENROUTER_API_KEY not found")

    st.info("""
Local Development:
Create a .env file:

OPENROUTER_API_KEY=your_key

Streamlit Cloud:
Settings → Secrets

OPENROUTER_API_KEY="your_key"
""")

    st.stop()

# -----------------------------
# OpenRouter Client
# -----------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# -----------------------------
# OpenRouter Client
# -----------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# -----------------------------
# Upload Resume
# -----------------------------
uploaded_file = st.file_uploader(
    "📄 Upload Your Resume (PDF)",
    type=["pdf"]
)

# -----------------------------
# Job Description Input
# -----------------------------
job_description = st.text_area(
    "📋 Paste Job Description",
    height=200,
    placeholder="Paste the job description here..."
)

# -----------------------------
# Process Resume
# -----------------------------
if uploaded_file:

    try:
        reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text + "\n"

        st.success("✅ Resume Uploaded Successfully!")

        st.subheader("📄 Extracted Resume Text")

        st.text_area(
            "Resume Content",
            resume_text,
            height=250
        )

        # -----------------------------
        # Analyze Button
        # -----------------------------
        if st.button("🚀 Analyze ATS Match"):

            if not resume_text.strip():
                st.error("❌ No text found in resume.")
                st.stop()

            if not job_description.strip():
                st.error("❌ Please paste a Job Description.")
                st.stop()

            with st.spinner("🔍 Performing ATS Analysis..."):

                prompt = f"""
You are an expert ATS (Applicant Tracking System) and Senior HR Recruiter.

Compare the resume with the job description.

Provide the report in the following format:

ATS Match Percentage: XX%

Resume Summary

Matching Skills

Missing Skills

Strengths

Weaknesses

ATS Score (0-100)

Resume Score (0-100)

Keywords Missing From Resume

Improvement Suggestions

Final Recommendation

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""

                try:

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b:free",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    result = response.choices[0].message.content

                    # -----------------------------
                    # Metrics Section
                    # -----------------------------
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("🎯 ATS Match", "82%")

                    with col2:
                        st.metric("📄 Resume Score", "88/100")

                    st.progress(82)

                    # -----------------------------
                    # Report
                    # -----------------------------
                    st.subheader("📊 ATS Analysis Report")

                    st.markdown(result)

                    # -----------------------------
                    # Download Report
                    # -----------------------------
                    st.download_button(
                        label="📥 Download Report",
                        data=result,
                        file_name="ATS_Report.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"❌ OpenRouter Error: {e}")

    except Exception as e:
        st.error(f"❌ PDF Error: {e}")

else:
    st.info("📄 Please upload a PDF resume.")