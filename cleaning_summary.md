# Data Quality Cleaning Summary

| Metric | Raw | Cleaned |
|---|---:|---:|
| Rows | 901 | 889 |
| Columns | 12 | 12 |
| Missing cells | 880 | 0 |
| Exact duplicate rows | 7 | 0 |
| Duplicate PassengerId rows | 22 | 0 |

## What was fixed
- Nulls and null-like markers were inventoried before changes.
- Text whitespace and category representations were standardized.
- Mixed types were converted to appropriate numeric types.
- Impossible Age/Fare values were invalidated.
- Missing fields were handled with field-specific rules.
- Exact duplicates were removed.
- Duplicate primary keys were resolved using record completeness.
- Automated post-cleaning validation passed.
