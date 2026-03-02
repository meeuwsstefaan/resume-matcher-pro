"""Extract keywords from text using RAKE and TF-IDF."""

import re
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

from config import MAX_KEYWORDS, RAKE_MIN_LENGTH, RAKE_MAX_LENGTH, MIN_KEYWORD_LENGTH


def extract_keywords(text: str) -> list[str]:
    rake_keywords = _rake_extract(text)
    tfidf_keywords = _tfidf_extract(text)

    seen = set()
    merged = []
    for kw in rake_keywords + tfidf_keywords:
        kw_lower = kw.lower().strip()
        if kw_lower not in seen and len(kw_lower) >= MIN_KEYWORD_LENGTH:
            seen.add(kw_lower)
            merged.append(kw_lower)

    return merged[:MAX_KEYWORDS]


def _rake_extract(text: str) -> list[str]:
    rake = Rake(min_length=RAKE_MIN_LENGTH, max_length=RAKE_MAX_LENGTH)
    rake.extract_keywords_from_text(text)
    ranked = rake.get_ranked_phrases()
    return ranked[:MAX_KEYWORDS]


def _tfidf_extract(text: str) -> list[str]:
    clean = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
    clean = re.sub(r"\s+", " ", clean).strip()

    if not clean:
        return []

    vectorizer = TfidfVectorizer(
        max_features=MAX_KEYWORDS,
        stop_words="english",
        token_pattern=r"\b[a-zA-Z]{2,}\b",
    )

    try:
        tfidf_matrix = vectorizer.fit_transform([clean])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        scored = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
        return [word for word, score in scored if score > 0]
    except ValueError:
        return []
