import re


def normalize_text(*values):
    """
    Combine multiple values into one lowercase string for matching.
    Safely handles None values.
    """
    parts = [str(v).strip().lower() for v in values if v]
    return " ".join(parts)


def contains_any(text, terms):
    """
    Return True if any term appears in the text.
    """
    text = text.lower()
    return any(term.lower() in text for term in terms)


def passes_currency_filter(project, settings):
    """
    Project currency must be in allowed_currencies.
    """
    allowed = settings.get("allowed_currencies", [])
    if not allowed:
        return True

    return getattr(project, "currency", None) in allowed


def passes_keyword_filter(project, keyword_groups):
    """
    Broad keyword matching for hard filters.
    Use looser terms here so good projects are not rejected too early.
    """
    text = normalize_text(
        getattr(project, "title", ""),
        getattr(project, "description", "")
    )

    broad_keywords = [
        "fix", "bug", "issue", "error", "broken", "debug",
        "css", "html", "responsive", "layout", "mobile",
        "wordpress", "shopify", "frontend", "ui",
        "testing", "audit", "review"
    ]

    return contains_any(text, broad_keywords)


def passes_exclude_terms_filter(project, settings):
    """
    Reject projects containing unwanted terms.
    """
    exclude_terms = settings.get("exclude_terms", [])
    if not exclude_terms:
        return True

    text = normalize_text(
        getattr(project, "title", ""),
        getattr(project, "description", "")
    )

    return not contains_any(text, exclude_terms)


def passes_bid_count_filter(project, settings):
    """
    Optional hard filter for bid count.
    If max_bid_count_hard is not set, do not reject.
    """
    max_bid_count_hard = settings.get("max_bid_count_hard")
    bid_count = getattr(project, "bid_count", None)

    if max_bid_count_hard is None or bid_count is None:
        return True

    return bid_count <= max_bid_count_hard


def passes_basic_quality_filter(project):
    """
    Require a title. Description is optional because some API search
    responses may not include it.
    """
    title = getattr(project, "title", "")

    if not title or not str(title).strip():
        return False

    return True


def passes_hard_filters(project, settings, keyword_groups):
    """
    Main entry point for all hard filtering.
    """
    checks = [
        passes_basic_quality_filter(project),
        passes_currency_filter(project, settings),
        passes_keyword_filter(project, keyword_groups),
        passes_exclude_terms_filter(project, settings),
        passes_bid_count_filter(project, settings),
    ]
    return all(checks)