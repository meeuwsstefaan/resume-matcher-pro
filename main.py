"""
Resume-Job Matcher — Main Entry Point
======================================
Reads resumes and job posts from input/, extracts keywords,
computes matches, and generates PDF + HTML reports in output/.
"""

import os
import sys

from config import RESUMES_DIR, JOBS_DIR, SUPPORTED_EXTENSIONS
from parsers.file_parser import parse_file
from extractors.keyword_extractor import extract_keywords
from matcher.job_matcher import compute_matches
from reporters.pdf_reporter import generate_pdf_report
from reporters.html_reporter import generate_html_report


def collect_files(directory: str) -> list[str]:
    """Return the list of supported file paths in a directory."""
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)
        return []
    return [
        os.path.join(directory, f)
        for f in sorted(os.listdir(directory))
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]


def process_documents(file_paths: list[str]) -> dict[str, list[str]]:
    """Parse files and extract keywords. Returns dict of filename -> keywords."""
    results = {}
    for path in file_paths:
        filename = os.path.basename(path)
        print(f"  Processing: {filename}...", end=" ")
        try:
            text = parse_file(path)
            if not text:
                raise ValueError("Empty file")
            else:
                print(f"({len(text)} characters)")
            keywords = extract_keywords(text)
            if not keywords:
                raise ValueError("No keywords found")
            else:
                keywords = sorted(set(keywords))
                print(f"({len(keywords)} keywords)")
                print(f"  {', '.join(keywords)}")
            results[filename] = keywords
        except Exception as e:
            print(f"ERROR: {e}")
            results[filename] = []
    return results


def main():
    print("=" * 60)
    print("  RESUME-JOB MATCHER")
    print("=" * 60)

    resume_files = collect_files(RESUMES_DIR)
    job_files = collect_files(JOBS_DIR)

    if not resume_files:
        print(f"\n⚠  No resumes found in {RESUMES_DIR}/")
        print("   Place PDF, DOCX, or TXT files there and re-run.")
        sys.exit(1)

    if not job_files:
        print(f"\n⚠  No job posts found in {JOBS_DIR}/")
        print("   Place PDF, DOCX, or TXT files there and re-run.")
        sys.exit(1)

    print(f"\nFound {len(resume_files)} resume(s) and {len(job_files)} job post(s).\n")

    print("── Extracting Resume Keywords ──")
    resumes = process_documents(resume_files)

    print("\n── Extracting Job Post Keywords ──")
    jobs = process_documents(job_files)

    print("\n── Computing Matches ──")
    matches = compute_matches(resumes, jobs)
    print(f"  Generated {len(matches)} match(es).\n")

    print("── Generating Reports ──")
    pdf_path = generate_pdf_report(resumes, jobs, matches)
    print(f"  ✓ PDF report: {pdf_path}")

    html_path = generate_html_report(resumes, jobs, matches)
    print(f"  ✓ HTML report: {html_path}")

    print("\n" + "=" * 60)
    print("  Done! Open the reports in output/")
    print("=" * 60)


if __name__ == "__main__":
    main()
