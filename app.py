"""A dependency-free customer retention analytics demo.

Run `python app.py` to analyse the sample data and create a shareable HTML report.
"""

from __future__ import annotations

import csv
import html
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "customer_retention.csv"
REPORT_FILE = ROOT / "reports" / "retention_report.html"


def load_customers(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def analyse(rows: list[dict[str, str]]) -> dict[str, object]:
    total = len(rows)
    churned = [row for row in rows if row["churned"] == "yes"]
    plans = Counter(row["plan"] for row in rows)
    plan_churn = {
        plan: sum(row["churned"] == "yes" for row in rows if row["plan"] == plan)
        / count
        for plan, count in plans.items()
    }
    at_risk = sorted(
        rows,
        key=lambda row: (int(row["support_tickets"]), -int(row["usage_hours"])),
        reverse=True,
    )[:3]
    return {
        "total": total,
        "churn_rate": len(churned) / total,
        "average_usage": statistics.mean(int(row["usage_hours"]) for row in rows),
        "plan_churn": plan_churn,
        "at_risk": at_risk,
    }


def build_report(result: dict[str, object]) -> str:
    plan_rows = "".join(
        f"<tr><td>{html.escape(plan.title())}</td><td>{percent(rate)}</td></tr>"
        for plan, rate in sorted(result["plan_churn"].items())
    )
    risk_rows = "".join(
        "<tr>"
        f"<td>{html.escape(row['customer_id'])}</td>"
        f"<td>{html.escape(row['plan'])}</td>"
        f"<td>{html.escape(row['usage_hours'])}</td>"
        f"<td>{html.escape(row['support_tickets'])}</td>"
        "</tr>"
        for row in result["at_risk"]
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>InsightForge Retention Report</title>
<style>
body{{font-family:Arial,sans-serif;background:#f6f8fc;color:#17233b;margin:0;padding:40px}}main{{max-width:920px;margin:auto}}
.eyebrow{{color:#5669d8;font-weight:700;letter-spacing:.08em}}h1{{font-size:42px;margin:8px 0}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:28px 0}}
.card,section{{background:#fff;border:1px solid #e3e8f4;border-radius:16px;padding:20px;box-shadow:0 8px 25px #1b31500c}}.metric{{font-size:30px;font-weight:bold;color:#4054c8}}section{{margin-top:18px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:12px;text-align:left;border-bottom:1px solid #edf0f6}}th{{color:#68748b;font-size:12px;text-transform:uppercase}}
@media(max-width:600px){{body{{padding:20px}}.grid{{grid-template-columns:1fr}}}}
</style></head><body><main><p class="eyebrow">SYNTHETIC DATA DEMO</p><h1>Customer Retention Snapshot</h1><p>Generated from the sample CSV included in this repository.</p>
<div class="grid"><div class="card"><small>Customers</small><div class="metric">{result['total']}</div></div><div class="card"><small>Churn rate</small><div class="metric">{percent(result['churn_rate'])}</div></div><div class="card"><small>Average monthly usage</small><div class="metric">{result['average_usage']:.1f}h</div></div></div>
<section><h2>Churn by plan</h2><table><thead><tr><th>Plan</th><th>Churn rate</th></tr></thead><tbody>{plan_rows}</tbody></table></section>
<section><h2>Follow-up candidates</h2><p>Sorted by support-ticket count, then low product usage. This is an exploratory heuristic, not a production prediction model.</p><table><thead><tr><th>Customer</th><th>Plan</th><th>Usage hours</th><th>Tickets</th></tr></thead><tbody>{risk_rows}</tbody></table></section>
</main></body></html>"""


def main() -> None:
    rows = load_customers(DATA_FILE)
    result = analyse(rows)
    REPORT_FILE.parent.mkdir(exist_ok=True)
    REPORT_FILE.write_text(build_report(result), encoding="utf-8")
    print("InsightForge analytics completed")
    print(f"Customers: {result['total']}")
    print(f"Churn rate: {percent(result['churn_rate'])}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()
