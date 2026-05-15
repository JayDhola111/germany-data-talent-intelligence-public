WITH jobs AS (
    SELECT
        job_id,
        role_category
    FROM read_csv_auto('data/processed/clean_jobs_with_skills.csv')
),

skills AS (
    SELECT
        job_id,
        skill_name,
        skill_category
    FROM read_csv_auto('data/processed/job_skills.csv')
),

skill_counts AS (
    SELECT
        j.role_category,
        s.skill_name,
        s.skill_category,
        COUNT(DISTINCT s.job_id) AS job_count
    FROM skills s
    JOIN jobs j
        ON s.job_id = j.job_id
    GROUP BY
        j.role_category,
        s.skill_name,
        s.skill_category
),

ranked_skills AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY role_category
            ORDER BY job_count DESC, skill_name
        ) AS skill_rank
    FROM skill_counts
)

SELECT
    role_category,
    skill_rank,
    skill_name,
    skill_category,
    job_count
FROM ranked_skills
WHERE skill_rank <= 10
ORDER BY
    role_category,
    skill_rank;