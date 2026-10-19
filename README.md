# Financial Performance & Transformation

**Portfolio case study — Jordan Boucetta**

Reproducible Python project demonstrating finance reporting automation, data quality controls, and budget-versus-actual analysis using **entirely fictional** data.

## Business question
How can a finance team automate monthly budget/actual variance reporting by department and expense/revenue category?

## Features
- Generate 12 months × 5 departments × 5 categories = **300 fictional records**.
- Validate unique reporting keys, missing values and non-negative amounts.
- Compute EUR and percentage variances.
- Export detailed and aggregated CSV reports.
- Produce a monthly budget-vs-actual chart.
- Run unit tests and the complete pipeline automatically with GitHub Actions.

## Run locally
```bash
python -m pip install -r requirements.txt
python -m unittest tests.py -v
python finance_pipeline.py --seed 42
```

## Generated outputs
- `data/fictional_finance.csv` — input data.
- `reports/budget_vs_actual_detail.csv` — row-level variance analysis.
- `reports/department_variances.csv` — department/category aggregation.
- `images/monthly_budget_actual.png` — chart.

GitHub Actions publishes generated outputs as a downloadable artifact named `finance-transformation-demo` after successful runs.

## Definitions and limitations
`variance_eur = actual_eur - budget_eur`. A positive variance is not necessarily favorable; its interpretation depends on whether the item is revenue or cost. This is a demonstrative reporting workflow, **not a real client project**. No confidential or employer financial information is used.

See [data dictionary](data_dictionary.md).
