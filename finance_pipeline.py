"""Fictional financial reporting: monthly budget vs actual, variance analysis."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DEPARTMENTS = ["Retail", "Corporate", "Operations", "Technology", "Compliance"]
CATEGORIES = ["Revenue", "Personnel", "IT", "External services", "Facilities"]

def generate_data(seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for month in pd.date_range("2025-01-01", periods=12, freq="MS"):
        for dept in DEPARTMENTS:
            for category in CATEGORIES:
                baseline = 200000 if category == "Revenue" else 65000
                budget = round(baseline * rng.uniform(.75, 1.25), 2)
                actual = round(budget * rng.uniform(.80, 1.22), 2)
                rows.append((month.strftime("%Y-%m"), dept, category, budget, actual))
    return pd.DataFrame(rows, columns=["month", "department", "category", "budget_eur", "actual_eur"])

def analyze(df):
    if df.duplicated(["month", "department", "category"]).any():
        raise ValueError("Duplicate month/department/category keys")
    if df[["budget_eur", "actual_eur"]].isna().any().any():
        raise ValueError("Missing financial amounts")
    if (df[["budget_eur", "actual_eur"]] < 0).any().any():
        raise ValueError("Negative amounts")
    report = df.copy()
    report["variance_eur"] = (report.actual_eur - report.budget_eur).round(2)
    report["variance_pct"] = (report.variance_eur / report.budget_eur * 100).round(2)
    return report

def run(seed=42):
    base = Path(__file__).resolve().parent
    for folder in ["data", "reports", "images"]:
        (base / folder).mkdir(exist_ok=True)
    df = generate_data(seed)
    report = analyze(df)
    df.to_csv(base / "data" / "fictional_finance.csv", index=False)
    report.to_csv(base / "reports" / "budget_vs_actual_detail.csv", index=False)
    summary = report.groupby(["department", "category"], as_index=False)[["budget_eur", "actual_eur", "variance_eur"]].sum()
    summary["variance_pct"] = (summary.variance_eur / summary.budget_eur * 100).round(2)
    summary.to_csv(base / "reports" / "department_variances.csv", index=False)
    monthly = report.groupby("month")[["budget_eur", "actual_eur"]].sum()
    ax = monthly.plot(kind="bar", figsize=(11, 5), title="Budget vs actual — fictional financial data")
    ax.set_ylabel("EUR")
    ax.figure.tight_layout()
    ax.figure.savefig(base / "images" / "monthly_budget_actual.png", dpi=160)
    plt.close(ax.figure)
    print(f"Generated {len(report)} synthetic rows; total variance: EUR {report.variance_eur.sum():,.2f}")
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    run(parser.parse_args().seed)
