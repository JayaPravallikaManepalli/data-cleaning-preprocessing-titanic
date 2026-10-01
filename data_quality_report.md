# Data Quality Report

## Before cleaning

- Rows: **901**
- Columns: **12**
- Missing cells: **880**
- Exact duplicate rows: **7**
- Duplicate PassengerId rows: **22**

## After cleaning

- Rows: **889**
- Columns: **12**
- Missing cells: **0**
- Exact duplicate rows: **0**
- Duplicate PassengerId rows: **0**

## Automated checks

- [x] `no_exact_duplicate_rows`
- [x] `unique_passenger_id`
- [x] `no_missing_passenger_id`
- [x] `survived_binary`
- [x] `pclass_valid`
- [x] `sex_valid`
- [x] `embarked_valid`
- [x] `age_valid`
- [x] `fare_nonnegative`
- [x] `required_columns_present`
