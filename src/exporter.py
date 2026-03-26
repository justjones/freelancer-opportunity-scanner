import csv
from pathlib import Path


def export_to_csv(projects, filename="freelancer_opportunities.csv"):
    output_dir = Path("output/reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / filename

    print(f"Exporting {len(projects)} projects to: {file_path.resolve()}")

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "title",
            "score",
            "fit_bucket",
            "currency",
            "bid_count",
            "matched_keywords",
            "url"
        ])

        for p in projects:
            writer.writerow([
                getattr(p, "title", ""),
                getattr(p, "score", ""),
                getattr(p, "fit_bucket", ""),
                getattr(p, "currency", ""),
                getattr(p, "bid_count", ""),
                 ", ".join(getattr(p, "matched_keywords", [])),
                getattr(p, "url", "")
            ])

    print("CSV export complete.\n")