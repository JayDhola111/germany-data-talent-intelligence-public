import pandas as pd
import re
from pathlib import Path


CLEAN_JOBS_PATH = Path("data/processed/clean_jobs.csv")
SKILL_TAXONOMY_PATH = Path("data/reference/skill_taxonomy.csv")

OUTPUT_JOBS_PATH = Path("data/processed/clean_jobs_with_skills.csv")
OUTPUT_JOB_SKILLS_PATH = Path("data/processed/job_skills.csv")


def clean_text(value):
    """Basic text cleaning."""
    if pd.isna(value):
        return ""
    value = str(value)
    value = value.replace("\n", " ").replace("\r", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_for_matching(text):
    """Lowercase and normalize text for skill matching."""
    text = clean_text(text).lower()
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def skill_found(skill, text):
    """
    Detect whether a skill appears in text.
    Uses word-boundary matching for better accuracy.
    """
    skill_lower = skill.lower().strip()

    # Special handling for common skills with symbols or spaces
    special_skills = {
        "c++": r"c\+\+",
        "c#": r"c#",
        "node.js": r"node\.js|nodejs",
        "scikit-learn": r"scikit learn|scikit-learn|sklearn",
        "power bi": r"power bi|powerbi",
        "power query": r"power query",
        "rest api": r"rest api|restful api",
        "machine learning": r"machine learning|ml",
        "data cleaning": r"data cleaning|datenbereinigung",
        "etl": r"\betl\b|extract transform load",
        "sql": r"\bsql\b",
        "api": r"\bapi\b|apis",
        "git": r"\bgit\b",
        "github": r"github",
        "gcp": r"\bgcp\b|google cloud",
        "aws": r"\baws\b|amazon web services",
    }

    if skill_lower in special_skills:
        return re.search(special_skills[skill_lower], text) is not None

    # General matching
    escaped_skill = re.escape(skill_lower)
    pattern = rf"\b{escaped_skill}\b"
    return re.search(pattern, text) is not None


def extract_skills_from_text(text, taxonomy_df):
    """Return detected skills and categories from one job description."""
    normalized_text = normalize_for_matching(text)

    detected = []

    for _, row in taxonomy_df.iterrows():
        skill_name = clean_text(row["skill_name"])
        skill_category = clean_text(row["skill_category"])

        if not skill_name:
            continue

        if skill_found(skill_name, normalized_text):
            detected.append(
                {
                    "skill_name": skill_name,
                    "skill_category": skill_category
                }
            )

    return detected


def main():
    jobs_df = pd.read_csv(CLEAN_JOBS_PATH)
    taxonomy_df = pd.read_csv(SKILL_TAXONOMY_PATH)

    all_job_skills = []
    skills_list_per_job = []
    skill_count_per_job = []

    for _, row in jobs_df.iterrows():
        job_id = row["job_id"]
        title = clean_text(row.get("job_title", ""))
        description = clean_text(row.get("job_description", ""))

        combined_text = f"{title} {description}"

        detected_skills = extract_skills_from_text(combined_text, taxonomy_df)

        skill_names = [item["skill_name"] for item in detected_skills]

        skills_list_per_job.append(", ".join(skill_names))
        skill_count_per_job.append(len(skill_names))

        for item in detected_skills:
            all_job_skills.append(
                {
                    "job_id": job_id,
                    "skill_name": item["skill_name"],
                    "skill_category": item["skill_category"]
                }
            )

    jobs_df["extracted_skills"] = skills_list_per_job
    jobs_df["skill_count"] = skill_count_per_job

    job_skills_df = pd.DataFrame(all_job_skills)

    OUTPUT_JOBS_PATH.parent.mkdir(parents=True, exist_ok=True)

    jobs_df.to_csv(OUTPUT_JOBS_PATH, index=False)
    job_skills_df.to_csv(OUTPUT_JOB_SKILLS_PATH, index=False)

    print(f"Saved jobs with skills to: {OUTPUT_JOBS_PATH}")
    print(f"Saved job-skill mapping to: {OUTPUT_JOB_SKILLS_PATH}")
    print(f"Total jobs processed: {len(jobs_df)}")
    print(f"Total job-skill rows created: {len(job_skills_df)}")

    if not job_skills_df.empty:
        print("\nTop detected skills:")
        print(job_skills_df["skill_name"].value_counts().head(15))
    else:
        print("\nNo skills detected. Check skill taxonomy or job descriptions.")


if __name__ == "__main__":
    main()
