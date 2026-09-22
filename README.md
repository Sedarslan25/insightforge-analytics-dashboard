# InsightForge Analytics Dashboard

A dependency-free Python mini-project that turns a customer-retention CSV into a clean HTML analytics report. It demonstrates CSV handling, exploratory metrics, prioritisation logic, and report generation using only the Python standard library.

**Kısa Türkçe özet:** Örnek müşteri verisini analiz edip churn oranlarını ve takip önceliklerini HTML raporuna dönüştüren Python projesi.

## What it analyses

- Overall customer count, churn rate, and average usage
- Churn rate segmented by subscription plan
- Follow-up candidates ranked by support tickets and usage

## Run

```bash
python app.py
```

The command creates `reports/retention_report.html`. Open that file in any browser.

## Data note

`data/customer_retention.csv` contains a small, fully synthetic data set for demonstration. The follow-up ranking is an explanatory heuristic—not a real-world prediction model or business decision system.
