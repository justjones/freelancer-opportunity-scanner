from src.utils import normalize_text


def score_keyword_group_matches(project, keyword_groups):
    text = normalize_text(project.title, project.description)
    score = 0
    matched_keywords = []

    group_weights = {
        "frontend_ui_fixes": 14,
        "website_troubleshooting": 14,
        "wordpress_adjustments": 10,
        "shopify_ecommerce_fixes": 10,
        "qa_testing": 18,
        "website_build": 10,
    }

    for group_name, terms in keyword_groups.items():
        matches = [term for term in terms if term.lower() in text]
        if matches:
            score += group_weights.get(group_name, 10)
            matched_keywords.extend(matches)

    return score, matched_keywords


def score_term_matches(title_text, body_text, rules):
    score = 0

    for term, points in rules.items():
        if term in title_text:
            score += points
        elif term in body_text:
            score += int(points * 0.6)

    return score


def score_positive_signals(project):
    title_text = normalize_text(project.title)
    body_text = normalize_text(project.description)

    positive_rules = {
        "fix": 18,
        "bug": 18,
        "issue": 14,
        "error": 16,
        "broken": 16,
        "debug": 16,
        "not working": 20,
        "troubleshoot": 16,
        "troubleshooting": 16,

        "css": 14,
        "html": 12,
        "responsive": 14,
        "layout": 12,
        "mobile": 10,
        "frontend": 12,
        "ui": 10,

        "wordpress": 10,
        "shopify": 10,

        "testing": 18,
        "manual testing": 22,
        "ui testing": 22,
        "website audit": 20,
        "audit": 16,
        "review": 10,

        "landing page": 10,
        "figma to html": 14,
        "figma to wordpress": 14,
        "one page website": 8,
    }

    return score_term_matches(title_text, body_text, positive_rules)


def score_negative_signals(project, settings):
    title_text = normalize_text(project.title)
    body_text = normalize_text(project.description)

    negative_rules = {
        "assistant": -14,
        "virtual assistant": -18,
        "ongoing": -10,
        "long term": -12,
        "maintenance": -12,
        "general website maintenance": -16,
        "content updates": -14,
        "uploading blog posts": -14,
        "replacing images": -10,
        "replacing text": -10,
        "data entry": -18,

        "divi": -10,
        "divi builder": -12,

        "full website": -16,
        "complete rebuild": -18,
        "enterprise": -16,
        "saas platform": -18,
        "android app": -18,
        "ios app": -18,
        "mobile app": -18,
        "backend": -12,
        "laravel": -10,
        "django": -10,
        "node.js": -10,
        "react native": -12,

        "agency": -10,
        "team of developers": -14,
        "long term team": -14,
    }

    return score_term_matches(title_text, body_text, negative_rules)


def score_budget(project, settings):
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
    bid_count = getattr(project, "bid_count", None)
    if bid_count is None:
        return 0

    if bid_count <= 5:
        return 15
    if bid_count <= 10:
        return 10
    if bid_count <= 20:
        return 5
    if bid_count <= 40:
        return 0

    return -8


def score_project(project, settings, keyword_groups):
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
    if score >= 55:
        return "Strong fit"
    if score >= 30:
        return "Possible fit"
    return "Skip"