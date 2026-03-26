# src/main.py
from src.client import search_projects
from src.filters import passes_hard_filters
from src.scorer import score_project, assign_fit_bucket
from src.utils import deduplicate_projects
from src.mailer import send_results_email

from config.keywords import KEYWORD_GROUPS
from config.settings import SETTINGS

#  python -m src.main

QUICK_FIX_QUERIES = [
    "css fix",
    "website bug",
    "wordpress fix",
    "shopify fix",
    "website testing",
    "responsive issue",
    "layout bug",
    "frontend bug",
    "fix website error",
    "ui bug",
]

SMALL_BUILD_QUERIES = [
    "landing page",
    "figma to html",
    "figma to wordpress",
    "website build",
    "one page website",
    "small business website",
]


def run_mode(mode_name, queries):
    all_projects = []

    for q in queries:
        results = search_projects(q)
        all_projects.extend(results)

    unique_projects = deduplicate_projects(all_projects)

    filtered = [
        p for p in unique_projects
        if passes_hard_filters(p, SETTINGS, KEYWORD_GROUPS)
    ]

    scored = []
    for p in filtered:
        score = score_project(p, SETTINGS, KEYWORD_GROUPS)
        bucket = assign_fit_bucket(score)
        p.score = score
        p.fit_bucket = bucket
        scored.append(p)

    ranked = sorted(scored, key=lambda x: x.score, reverse=True)
    ranked_for_email = [p for p in ranked if p.fit_bucket != "Skip"]

    return {
        "mode": mode_name,
        "raw_count": len(all_projects),
        "unique_count": len(unique_projects),
        "filtered_count": len(filtered),
        "ranked": ranked_for_email,
    }


def main():
    quick_fix_results = run_mode("quick_fix", QUICK_FIX_QUERIES)
    small_build_results = run_mode("small_build", SMALL_BUILD_QUERIES)

    send_results_email([quick_fix_results, small_build_results])


if __name__ == "__main__":
    main()