# Data Cleaning and Preprocessing

Professional, reproducible data-quality pipeline using **Python, pandas, NumPy, Jupyter and Excel**.

## Objective
Clean a raw dataset containing null values, duplicates, inconsistent formats and incorrect data types so it is ready for reliable analysis.

## Dataset
- Dataset: Titanic passenger dataset
- Public reference: https://github.com/datasciencedojo/datasets/blob/master/titanic.csv
- Source size: 891 rows × 12 columns
- Raw working file: `data/raw/titanic_messy.csv`
- Cleaned CSV: `data/processed/titanic_cleaned.csv`
- Cleaned Excel: `data/processed/titanic_cleaned.xlsx`

The raw project file is a reproducible messy working copy. Controlled quality issues were introduced to demonstrate the requested cleaning scenarios.

## Workflow
1. Inventory shape, nulls, duplicates, duplicate keys and data types.
2. Standardize whitespace and categorical formats.
3. Correct data types.
4. Validate numeric ranges.
5. Handle missing values with field-specific rules.
6. Remove exact duplicates.
7. Resolve duplicate primary keys.
8. Re-run quality checks.
9. Export cleaned CSV/XLSX and an audit log.

## Missing-value rules
| Field | Rule | Reason |
|---|---|---|
| PassengerId | Drop missing | Required record key |
| Age | Median by Pclass + Sex, then global median | Preserves subgroup structure |
| Fare | Median by Pclass, then global median | Fare is associated with class |
| Embarked | Mode | Small amount of missing categorical data |
| Cabin | `Unknown` | High missingness; avoid inventing a cabin |

## Duplicate rules
- Exact duplicate rows are removed.
- Duplicate PassengerId groups retain the most complete record.
- Every transformation is documented in `reports/cleaning_log.csv`.

## Outlier rule
Rare values are not automatically deleted. Only values that violate domain constraints are treated as invalid. This project converts negative Fare and impossible Age values to missing before applying the documented missing-value rules.

## Validation
The final dataset is checked for duplicate rows, unique PassengerId, valid categories, valid age/fare ranges, required columns and missing required fields.

## Deliverables
- `data/raw/titanic_messy.csv`
- `data/processed/titanic_cleaned.csv`
- `data/processed/titanic_cleaned.xlsx`
- `reports/cleaning_log.csv`
- `reports/before_after_quality.csv`
- `reports/data_quality_report.md`
- `reports/cleaning_summary.md`
- `reports/interview_questions.md`
- `notebooks/data_cleaning.ipynb`
- `scripts/make_messy.py`
- `scripts/clean_data.py`
- `tests/test_cleaning.py`

## Run locally
```bash
python -m pip install -r requirements.txt
python scripts/make_messy.py
python scripts/clean_data.py
pytest -q
```
