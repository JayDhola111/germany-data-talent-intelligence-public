SELECT
    language_requirement,
    COUNT(*) AS total_jobs,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM read_csv_auto('data/processed/clean_jobs_with_skills.csv')),
        1
    ) AS percentage_of_jobs
FROM read_csv_auto('data/processed/clean_jobs_with_skills.csv')
GROUP BY
    language_requirement
ORDER BY
    total_jobs DESC;