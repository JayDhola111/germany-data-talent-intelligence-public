SELECT
    skill_name,
    skill_category,
    COUNT(DISTINCT job_id) AS job_count,
    ROUND(
        COUNT(DISTINCT job_id) * 100.0 /
        (SELECT COUNT(DISTINCT job_id)
         FROM read_csv_auto('data/processed/clean_jobs_with_skills.csv')),
        1
    ) AS job_percentage
FROM read_csv_auto('data/processed/job_skills.csv')
GROUP BY
    skill_name,
    skill_category
ORDER BY
    job_count DESC,
    skill_name;