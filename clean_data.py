from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/titanic_messy.csv"
OUT = ROOT / "data/processed/titanic_cleaned.csv"
XLSX = ROOT / "data/processed/titanic_cleaned.xlsx"
LOG = ROOT / "reports/cleaning_log.csv"

df = pd.read_csv(
    RAW,
    keep_default_na=False,
    na_values=["", "NA", "N/A", "null", "NULL", "None", "none", "-"]
)

log = []

def record(issue, rule, before, after, impact, rationale):
    log.append({
        "issue": issue,
        "rule_applied": rule,
        "before": before,
        "after": after,
        "impact": impact,
        "rationale": rationale
    })

# 1. Standardize whitespace
for c in df.select_dtypes(include="object").columns:
    df[c] = df[c].map(lambda x: x.strip() if isinstance(x, str) else x)

record(
    "Whitespace",
    "Strip leading/trailing whitespace",
    "Text fields contained surrounding spaces",
    "Whitespace removed",
    "No row loss",
    "Prevents false category splits."
)

# 2. Standardize categorical values
df["Sex"] = (
    df["Sex"].astype("string").str.strip().str.lower()
    .map({"male": "male", "m": "male", "female": "female", "f": "female"})
)

df["Embarked"] = (
    df["Embarked"].astype("string").str.strip().str.lower()
    .map({
        "s": "S", "southampton": "S",
        "c": "C", "cherbourg": "C",
        "q": "Q", "queenstown": "Q"
    })
)

record(
    "Categorical inconsistency",
    "Normalize case, abbreviations and full names",
    "Mixed category representations",
    "Canonical categories",
    "No row loss",
    "Makes grouping and validation deterministic."
)

# 3. Correct data types
df["Pclass"] = pd.to_numeric(
    df["Pclass"].astype(str).str.extract(r"(\d+)", expand=False),
    errors="coerce"
)

df["Survived"] = pd.to_numeric(
    df["Survived"].astype(str).str.lower().replace({"yes": 1, "no": 0}),
    errors="coerce"
)

for c in ["PassengerId", "Age", "SibSp", "Parch", "Fare"]:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(r"[^0-9.\-]", "", regex=True),
        errors="coerce"
    )

record(
    "Incorrect data types",
    "Convert mixed text/numeric fields to numeric",
    "Mixed representations such as Class 3, Yes and $7.25",
    "Numeric types established",
    "No row loss",
    "Required for calculations and validation."
)

# 4. Validate numeric ranges
bad_age = df["Age"].notna() & ~df["Age"].between(0, 100)
bad_fare = df["Fare"].notna() & (df["Fare"] < 0)

df.loc[bad_age, "Age"] = np.nan
df.loc[bad_fare, "Fare"] = np.nan

record(
    "Invalid numeric values",
    "Set impossible Age/Fare values to missing",
    f"{int(bad_age.sum())} invalid ages; {int(bad_fare.sum())} invalid fares",
    "Invalid values became NaN",
    "Handled by imputation rules",
    "Prevents impossible observations from entering analysis."
)

