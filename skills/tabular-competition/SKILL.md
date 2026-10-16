---
name: tabular-competition
description: Build a standalone Kaggle notebook, inspect a dataset, or prepare slide-by-slide presentation content for binary and multiclass tabular competitions. Covers EDA, cleaning, validation, and evidence-backed results; exclude image, text, ranking, regression, and time-series forecasting competitions.
---

# Tabular competition notebook

Produce a **single executable `.ipynb`** that reads attached Kaggle input, validates with a split matching the competition's data-generating process, trains strong baselines, emits visual diagnostics, and saves the requested submission. Start from the matching repository notebook if available, then adapt its configuration and code to the actual dataset. Keep the final notebook standalone: never depend on a helper `.py` or local skill file at Kaggle runtime.

Read only the relevant guide:

- [skill_binary_classification.md](skill_binary_classification.md) for exactly two target classes.
- [skill_multiclass_classification.md](skill_multiclass_classification.md) for three or more classes.
- [skill_eda.md](skill_eda.md) when given a dataset or link and asked to characterize it, or before choosing cleaning and validation.
- [skill_data_cleaning.md](skill_data_cleaning.md) when the dataset contains missing, duplicate, inconsistent, or suspect values.
- [skill_larp.md](skill_larp.md) when preparing a competition presentation, speaker notes, or judge Q&A from actual notebook results.
- [skill_ppt.md](skill_ppt.md) when asked to prepare ordered, slide-by-slide content and visual directions for a PowerPoint presentation about tabular competition results.

## Non-negotiable decisions

1. Read the competition metric, submission format, leakage rules, entity structure, and time semantics. A benchmark's aggregate rank is not a guaranteed winner on a particular competition.
2. Keep target labels and any post-outcome columns out of features. Fit imputers, encoders, samplers, feature selection, calibrators, and threshold selection on training folds only. Never learn from the hidden test labels.
3. For a fixed validation scheme, compare CatBoost, LightGBM, and XGBoost as practical first candidates; consider AutoGluon ensembles or TabPFN family when data size, dependencies, licensing, compute, and competition rules permit. A fast baseline and honest CV are mandatory before expensive search.
4. Make every code branch executable for the chosen settings. Fail with a specific message for unsupported combinations. Save OOF predictions, fold scores, model comparison, plots, and submission under `/kaggle/working`.
5. Label every plot with its population (train sample, validation fold, or OOF). Explain when curves or importance are unavailable or model specific. Do not treat a threshold optimized on the same OOF as an unbiased CV gain.

The evidence review and source links are in [RESEARCH.md](../../RESEARCH.md). Recheck library APIs and competition rules when creating a new notebook; these evolve.
