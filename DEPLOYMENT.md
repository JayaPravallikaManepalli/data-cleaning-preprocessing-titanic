# Deployment Configuration

This project is designed as a reproducible batch-cleaning pipeline rather than a web service.

## Run

```bash
python -m pip install -r requirements.txt
python scripts/make_messy.py
python scripts/clean_data.py
pytest -q
```

The cleaning script fails fast if a quality assertion fails.

## Outputs

- `data/processed/titanic_cleaned.csv`
- `data/processed/titanic_cleaned.xlsx`
- `reports/cleaning_log.csv`
