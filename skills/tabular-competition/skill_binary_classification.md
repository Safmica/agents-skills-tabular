# Skill: binary tabular competition

Use this guide when the target has exactly two values. Deliver one Kaggle-ready standalone notebook, ideally adapted from `notebooks/tabular_binary_kaggle.ipynb`.

## Decide before fitting

- Record the positive class explicitly. `LabelEncoder` orders strings lexicographically; the competition may define the positive class differently. Map the required class and sample-submission column before writing probabilities.
- Match the official metric. ROC AUC ranks discrimination; PR AUC is useful when positives are rare; log loss rewards calibrated probability; F1 and accuracy depend on a threshold. Do not select or report only accuracy for strong imbalance.
- For repeated people, accounts, devices, or products, use group CV; for future-event prediction, use forward-time CV with an embargo when needed. Random stratification is appropriate only for independent, identically distributed rows.
- Set aside an untouched holdout or use nested CV if many models, features, or thresholds are tuned against the same OOF scores.

## Strong model path

1. Build a trivial prevalence baseline and a fast CatBoost/LightGBM baseline. Include XGBoost as a third candidate when time permits. Tune tree depth/leaves, learning rate with iteration count, regularization, min leaf size, subsampling, and early stopping using the same folds. Try blending only after checking complementary OOF errors.
2. CatBoost handles categories natively; pass categorical columns as strings and numeric missing as NaN when using native mode. LightGBM supports pandas categorical columns and numeric missing. For XGBoost and linear baselines, fit `ColumnTransformer` / `OneHotEncoder(handle_unknown="ignore")` and imputation within each fold. Scaling is mainly for linear or neural methods, not tree boosting.
3. Start imbalance handling with `class_weight` or sample weights and compare against no weighting on the official metric. Random oversampling happens only inside training folds. Numeric-only SMOTE is optional and must be evaluated against simpler alternatives; naive SMOTE on one-hot mixed categorical features invents invalid categories.
4. Use a fixed threshold of 0.5 for initial OOF confusion, precision, recall, F1, MCC, and balanced accuracy. If the competition scores labels, optimize the threshold on a separate calibration split or nested CV. If it scores probabilities, submit probabilities and evaluate calibration with Brier/log loss and reliability plots.

## Required notebook artifacts

Audit of schema, target prevalence, missingness and duplicates; numeric distributions, category-target and numeric-target relationships, train/test drift; fold table, OOF and model comparison; count and normalized confusion matrices; ROC, PR, calibration and score distributions; training/validation loss curves for boosting; model-specific feature importance; error rows; submission with correct positive-class probability. Record seed, package versions, selected metric, fold design, and which accelerator actually ran.

Stop and state the precise adaptation needed if a competition requires ranking, custom metric, unusual submission schema, or labels not represented in the notebook template.
