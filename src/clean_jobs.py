import pandas as pd
import re
from pathlib import Path


RAW_PATH = Path("data/raw/raw_jobs.csv")
PROCESSED_PATH = Path("data/processed/clean_jobs.csv")


def clean_text(value):
    """Basic text cleaning for string columns."""
    if pd.isna(value):
        return ""
    value = str(value)
    value = value.replace("\n", " ").replace("\r", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def standardize_work_model(value):
    """Standardize work model values."""
    value = clean_text(value).lower()

    if "remote" in value:
        return "Remote"
    if "hybrid" in value:
        return "Hybrid"
    if "on-site" in value or "onsite" in value or "office" in value:
        return "On-site"
    return "Unknown"


def standardize_employment_type(value, title=""):
    """Standardize employment type based on field and title."""
    combined = f"{clean_text(value)} {clean_text(title)}".lower()

    if "werkstudent" in combined or "working student" in combined:
        return "Working Student"
    if "intern" in combined or "praktikum" in combined or "internship" in combined:
        return "Internship"
    if "trainee" in combined:
        return "Trainee"
    if "full-time" in combined or "full time" in combined or "vollzeit" in combined:
        return "Full-time"
    if "part-time" in combined or "teilzeit" in combined:
        return "Part-time"

    return "Unknown"


def categorize_role(title, description):
    """Classify job into simple role categories."""
    combined = f"{clean_text(title)} {clean_text(description)}".lower()

    if any(word in combined for word in ["business intelligence", "bi analyst", "power bi", "tableau", "dashboard"]):
        return "BI / Reporting"
    if any(word in combined for word in ["data engineer", "etl", "pipeline", "warehouse", "dbt"]):
        return "Data Engineering"
    if any(word in combined for word in ["machine learning", "ml engineer", "ai engineer", "deep learning", "llm"]):
        return "AI / ML"
    if any(word in combined for word in ["data analyst", "analytics", "reporting analyst", "sql analyst"]):
        return "Data Analytics"

    return "Other Data Role"


def detect_language_requirement(description):
    """Detect basic language requirement from job description."""
    description = clean_text(description).lower()

    german_words = ["german", "deutsch", "deutschkentnisse", "deutschkenntnisse"]
    english_words = ["english", "englisch"]

    has_german = any(word in description for word in german_words)
    has_english = any(word in description for word in english_words)

    if has_german and has_english:
        return "German + English"
    if has_german:
        return "German"
    if has_english:
        return "English"
    return "Not specified"


def main():
    try:
        df = pd.read_csv(RAW_PATH, encoding="utf-8")
    except UnicodeDecodeError:
        print("UTF-8 failed. Trying Windows/Latin encoding...")
        df = pd.read_csv(RAW_PATH, encoding="latin1")

    # Clean basic text columns
    text_columns = [
        "job_title",
        "company",
        "location",
        "employment_type",
        "work_model",
        "source",
        "job_description",
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    # Create new clean columns
    df["clean_job_title"] = df["job_title"].apply(clean_text)
    df["clean_location"] = df["location"].apply(clean_text)
    df["standard_work_model"] = df["work_model"].apply(standardize_work_model)
    df["standard_employment_type"] = df.apply(
        lambda row: standardize_employment_type(row["employment_type"], row["job_title"]),
        axis=1
    )
    df["role_category"] = df.apply(
        lambda row: categorize_role(row["job_title"], row["job_description"]),
        axis=1
    )
    df["language_requirement"] = df["job_description"].apply(detect_language_requirement)

    # Basic quality checks
    df["description_length"] = df["job_description"].apply(len)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"Cleaned data saved to: {PROCESSED_PATH}")
    print(f"Rows processed: {len(df)}")
    print("\nRole category counts:")
    print(df["role_category"].value_counts())
    print("\nEmployment type counts:")
    print(df["standard_employment_type"].value_counts())


if __name__ == "__main__":
    main()
