# Interview Questions and Answers

### How do you decide whether to drop or impute a missing value?
I first assess the field's role, missingness and business meaning. I drop a row when a required identifier is missing and the record cannot be reliably tracked. For numeric fields, I use a documented imputation strategy when it is defensible.

### What's the difference between a duplicate row and a duplicate key?
A duplicate row repeats the same complete record. A duplicate key means the field expected to uniquely identify a record appears more than once, even if other fields differ. Exact duplicates can usually be removed, while duplicate keys need investigation and a resolution rule.

### How would you handle outliers differently from missing values?
A missing value is absent information. An outlier is an observed value that is unusual. I validate an outlier before removing it. I only treat it as an error when it violates a known constraint.

### How would you validate that a dataset is clean?
I rerun the inventory and use assertions for key uniqueness, duplicates, allowed categories, numeric ranges, required columns and required fields. I also compare before/after metrics and retain a cleaning log.

### Why median imputation for Age?
Median is less sensitive to extreme values than mean, and grouping by Pclass and Sex preserves subgroup structure.

### Why `Unknown` for Cabin?
Cabin has substantial missingness. Filling missing cabins with an actual cabin would invent information, so an explicit Unknown category is safer.

### Why is a change log important?
It makes the process auditable and reproducible. A reviewer can see what was changed, why it was changed and what impact it had.
