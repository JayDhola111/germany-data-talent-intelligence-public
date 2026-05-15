SELECT
    job_id,
    job_title,
    company,
    location,
    standard_employment_type,
    standard_work_model,
    role_category,
    language_requirement,
    skill_count,
    extracted_skills,
    CASE
        WHEN LOWER(job_title) LIKE '%junior%' THEN 'Entry-Level Friendly'
        WHEN LOWER(job_title) LIKE '%trainee%' THEN 'Entry-Level Friendly'
        WHEN LOWER(job_title) LIKE '%werkstudent%' THEN 'Student Friendly'
        WHEN LOWER(standard_employment_type) LIKE '%working student%' THEN 'Student Friendly'
        WHEN LOWER(standard_employment_type) LIKE '%trainee%' THEN 'Entry-Level Friendly'
        ELSE 'Check Manually'
    END AS opportunity_type
FROM read_csv_auto('data/processed/clean_jobs_with_skills.csv')
ORDER BY
    opportunity_type,
    role_category,
    skill_count DESC;