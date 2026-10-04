
# 🎧 Vireo Audio Support Insights

An interactive customer-support analytics dashboard built with **Python, Pandas, and Streamlit** to explore weekly support performance, agent workload, SLA compliance, repeat-contact signals, and data quality.

The dashboard transforms support-ticket data into actionable insights while preserving important business-policy rules and highlighting data-quality limitations.

## 🚀 Live Demo

**[Open Vireo Audio Support Insights Dashboard](https://rak-shi-vireo-support-insights-app-mbszfw.streamlit.app/)**

## 📸 Dashboard Screenshots

### 1. Weekly Support Overview

A high-level view of weekly ticket volume, resolved or closed tickets, SLA breach rate, and estimated support costs.

![Weekly Support Overview](screenshots/dashboard-overview.png)

### 2. Weekly Support Digest

Visualizes weekly ticket volume across support channels and assigned teams to help identify workload patterns.

![Weekly Support Digest](screenshots/weekly-digest.png)

### 3. Agent Leaderboard

Displays weekly agent workload, tickets closed, SLA breaches, and response-time metrics. Tier 2 and warranty work should not be ranked by weekly closure volume alone.

![Agent Leaderboard](screenshots/agent-leaderboard.png)

### 4. Repeat Contact Investigation

Highlights potential repeat contacts based on customer, product SKU, category, and the 30-day window after a previous ticket's resolution. These cases are candidates for human review, not confirmed repeat issues.

![Repeat Contact Investigation](screenshots/repeat-contacts.png)

### 5. Data Quality and Assumptions

Summarizes source rows, distinct ticket IDs, repeated ticket-ID groups, and key data-quality considerations.

![Data Quality and Assumptions](screenshots/data-quality.png)

## ✨ Key Features

- **Weekly Support Overview:** Track incoming tickets, resolutions, SLA breaches, and estimated contact costs.
- **Channel Analysis:** Compare ticket volumes across chat, email, voice, and social channels.
- **Team Workload Analysis:** Understand ticket distribution across assigned support teams.
- **Agent Leaderboard:** Review workload and operational metrics for eligible agents.
- **Repeat Contact Signals:** Identify potential repeat contacts for further investigation.
- **Data Quality Monitoring:** Highlight repeated ticket IDs and potential source-data inconsistencies.
- **Interactive Filters:** Filter dashboard results by calendar week and assigned team.
- **Policy-Aware Reporting:** Apply channel-specific contact costs and SLA targets.
- **Data Transparency:** Preserve repeated ticket records for review rather than silently removing them.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and application logic |
| Streamlit | Interactive dashboard interface |
| Pandas | Data cleaning, transformation, and analysis |
| Matplotlib | Data visualization |
| Git and GitHub | Version control and source-code hosting |
| Streamlit Community Cloud | Dashboard deployment |

## 📊 Business Rules and Policy Considerations

### Contact Cost

The policy's blended reference contact cost is **₹290 per contact**. Channel-specific rates are used when estimating contact costs.

| Channel | Cost per Contact |
|---|---:|
| Chat | ₹210 |
| Email | ₹260 |
| Voice | ₹520 |
| Social | ₹240 |

The blended rate is a reference value; channel-specific estimates use the applicable channel rate.

### Service-Level Agreement (SLA)

The dashboard uses the following first-response targets:

| Channel | First-Response Target |
|---|---:|
| Chat | 15 minutes |
| Voice | 2 hours |
| Social | 4 hours |
| Email | 8 hours |

A missed SLA creates a **₹350 credit at resolution**, according to the supplied policy. SLA performance should be interpreted using the applicable channel target.

### Agent Performance

- The agent leaderboard is intended as a weekly workload view, not a standalone performance assessment.
- Tier 2 Escalations and Warranty work should not be ranked by weekly ticket closures alone.
- Resolution time and relevant case complexity should be considered when assessing these teams.

### Repeat Contacts

A repeat contact is defined by the policy as the same customer contacting support about the same issue within 30 days after resolution.

The dashboard identifies **potential repeat-contact candidates** using available customer, product, category, and timestamp fields. These fields do not prove that two contacts concern the identical issue, so flagged cases require review.

### Data Quality

- Repeated ticket IDs are flagged rather than automatically removed.
- Legacy helpdesk migration records may overlap with newer records and may contain conflicting values.
- Blank or legacy zero CSAT values are treated as no response.
- Timestamps are interpreted in Indian Standard Time (IST).

## 📁 Project Structure

```text
vireo-support-insights/
├── data/
│   ├── tickets.csv
│   ├── agents.csv
│   ├── customers.csv
│   ├── orders.csv
│   ├── products.csv
│   └── support-policy.pdf
├── screenshots/
│   ├── dashboard-overview.png
│   ├── weekly-digest.png
│   ├── agent-leaderboard.png
│   ├── repeat-contacts.png
│   └── data-quality.png
├── app.py
├── analysis.py
├── check_duplicates.py
├── requirements.txt
├── .gitignore
└── README.md
```

*The structure above describes the expected project layout. Filenames in `data/` and `screenshots/` should match the files actually present in your repository.*

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11 or later
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/rak-shi/vireo-support-insights.git
cd vireo-support-insights
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the dashboard

```bash
streamlit run app.py
```

The terminal will display a local URL, usually `http://localhost:8501`. Open it in your browser to use the dashboard.

## ▶️ How to Use the Dashboard

1. Open the dashboard.
2. Select a week using the **Week starting** filter.
3. Choose an assigned team or leave the filter set to all teams.
4. Review the weekly support metrics and charts.
5. Open the **Agent leaderboard** tab to inspect workload and response metrics.
6. Open **Repeat contacts** to review potential repeat-contact candidates.
7. Open **Data quality** to inspect repeated ticket IDs and data-quality assumptions.

## 🔍 Data Quality Approach

The dashboard distinguishes between source records and distinct ticket IDs. This is important because migration-related records can share a ticket ID while containing different values.

Rather than silently deleting records, the analysis flags repeated IDs so that discrepancies can be reviewed. Repeat-contact indicators are also presented as candidate cases instead of confirmed same-issue contacts.

## 🔮 Possible Future Improvements

- Add date-range comparisons and trend analysis.
- Add downloadable weekly reports.
- Introduce richer repeat-contact matching using ticket-message similarity.
- Add filters for support channel, issue category, and agent tier.
- Add automated data-validation tests.
- Improve reporting on SLA credits and operational costs.
- Add authentication if the dashboard is used with non-public business data.

## 👩‍💻 Author

**Rakshitha Valipireddy**

- GitHub: [rak-shi](https://github.com/rak-shi)
- LinkedIn: [Rakshitha Valipireddy](https://www.linkedin.com/in/rakshitha-valipireddy-68694b210/)

---

*Built as a support analytics project focused on operational visibility, policy-aware metrics, and transparent data-quality handling.*
