"""Generate a PDF report of resume-job matches."""

import os
from fpdf import FPDF

from matcher.job_matcher import MatchResult
from config import OUTPUT_DIR


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Resume-Job Matching Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def generate_pdf_report(
    resumes: dict[str, list[str]],
    jobs: dict[str, list[str]],
    matches: list[MatchResult],
) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "report.pdf")

    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Section 1: Resume Keywords
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "SECTION 1: Resume Keywords", ln=True)
    pdf.ln(3)

    for resume_name, keywords in resumes.items():
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, f"Resume: {resume_name}", ln=True)
        pdf.set_font("Helvetica", "", 9)
        kw_text = ", ".join(keywords) if keywords else "(no keywords extracted)"
        pdf.multi_cell(0, 6, f"  Keywords: {kw_text}")
        pdf.ln(3)

    # Section 2: Matches per Resume
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "SECTION 2: Relevant Jobs per Resume", ln=True)
    pdf.ln(3)

    for resume_name in resumes:
        resume_matches = [m for m in matches if m.resume_name == resume_name]
        resume_matches.sort(key=lambda m: m.fit_percentage, reverse=True)

        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, f"Resume: {resume_name}", ln=True)

        if not resume_matches:
            pdf.set_font("Helvetica", "I", 9)
            pdf.cell(0, 6, "  No matching jobs found.", ln=True)
        else:
            for m in resume_matches:
                pdf.set_font("Helvetica", "", 9)
                pdf.cell(0, 6, f"  - {m.job_name}: {m.fit_percentage}% fit", ln=True)
                if m.matched_keywords:
                    pdf.set_font("Helvetica", "I", 8)
                    pdf.cell(0, 5, f"    Matched: {', '.join(m.matched_keywords)}", ln=True)
        pdf.ln(3)

    # Section 3: Matches per Job
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "SECTION 3: Resumes per Job (sorted by fit %)", ln=True)
    pdf.ln(3)

    for job_name in jobs:
        job_matches = [m for m in matches if m.job_name == job_name]
        job_matches.sort(key=lambda m: m.fit_percentage, reverse=True)

        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, f"Job: {job_name}", ln=True)

        if not job_matches:
            pdf.set_font("Helvetica", "I", 9)
            pdf.cell(0, 6, "  No matching resumes found.", ln=True)
        else:
            for m in job_matches:
                pdf.set_font("Helvetica", "", 9)
                pdf.cell(0, 6, f"  - {m.resume_name}: {m.fit_percentage}% fit", ln=True)
        pdf.ln(3)

    pdf.output(output_path)
    return output_path
