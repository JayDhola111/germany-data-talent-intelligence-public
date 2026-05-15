SELECT
    role_category,
    COUNT(*) AS total_jobs,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM read_csv_auto('data/processed/clean_jobs_with_skills.csv')),
        1
    ) AS percentage_of_jobs,
    ROUND(AVG(skill_count), 1) AS avg_skills_per_job
FROM read_csv_auto('data/processed/clean_jobs_with_skills.csv')
GROUP BY
    role_category
ORDER BY
    total_jobs DESC;