def normalize_text(*values):
    """
    Combine multiple values into one lowercase string for matching.
    """
    parts = [str(v).strip().lower() for v in values if v]
    return " ".join(parts)


def count_matches(text, terms):
    """
    Count how many terms appear in text.
    """
    text = text.lower()
    return sum(1 for term in terms if term.lower() in text)


def score_keyword_group_matches(project, keyword_groups):
    """
    Score based on keyword group matches in title/description.
    """
    text = normalize_text(project.title, project.description)
    score = 0
    matched_keywords = []

    group_weights = {
        "frontend_ui_fixes": 15,
        "website_troubleshooting": 15,
        "wordpress_adjustments": 10,
        "shopify_ecommerce_fixes": 10,
        "qa_testing": 20,
        "website_build": 20,
    }

    for group_name, terms in keyword_groups.items():
        matches = [term for term in terms if term.lower() in text]
        if matches:
            score += group_weights.get(group_name, 10)
            matched_keywords.extend(matches)

    return score, matched_keywords


def score_positive_signals(project):
    """
    Extra scoring for strong-fit language.
    """
    text = normalize_text(project.title, project.description)

    score = 0

    positive_rules = {
    "fix": 20,
    "bug": 18,
    "error": 18,
    "debug": 18,
    "broken": 18,
    "not working": 20,
    "responsive": 12,
    "css": 12,
    "layout": 10,
    "frontend": 10,
    "testing": 20,
    "audit": 16,
    "website":20,
    "figma": 20,
    "landing page": 20,
}

    for term, points in positive_rules.items():
        if term in text:
            score += points

    return score


def score_negative_signals(project, settings):
    """
    Deduct points for poor-fit language.
    """
    text = normalize_text(project.title, project.description)
    score = 0

    negative_rules = {
    "long term": -10,
    "ongoing": -8,
    "assistant": -12,
    "general website maintenance": -12,
    "uploading blog posts": -12,
    "replacing images": -8,
    "content updates": -10,
    "divi builder": -10,
    "divi": -8,
    "virtual assistant": -12,
}

    for term, points in negative_rules.items():
        if term in text:
            score += points

    return score


def score_budget(project, settings):
    """
    Prefer smaller, quicker-win opportunities.
    """
    preferred_budget_max = settings.get("preferred_budget_max")
    min_budget = getattr(project, "min_budget", None)
    max_budget = getattr(project, "max_budget", None)

    if preferred_budget_max is None:
        return 0

    if max_budget is not None and max_budget <= preferred_budget_max:
        return 10

    if min_budget is not None and min_budget <= preferred_budget_max:
        return 5

    return 0


def score_bid_count(project, settings):
    """
    Lower bid counts are generally better.
    """
    bid_count = getattr(project, "bid_count", None)
    if bid_count is None:
        return 0

    if bid_count <= 5:
        return 15
    if bid_count <= 10:
        return 10
    if bid_count <= 20:
        return 5

    return -5


def score_project(project, settings, keyword_groups):
    """
    Main scoring function.
    Returns a numeric score and attaches matched keywords if desired.
    """
    total_score = 0

    keyword_score, matched_keywords = score_keyword_group_matches(project, keyword_groups)
    total_score += keyword_score
    total_score += score_positive_signals(project)
    total_score += score_negative_signals(project, settings)
    total_score += score_budget(project, settings)
    total_score += score_bid_count(project, settings)

    project.matched_keywords = matched_keywords
    return total_score


def assign_fit_bucket(score):
    """
    Convert numeric score into a fit label.
    """
    if score >= 70:
        return "Strong fit"
    if score >= 45:
        return "Possible fit"
    return "Skip"