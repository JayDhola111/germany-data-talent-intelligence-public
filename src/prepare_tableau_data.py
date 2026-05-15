import pandas as pd
from pathlib import Path


PROCESSED_DIR = Path("data/processed")
ANALYSIS_DIR = Path("data/analysis")
TABLEAU_DIR = Path("data/tableau")


FILES_TO_EXPORT = {
    "clean_jobs_with_skills.csv": "tableau_jobs.csv",
    "job_skills.csv": "tableau_job_skills.csv",
    "top_skills.csv": "tableau_top_skills.csv",
    "skill_by_role_analysis.csv": "tableau_skill_by_role.csv",
    "role_category_analysis.csv": "tableau_role_category.csv",
    "employment_type_analysis.csv": "tableau_employment_type.csv",
    "language_requirement_analysis.csv": "tableau_language_requirement.csv",
    "entry_level_opportunities.csv": "tableau_entry_level_opportunities.csv",
}


def read_csv_safely(path):
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")


def export_file(source_path, output_path):
    if not source_path.exists():
        print(f"Missing file: {source_path}")
        return

    df = read_csv_safely(source_path)

    # Remove duplicate rows if any
    df = df.drop_duplicates()

    # Save clean Tableau version
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Exported {source_path} → {output_path}")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")


def main():
    TABLEAU_DIR.mkdir(parents=True, exist_ok=True)

    for input_file, output_file in FILES_TO_EXPORT.items():
        if input_file in ["clean_jobs_with_skills.csv", "job_skills.csv"]:
            source_path = PROCESSED_DIR / input_file
        else:
            source_path = ANALYSIS_DIR / input_file

        output_path = TABLEAU_DIR / output_file
        export_file(source_path, output_path)

    print("\nTableau data preparation completed.")


if __name__ == "__main__":
    main()
