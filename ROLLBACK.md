# Rollback Evidence

The raw input is preserved separately from generated outputs.

## Rollback procedure

1. Preserve the current `reports/cleaning_log.csv`.
2. Remove generated files under `data/processed/`.
3. Regenerate the raw working file with:
   `python scripts/make_messy.py`
4. Re-run:
   `python scripts/clean_data.py`
5. Verify with:
   `pytest -q`

The original source/raw data is never overwritten by the cleaning pipeline.
