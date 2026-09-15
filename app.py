import re
import pandas as pd
import streamlit as st
from io import StringIO
from docx import Document
from pypdf import PdfReader

ROLE_PROFILES = {
    "Quantitative Risk Analyst": [
        "Python","statistics","time series analysis","Monte Carlo simulation","Value at Risk",
        "credit risk modeling","market risk modeling","financial modeling","stress testing","Basel III"
    ],
    "Financial Engineer": [
        "Python","C++","stochastic processes","derivatives pricing","Monte Carlo simulation",
        "numerical methods","optimization algorithms","financial econometrics","time series forecasting","risk-neutral valuation"
    ],
    "Business Analytics Consultant": [
        "Python","SQL","data visualization","regression analysis","machine learning",
        "A/B testing","forecasting","dashboard creation","stakeholder communication","business case development"
    ],
    "Product Manager (Tech / FinTech)": [
        "product strategy","roadmap planning","data analysis","SQL","A/B testing",
        "KPI definition","agile methodology","stakeholder management","user research","data-driven decision making"
    ],
    "Data Scientist": [
        "Python","SQL","machine learning","deep learning","statistics",
        "feature engineering","model evaluation","natural language processing","time series analysis","data cleaning"
    ],
    "AI Risk & Model Governance Specialist": [
        "model risk management","regulatory compliance","Basel III","explainable AI","bias detection",
        "stress testing","model validation","risk assessment methodologies","Python","governance frameworks"
    ],
    "Investment Banking Analyst": [
        "financial modeling","DCF modeling","valuation techniques","Excel","financial statement analysis",
        "capital markets knowledge","comparable company analysis","PowerPoint","due diligence","attention to detail"
    ],
    "FinTech Startup Founder": [
        "product development","financial modeling","fundraising","user acquisition strategy","data analytics",
        "Python","cloud computing","strategic planning","leadership","fintech regulation"
    ]
}

def read_pdf(file) -> str:
    reader = PdfReader(file)
    return "\n".join([(p.extract_text() or "") for p in reader.pages])

def read_docx(file) -> str:
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def contains_skill(text: str, skill: str) -> bool:
    # handle short skills like SQL, C++
    t = text.lower()
    s = skill.lower().strip()
    if len(s) <= 4 or any(ch in s for ch in "+#/."):
        return s in t
    return re.search(rf"\b{re.escape(s)}\b", t) is not None

def gap_analysis(cv_text: str, target_role: str) -> pd.DataFrame:
    skills = ROLE_PROFILES[target_role]
    rows = [{"skill": s, "present": contains_skill(cv_text, s)} for s in skills]
    return pd.DataFrame(rows)

st.set_page_config(page_title="CV Skill Gap Analyzer", page_icon="🚀", layout="centered")
st.title("🚀 CV Skill Gap Analyzer")
st.write("Upload your CV and pick a target role. You'll get a skill gap analysis.")

uploaded = st.file_uploader("Upload CV (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])
role = st.selectbox("Target role", list(ROLE_PROFILES.keys()))

if uploaded is not None:
    if uploaded.name.lower().endswith(".pdf"):
        cv_text = read_pdf(uploaded)
    elif uploaded.name.lower().endswith(".docx"):
        cv_text = read_docx(uploaded)
    else:
        cv_text = StringIO(uploaded.getvalue().decode("utf-8", errors="ignore")).read()

    df = gap_analysis(cv_text, role)
    present = df[df["present"]]["skill"].tolist()
    missing = df[~df["present"]]["skill"].tolist()
    score = round(len(present) / len(df) * 100, 1)

    st.metric("Readiness score", f"{score}%")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Found in CV")
        st.write(present if present else ["(none detected)"])
    with col2:
        st.subheader("❌ Missing / not detected")
        st.write(missing if missing else ["(no gaps detected)"])

    st.subheader("Full table")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Upload a CV to run the analysis.")
