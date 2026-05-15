import pandas as pd
from pathlib import Path

PUBLIC_DIR = Path("public_data")
PUBLIC_DIR.mkdir(exist_ok=True)

def read_csv(path):
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")

# Remove full job descriptions from job-level data
jobs = read_csv("data/processed/clean_jobs_with_skills.csv")

columns_to_remove = [
    "job_description"
]

safe_jobs = jobs.drop(columns=[col for col in columns_to_remove if col in jobs.columns])
safe_jobs.to_csv(PUBLIC_DIR / "public_jobs.csv", index=False)

# These analysis files are safe because they contain aggregated insights
safe_files = {
    "data/processed/job_skills.csv": "public_job_skills.csv",
    "data/analysis/top_skills.csv": "public_top_skills.csv",
    "data/analysis/role_category_analysis.csv": "public_role_category_analysis.csv",
    "data/analysis/employment_type_analysis.csv": "public_employment_type_analysis.csv",
    "data/analysis/language_requirement_analysis.csv": "public_language_requirement_analysis.csv",
    "data/analysis/skill_by_role_analysis.csv": "public_skill_by_role_analysis.csv",
    "data/analysis/entry_level_opportunities.csv": "public_entry_level_opportunities.csv",
}

for source, target in safe_files.items():
    df = read_csv(source)
    if "job_description" in df.columns:
        df = df.drop(columns=["job_description"])
    df.to_csv(PUBLIC_DIR / target, index=False)

print("Public-safe data created in public_data/")
