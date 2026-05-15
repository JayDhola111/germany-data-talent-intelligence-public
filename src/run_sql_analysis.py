import duckdb
from pathlib import Path


SQL_DIR = Path("sql")
OUTPUT_DIR = Path("data/analysis")

QUERY_FILES = {
    "top_skills": SQL_DIR / "top_skills.sql",
    "role_category_analysis": SQL_DIR / "role_category_analysis.sql",
    "employment_type_analysis": SQL_DIR / "employment_type_analysis.sql",
    "language_requirement_analysis": SQL_DIR / "language_requirement_analysis.sql",
    "skill_by_role_analysis": SQL_DIR / "skill_by_role_analysis.sql",
    "entry_level_opportunities": SQL_DIR / "entry_level_opportunities.sql",
}


def run_query(connection, query_name, query_path):
    print(f"\nRunning: {query_name}")

    sql = query_path.read_text(encoding="utf-8")
    result_df = connection.execute(sql).df()

    output_path = OUTPUT_DIR / f"{query_name}.csv"
    result_df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(result_df.head(10).to_string(index=False))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    connection = duckdb.connect()

    for query_name, query_path in QUERY_FILES.items():
        if not query_path.exists():
            print(f"Missing SQL file: {query_path}")
            continue

        run_query(connection, query_name, query_path)

    connection.close()

    print("\nSQL analysis completed successfully.")


if __name__ == "__main__":
    main()