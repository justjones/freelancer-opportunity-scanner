# Freelancer Opportunity Scanner

A Python-based automation tool that searches Freelancer.com for relevant projects, filters and ranks them based on custom criteria, and delivers a curated shortlist via email.

## Project Summary

Freelancer Opportunity Scanner is a Python-based automation tool designed to streamline the process of finding high-quality freelance work. Instead of manually browsing job listings, the tool automatically searches, filters, and ranks projects based on relevance, then delivers a curated shortlist via email.

The system applies a structured decision pipeline using keyword analysis, scoring logic, and filtering rules to prioritize opportunities that align with frontend development and QA-focused work. This project reflects a practical approach to automation, combining real-world problem solving with clean, maintainable code.

## Overview

This project was built to reduce the time spent manually searching freelance platforms and to focus only on high-quality opportunities.

The scanner:
- Queries Freelancer.com using multiple targeted search terms
- Deduplicates results across searches
- Applies hard filters (currency, keywords, bid count, etc.)
- Scores each project based on relevance
- Categorizes results into:
  - Strong fit
  - Possible fit
  - Skip
- Sends a daily email with the top opportunities

## Features

- Multi-query search (quick fixes and small builds)
- Custom filtering pipeline
- Scoring system with positive and negative signals
- Keyword-based relevance tracking
- Email delivery using SMTP
- Scheduled execution via Windows Task Scheduler
- Optional CSV export for review/debugging

## Project Structure
│
├── src/
│ ├── main.py # Entry point
│ ├── client.py # API calls to Freelancer
│ ├── filters.py # Hard filtering logic
│ ├── scorer.py # Scoring + ranking
│ ├── utils.py # Helpers (deduplication, normalization)
│ ├── exporter.py # CSV export
│ └── mailer.py # Email sending logic
│
├── config/
│ ├── keywords.py # Keyword groups
│ └── settings.py # Filters + scoring settings
│
├── output/
│ ├── logs/
│ └── reports/
│
├── .env # Secrets (not committed)
├── .env.example # Template for environment variables
├── requirements.txt
└── run_scanner.bat # Scheduled execution script


## How It Works

1. The scanner runs multiple search queries (e.g., "css fix", "website bug", etc.)
2. Results are combined and deduplicated
3. Hard filters remove:
   - unwanted currencies
   - irrelevant keywords
   - high-bid projects
4. Remaining projects are scored using:
   - positive signals (fix, bug, testing, etc.)
   - negative signals (assistant roles, maintenance, etc.)
   - bid count and budget
5. Projects are categorized into fit buckets
6. Top results are emailed

## Setup

### 1. Clone the repo
git clone https://github.com/yourusername/freelancer-opportunity-scanner.git


### 2. Install dependencies
pip install -r requirements.txt


### 3. Configure environment variables

Create a `.env` file:

### 3. Configure environment variables

Create a `.env` file:

FREELANCER_API_TOKEN=your_token_here

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com

SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com

EMAIL_TO=your_email@gmail.com


### 4. Run manually
python -m src.main


## Scheduling

This project is designed to run automatically using Windows Task Scheduler.

Example schedule:
- 9:00 AM
- 1:00 PM
- 5:00 PM

The `run_scanner.bat` file handles execution:

cd /d C:\Dev\freelancer-opportunity-scanner
python -m src.main


## Output

### Email

Each run sends an email containing:

- Summary statistics
- Top ranked opportunities
- Quick Fix and Small Build results

### CSV (optional)

- `filtered` → broader review pool
- `ranked` → scored shortlist

## Scoring Strategy

Projects are ranked using a weighted scoring system:

### Positive signals
- fix, bug, error, debug
- css, responsive, layout
- testing, audit
- wordpress, shopify

### Negative signals
- assistant, maintenance, ongoing work
- content updates
- large rebuilds or enterprise projects

### Additional factors
- bid count (lower preferred)
- budget alignment
- keyword group matches

## Modes

The scanner runs two modes:

### Quick Fix Mode
Targets:
- bug fixes
- UI issues
- small troubleshooting tasks

### Small Build Mode
Targets:
- landing pages
- Figma conversions
- small website builds

## Future Improvements

- Track previously seen projects to avoid duplicates across runs
- Improve scoring with keyword weighting by mode
- Add logging dashboard
- Support additional freelance platforms (Upwork, etc.)

## Notes

This project was built to support a QA-focused freelancer workflow by prioritizing:
- clarity
- repeatability
- decision efficiency

## License

MIT

