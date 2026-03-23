# Core modules
from config.keywords import KEYWORD_GROUPS
from config.settings import SETTINGS

from src.client import search_projects
from src.filters import passes_hard_filters
from src.scorer import score_project, assign_fit_bucket
from src.exporter import export_to_csv
from src.utils import deduplicate_projects

# Utilities
from src.utils import deduplicate_projects
def main():
    print("Starting Freelancer Opportunity Scanner...\n")

    all_projects = []

    # 1. Search projects by keyword groups
    for group_name, terms in KEYWORD_GROUPS.items():
        print(f"Searching group: {group_name}")

        for term in terms:
            print(f"  → Searching: {term}")
            results = search_projects(term)

            if results:
                all_projects.extend(results)

    print(f"\nTotal projects fetched: {len(all_projects)}")

    # 2. Deduplicate
    unique_projects = deduplicate_projects(all_projects)
    print(f"After deduplication: {len(unique_projects)}")

    # 3. Apply hard filters
    filtered_projects = [
        p for p in unique_projects if passes_hard_filters(p, SETTINGS)
    ]
    print(f"After filtering: {len(filtered_projects)}")

    # 4. Score projects
    scored_projects = []
    for project in filtered_projects:
        score = score_project(project, SETTINGS)
        fit_bucket = assign_fit_bucket(score)

        project.score = score
        project.fit_bucket = fit_bucket

        scored_projects.append(project)

    # 5. Sort by score
    ranked_projects = sorted(
        scored_projects,
        key=lambda x: x.score,
        reverse=True
    )

    # 6. Export results
    export_to_csv(ranked_projects)

    # 7. Print top matches
    print("\nTop Opportunities:\n")

    for project in ranked_projects[:10]:
        print(f"[{project.fit_bucket}] ({project.score}) {project.title}")
        print(f"→ {project.url}\n")

    print("Done.\n")


if __name__ == "__main__":
    main()
    
filtered_projects = [
    p for p in unique_projects
    if passes_hard_filters(p, SETTINGS, KEYWORD_GROUPS)
]

scored_projects = []
for project in filtered_projects:
    score = score_project(project, SETTINGS, KEYWORD_GROUPS)
    fit_bucket = assign_fit_bucket(score)

    project.score = score
    project.fit_bucket = fit_bucket
    scored_projects.append(project)
    
import time

start = time.time()
main()
end = time.time()

print(f"Execution time: {round(end - start, 2)} seconds")