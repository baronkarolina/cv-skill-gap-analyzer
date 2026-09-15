# CV Skill Gap Analyzer

A Streamlit web app that compares a CV against the skill profile of a target job role and highlights what's already there and what's missing.

## What it does

- Upload a CV as PDF, DOCX, or TXT
- Pick a target role (e.g. Quantitative Risk Analyst, Financial Engineer, Data Scientist, Investment Banking Analyst, and more)
- Get a readiness score, a breakdown of skills found vs. missing, and a full comparison table


## Tech stack

- **Streamlit** – web app framework
- **pandas** – data handling and the comparison table
- **pypdf** – PDF text extraction
- **python-docx** – Word document text extraction
- Simple regex-based keyword matching against role-specific skill profiles

## Running it locally

```bash
# Clone the repo
git clone https://github.com/baronkarolina/cv-skill-gap-analyzer.git
cd cv-skill-gap-analyzer

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

## Possible improvements

- Add more role profiles and let users define custom ones
- Move from keyword matching to embedding-based semantic matching
- Suggest specific resources or courses for each missing skill

## License

Personal project, shared for portfolio purposes.