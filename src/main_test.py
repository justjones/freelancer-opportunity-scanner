from src.client import search_projects
from src.filters import passes_hard_filters
from src.scorer import score_project, assign_fit_bucket
from src.utils import deduplicate_projects
from src.exporter import export_to_csv

from config.keywords import KEYWORD_GROUPS
from config.settings import SETTINGS


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
    "ui bug"
]

SMALL_BUILD_QUERIES = [
    "landing page",
    "figma to html",
    "figma to wordpress",
    "website build",
    "one page website",
    "small business website"
]


def main():
    print("Running scanner...\n")

    # MODE = "quick_fix"   # change to "small_build"
    MODE = "small_build"

    if MODE == "quick_fix":
        queries = QUICK_FIX_QUERIES
    elif MODE == "small_build":
        queries = SMALL_BUILD_QUERIES
    else:
        print("Invalid MODE")
        return

    all_projects = []

    for q in queries:
        print(f"Searching: {q}")
        results = search_projects(q)
        all_projects.extend(results)

    print(f"\nTotal raw results: {len(all_projects)}")

    unique_projects = deduplicate_projects(all_projects)
    print(f"After deduplication: {len(unique_projects)}")

    filtered = [
        p for p in unique_projects
        if passes_hard_filters(p, SETTINGS, KEYWORD_GROUPS)
    ]
    print(f"After filtering: {len(filtered)}\n")

    scored = []
    for p in filtered:
        score = score_project(p, SETTINGS, KEYWORD_GROUPS)
        bucket = assign_fit_bucket(score)

        p.score = score
        p.fit_bucket = bucket
        scored.append(p)

    ranked = sorted(scored, key=lambda x: x.score, reverse=True)
    ranked = [p for p in ranked if p.fit_bucket != "Skip"]

    print("Top Opportunities:\n")

    for p in ranked:
        print(f"[{p.fit_bucket}] ({p.score}) {p.title}")
        print(f"Currency: {p.currency} | Bids: {p.bid_count}")
        print(p.url)
        print("---")

    print(f"Ranked count before export: {len(ranked)}")
    # export_to_csv(ranked)
    export_to_csv(filtered)
    print(f"Filtered count: {len(filtered)}")
    print(f"Ranked count before export: {len(ranked)}")


if __name__ == "__main__":
    main()