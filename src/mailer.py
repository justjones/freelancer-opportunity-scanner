# src/mailer.py
from pathlib import Path
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")


def build_email_body(mode_results):
    lines = []
    lines.append("Freelancer Opportunity Scanner")
    lines.append("")

    for result in mode_results:
        lines.append(f"Mode: {result['mode']}")
        lines.append(f"Raw results: {result['raw_count']}")
        lines.append(f"After deduplication: {result['unique_count']}")
        lines.append(f"After filtering: {result['filtered_count']}")
        lines.append("")

        if not result["ranked"]:
            lines.append("No ranked opportunities to show. Filtered candidates were found but did not meet scoring thresholds.")
            lines.append("")
            continue

        for p in result["ranked"][:10]:
            lines.append(f"[{p.fit_bucket}] ({p.score}) {p.title}")
            lines.append(f"Currency: {getattr(p, 'currency', '')} | Bids: {getattr(p, 'bid_count', '')}")
            lines.append(getattr(p, "url", ""))
            lines.append("")

        lines.append("-" * 60)
        lines.append("")

    return "\n".join(lines)


def send_results_email(mode_results):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")

    body = build_email_body(mode_results)

    msg = EmailMessage()
    msg["Subject"] = "Freelancer Scanner Results"
    msg["From"] = email_from
    msg["To"] = email_to
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)