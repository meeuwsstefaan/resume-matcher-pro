"""Configuration constants for the resume matcher."""

import os

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
RESUMES_DIR = os.path.join(INPUT_DIR, "resumes")
JOBS_DIR = os.path.join(INPUT_DIR, "jobs")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Supported file extensions
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}

# Keyword extraction settings
MAX_KEYWORDS = 30
MIN_KEYWORD_LENGTH = 2
RAKE_MIN_LENGTH = 1
RAKE_MAX_LENGTH = 3

# Matching settings
MIN_FIT_PERCENTAGE = 0.0