# 5. Text normalization
df["Name"] = df["Name"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
df["Ticket"] = df["Ticket"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip().str.upper()

record(
    "Text consistency",
    "Collapse repeated whitespace and standardize ticket case",
    "Extra spaces and mixed case",
    "Canonical text formatting",
    "No row loss",
    "Improves matching and readability."
)

# 6. Missing primary key
missing_id = int(df["PassengerId"].isna().sum())
df = df.dropna(subset=["PassengerId"]).copy()

record(
    "Missing primary key",
    "Drop rows without PassengerId",
    missing_id,
    f"{missing_id} rows removed",
    "Rows removed",
    "A primary key is required for record identity."
)

# 7. Missing Embarked
emb_missing = int(df["Embarked"].isna().sum())
emb_mode = df["Embarked"].mode().iloc[0]
df["Embarked"] = df["Embarked"].fillna(emb_mode)

record(
    "Missing Embarked",
    "Mode imputation",
    emb_missing,
    f"Filled with {emb_mode}",
    "No row loss",
    "Small amount of categorical missingness."
)

# 8. Missing Cabin
cabin_missing = int(df["Cabin"].isna().sum())
df["Cabin"] = df["Cabin"].fillna("Unknown")

record(
    "Missing Cabin",
    "Use explicit Unknown category",
    cabin_missing,
    "Unknown",
    "No row loss",
    "Avoids fabricating cabin information."
)

# 9. Missing Age
age_missing = int(df["Age"].isna().sum())
df["Age"] = (
    df["Age"]
    .fillna(df.groupby(["Pclass", "Sex"])["Age"].transform("median"))
    .fillna(df["Age"].median())
)

record(
    "Missing Age",
    "Median by Pclass + Sex, then global median",
    age_missing,
    int(df["Age"].isna().sum()),
    "No row loss",
    "Context-aware imputation preserves subgroup structure."
)

# 10. Missing Fare
fare_missing = int(df["Fare"].isna().sum())
df["Fare"] = (
    df["Fare"]
    .fillna(df.groupby("Pclass")["Fare"].transform("median"))
    .fillna(df["Fare"].median())
)

record(
    "Missing Fare",
    "Median by Pclass, then global median",
    fare_missing,
    int(df["Fare"].isna().sum()),
    "No row loss",
    "Fare is associated with passenger class."
)

# 11. Exact duplicates
exact_dups = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

record(
    "Exact duplicates",
    "Remove exact duplicate rows",
    exact_dups,
    0,
    f"{exact_dups} rows removed",
    "Prevents double-counting identical records."
)

# 12. Duplicate primary keys
dup_keys = int(df["PassengerId"].duplicated(keep=False).sum())

if dup_keys:
    df["_completeness"] = df.notna().sum(axis=1)
    df = (
        df.sort_values(["PassengerId", "_completeness"], ascending=[True, False])
        .drop_duplicates("PassengerId", keep="first")
        .drop(columns="_completeness")
    )

record(
    "Duplicate primary keys",
    "Keep most complete record per PassengerId",
    dup_keys,
    0,
    "One canonical record per key",
    "Uses a transparent completeness rule for conflicting copies."
)

# 13. Final data types and column order
expected = [
    "PassengerId", "Survived", "Pclass", "Name", "Sex",
    "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"
]

df["PassengerId"] = df["PassengerId"].astype("int64")
df["Survived"] = df["Survived"].astype("int64")
df["Pclass"] = df["Pclass"].astype("int64")
df["SibSp"] = df["SibSp"].astype("int64")
df["Parch"] = df["Parch"].astype("int64")
df["Age"] = df["Age"].astype("float64")
df["Fare"] = df["Fare"].astype("float64")
df["Sex"] = df["Sex"].astype("category")
df["Embarked"] = df["Embarked"].astype("category")

df = df[expected].sort_values("PassengerId").reset_index(drop=True)

# 14. Automated validation
assert df.duplicated().sum() == 0
assert df["PassengerId"].is_unique
assert df["PassengerId"].notna().all()
assert set(df["Survived"].unique()).issubset({0, 1})
assert set(df["Pclass"].unique()).issubset({1, 2, 3})
assert set(df["Sex"].astype(str).unique()).issubset({"male", "female"})
assert set(df["Embarked"].astype(str).unique()).issubset({"S", "C", "Q"})
assert df["Age"].between(0, 100).all()
assert (df["Fare"] >= 0).all()
assert df.columns.tolist() == expected

# 15. Export
OUT.parent.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUT, index=False)
df.to_excel(XLSX, index=False)
pd.DataFrame(log).to_csv(LOG, index=False)

print(f"Cleaned dataset: {len(df):,} rows x {len(df.columns)} columns")
print(f"Cleaning log: {LOG}")
print("All validation checks passed.")
