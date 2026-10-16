# Skill: competition tabular EDA

Use for a provided dataset file or link. If the link cannot be read, report that access limit and request the file or a public direct download. Never invent dataset-specific findings. Produce a concise audit table, a prioritized insight list with evidence, and notebook cells that recreate the plots.

## Record before modeling

1. Dataset provenance, train/test/sample-submission paths, row and column counts, target and class frequencies, competition metric, row identity, group and time keys, and permitted external data. State which fields are known only after the outcome.
2. Column-level dtype, semantic type (continuous, count, ordinal, nominal, identifier, datetime, free text), unique count, missing count and fraction, parse failures, sentinel values, zero/near-zero variance, duplicates, conflicting labels on duplicate features, and plausible range/unit violations.
3. Per-feature numeric quantiles/distributions/outliers, categorical frequency and rare levels, target relationships, correlations/collinearity, missingness versus target, and train/test distribution changes. Include sample size and denominator on plots. Limit wide/high-cardinality plots to informative subsets and save complete audits as CSV.
4. Identify likely leakage from IDs, timestamps, aggregates spanning validation boundaries, target-derived fields, and duplicate entities across folds. Distinguish direct evidence from hypotheses that need domain confirmation.
5. Rank issues by likely effect on validation or inference and propose a testable action, such as group CV, time CV, rare-category policy, missing indicator, or dropping a post-outcome feature. For each action state whether it is deterministic or must be fitted within folds.

Suggested plots: target balance; missingness bar chart; numeric histogram/boxplot; categorical top levels; numeric-by-target and category-by-target plots; Spearman heatmap; train/test drift bar chart; group overlap and timeline where applicable. For large data, plot a seeded sample but compute counts on full data.

EDA is descriptive. Do not call a feature causal, or call a suspected leakage field proven without checking how and when it was collected. Do not use the hidden test target.
