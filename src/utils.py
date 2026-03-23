def normalize_text(*values):
    parts = [str(v).strip().lower() for v in values if v]
    return " ".join(parts)


def deduplicate_projects(projects):
    seen = set()
    unique = []

    for p in projects:
        if p.id not in seen:
            seen.add(p.id)
            unique.append(p)

    return unique