def compute_similarity(resume_skills, job_skills):
    if not resume_skills or not job_skills:
        return 0.0

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = len(resume_set & job_set)

    keyword_score = matched / len(job_set) if job_set else 0

    overlap_ratio = len(resume_set & job_set) / max(len(resume_set), 1)

    return (keyword_score * 0.7 + overlap_ratio * 0.3)


def store_skills(skills, doc_type):
    return