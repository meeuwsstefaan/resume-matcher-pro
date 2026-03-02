"""Generate an HTML report with interactive tables."""

import os
from jinja2 import Template

from matcher.job_matcher import MatchResult
from config import OUTPUT_DIR

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume-Job Matching Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; color: #1a1a2e; padding: 2rem; }
        h1 { text-align: center; margin-bottom: 2rem; color: #16213e; font-size: 1.8rem; }
        h2 { margin: 2rem 0 1rem; color: #0f3460; border-bottom: 2px solid #e94560; padding-bottom: 0.5rem; }
        h3 { margin: 1rem 0 0.5rem; color: #16213e; }
        .container { max-width: 1200px; margin: 0 auto; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        th { background: #16213e; color: #fff; padding: 12px 16px; text-align: left; font-weight: 600; }
        td { padding: 10px 16px; border-bottom: 1px solid #eee; }
        tr:hover td { background: #f8f9ff; }
        .fit-high { color: #27ae60; font-weight: bold; }
        .fit-mid { color: #f39c12; font-weight: bold; }
        .fit-low { color: #e74c3c; font-weight: bold; }
        .keywords { font-size: 0.85rem; color: #555; }
        .badge { display: inline-block; background: #e8f4fd; color: #0f3460; padding: 2px 8px; border-radius: 12px; font-size: 0.78rem; margin: 2px; }
        .section { background: #fff; border-radius: 12px; padding: 1.5rem 2rem; margin-bottom: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    </style>
</head>
<body>
<div class="container">
    <h1>📄 Resume-Job Matching Report</h1>

    <div class="section">
        <h2>Resume Keywords</h2>
        {% for resume_name, keywords in resumes.items() %}
        <h3>{{ resume_name }}</h3>
        <p class="keywords">
            {% for kw in keywords %}<span class="badge">{{ kw }}</span>{% endfor %}
            {% if not keywords %}<em>No keywords extracted.</em>{% endif %}
        </p>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Matches by Resume</h2>
        {% for resume_name in resumes %}
        <h3>{{ resume_name }}</h3>
        {% set resume_matches = matches | selectattr("resume_name", "equalto", resume_name) | sort(attribute="fit_percentage", reverse=true) | list %}
        {% if resume_matches %}
        <table>
            <tr><th>Job Post</th><th>Fit %</th><th>Matched Keywords</th></tr>
            {% for m in resume_matches %}
            <tr>
                <td>{{ m.job_name }}</td>
                <td class="{{ 'fit-high' if m.fit_percentage >= 60 else 'fit-mid' if m.fit_percentage >= 30 else 'fit-low' }}">{{ m.fit_percentage }}%</td>
                <td class="keywords">{{ m.matched_keywords | join(', ') }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p><em>No matching jobs.</em></p>
        {% endif %}
        {% endfor %}
    </div>

    <div class="section">
        <h2>Matches by Job Post (sorted by fit %)</h2>
        {% for job_name in jobs %}
        <h3>{{ job_name }}</h3>
        {% set job_matches = matches | selectattr("job_name", "equalto", job_name) | sort(attribute="fit_percentage", reverse=true) | list %}
        {% if job_matches %}
        <table>
            <tr><th>Resume</th><th>Fit %</th><th>Matched Keywords</th></tr>
            {% for m in job_matches %}
            <tr>
                <td>{{ m.resume_name }}</td>
                <td class="{{ 'fit-high' if m.fit_percentage >= 60 else 'fit-mid' if m.fit_percentage >= 30 else 'fit-low' }}">{{ m.fit_percentage }}%</td>
                <td class="keywords">{{ m.matched_keywords | join(', ') }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p><em>No matching resumes.</em></p>
        {% endif %}
        {% endfor %}
    </div>
</div>
</body>
</html>"""


def generate_html_report(
    resumes: dict[str, list[str]],
    jobs: dict[str, list[str]],
    matches: list[MatchResult],
) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "report.html")

    template = Template(HTML_TEMPLATE)
    html = template.render(resumes=resumes, jobs=jobs, matches=matches)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
