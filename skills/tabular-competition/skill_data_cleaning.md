# Skill: tabular competition data cleaning

Use after schema and EDA reveal concrete quality issues. Cleaning is a model choice evaluated with leakage-safe CV, not a universal sequence that always improves scores.

## Decision rules

| Issue | Default action | Validate before changing |
| --- | --- | --- |
| String sentinels and whitespace | Normalize known markers, strip surrounding whitespace consistently in train/test | Ensure `"NA"`, `"0"`, or spaces are not legitimate categories |
| Numeric missing | Native NaN for supporting trees or fold-fitted median plus indicator | Compare missingness signal and official metric; never fit an imputer on validation/test |
| Categorical missing/unseen | Explicit missing token; native categories or fold-fitted one-hot with unknown handling | Check semantic difference between absent, unknown, and not applicable |
| Exact duplicates | Report, inspect conflicting targets, then optionally remove exact duplicate training rows | Group identical entities across folds if duplicates would inflate CV |
| Extreme values | Check units, physical bounds, parse errors, and data-entry evidence first | Tree methods often tolerate extremes; arbitrary clipping can remove valid signal |
| High-cardinality IDs | Determine whether they encode stable entities or leak row identity | Drop known IDs; use group CV or leakage-safe encoding if entity history is valid |
| Date/time | Parse explicitly; create only inference-available calendar or lag features | Lag/aggregate calculations must use past data within each fold |
| Class imbalance | Compare no correction, weights, then fold-local resampling | Keep natural validation distribution; measure PR, recall, macro F1 or official metric |

Target encoding, count encoding based on target, feature selection, iterative/KNN imputation, outlier thresholds, and any learned cleaning rule must be fitted only on each training fold. Target encoding needs internal cross-fitting to avoid a row seeing its own label. Use native tree handling or one-hot as a robust baseline first. A sophisticated imputer is not automatically better for prediction, even if it reconstructs missing values accurately.

Write down each mutation and its row/column impact. Reject silent target-label fixes, undocumented unit conversion, blanket row deletion for missingness, and test-informed tuning disguised as preprocessing.
