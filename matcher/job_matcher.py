"""Match resumes to jobs based on keyword overlap."""

from dataclasses import dataclass


@dataclass
class MatchResult:
    resume_name: str
    job_name: str
    fit_percentage: float
    matched_keywords: list[str]
    resume_keywords: list[str]
    job_keywords: list[str]


def compute_matches(
    resumes: dict[str, list[str]],
    jobs: dict[str, list[str]],
) -> list[MatchResult]:
    results = []

    for resume_name, resume_kw in resumes.items():
        resume_set = set(resume_kw)

        for job_name, job_kw in jobs.items():
            job_set = set(job_kw)

            if not job_set:
                continue

            matched = resume_set & job_set
            fit_pct = (len(matched) / len(job_set)) * 100

            results.append(MatchResult(
                resume_name=resume_name,
                job_name=job_name,
                fit_percentage=round(fit_pct, 1),
                matched_keywords=sorted(matched),
                resume_keywords=resume_kw,
                job_keywords=job_kw,
            ))

    results.sort(key=lambda r: r.fit_percentage, reverse=True)
    return results
