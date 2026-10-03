
# Vireo Audio Support Insights Dashboard

An interactive support analytics dashboard built with Python and Streamlit to analyze customer support tickets, monitor SLA performance, identify repeat contacts, and understand agent workload.

## Project Overview

This project transforms customer support ticket data into actionable insights through an interactive dashboard. It provides weekly support summaries, agent performance metrics, repeat-contact signals, and data quality checks.

## Features

- **Weekly Support Digest:** View ticket volumes, resolution trends, SLA breaches, and support costs.
- **Agent Leaderboard:** Analyze agent workload and support metrics while respecting team-specific ranking restrictions.
- **Repeat Contact Analysis:** Identify potential repeat contacts from the same customer for similar issues within a 30-day window after resolution.
- **SLA Monitoring:** Compare first-response times against channel-specific SLA targets.
- **Support Cost Analysis:** Compare channel-specific contact costs with the blended reference cost.
- **Data Quality Checks:** Inspect duplicate ticket IDs, missing fields, and other data quality issues.

## Live Demo

Explore the deployed dashboard here:

**[Vireo Audio Support Insights Dashboard](https://rak-shi-vireo-support-insights-app-mbszfw.streamlit.app/)**

The dashboard provides interactive weekly support analytics, agent workload metrics, repeat-contact investigation, and data quality reporting.

## Technology Stack

- Python
- Streamlit
- Pandas
- Matplotlib
- Git and GitHub

## Repository Structure

```text
vireo-support-insights/
├── app.py
├── analysis.py
├── check_duplicates.py
├── requirements.txt
├── data/
│   ├── tickets.csv
│   ├── agents.csv
│   ├── customers.csv
│   ├── orders.csv
│   └── products.csv
├── support-policy.pdf
└── README.md
```

The files listed under `data/` and `support-policy.pdf` should be present only if they are included in your local project.

## Prerequisites

- Python 3.11 or later
- pip

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/rak-shi/vireo-support-insights.git
cd vireo-support-insights
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the dashboard

```powershell
streamlit run app.py
```

Streamlit will provide a local URL in the terminal, usually:

`http://localhost:8501`

## Support Policy Reference

The dashboard uses the following assignment-provided reference values:

| Metric | Value |
|---|---:|
| Blended contact cost | ₹290 per contact |
| Chat contact cost | ₹210 |
| Email contact cost | ₹260 |
| Social contact cost | ₹240 |
| Voice contact cost | ₹520 |
| SLA credit for a missed target | ₹350 |

First-response SLA targets:

| Channel | Target |
|---|---:|
| Chat | 15 minutes |
| Voice | 2 hours |
| Social | 4 hours |
| Email | 8 hours |

A zero or blank CSAT score is treated as no response. Migration-related duplicate ticket IDs are reviewed rather than automatically treated as separate contacts.

## Data Handling Notes

- Ticket IDs may occur more than once due to legacy-system migration.
- Repeat contacts are treated as potential signals and should be interpreted in context.
- Tier 2 Escalations and Warranty teams should not be ranked by weekly ticket closures.
- Timestamps are interpreted in Indian Standard Time (IST).
- Do not publish customer personal information or confidential data.

## Running the Analysis Script

To print the analysis and data quality summary, run:

```powershell
python analysis.py
```

## Author

**Rakshitha Valipireddy**

GitHub: [rak-shi](https://github.com/rak-shi)

## Disclaimer

This project was developed for support analytics and learning purposes using the Vireo Audio Support Tickets assignment dataset. Results depend on the supplied data and the assumptions documented in the project.
