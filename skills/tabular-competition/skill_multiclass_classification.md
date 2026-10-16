# Skill: multiclass tabular competition

Use when the target contains three or more mutually exclusive classes. Deliver one Kaggle-ready standalone notebook, ideally adapted from `notebooks/tabular_multiclass_kaggle.ipynb`.

## Decide before fitting

- Confirm every class name, frequency, and expected submission column order. Preserve the original labels for the final file, and assert that probability columns sum to one.
- Match the official metric. Multiclass log loss needs all class probabilities and punishes confident errors; macro F1 gives rare classes equal weight; weighted F1 follows prevalence; accuracy can obscure weak minority classes. OOF `roc_auc_ovr_macro` is supplemental, not interchangeable with log loss.
- Keep each class represented in every training fold. If groups or forward-time splits leave a class absent, reconsider the split or model the actual deployment constraint explicitly. Never silently discard a class.

## Strong model path

1. Train native-category CatBoost and LightGBM baselines with early stopping; compare XGBoost when budget allows. Use identical fold indices and metric computation. Add simple probability averaging only if OOF improves the official metric.
2. Fit per-fold imputers and encoders as in the binary guide. Prefer simple native missing handling or median plus missing indicators before complex imputers; judge cleaning by out-of-fold performance and data validity.
3. For imbalance, try sample weighting first. Fold-local random oversampling is another option. Check per-class precision, recall, and confusion before enabling it; a better macro F1 may lower log loss. Do not alter validation prevalence.
4. If a probability submission is required, map every sample-submission class column to the correct `predict_proba` index. Never use the argmax class index as a probability or assume alphabetic order matches the competition template.

## Required notebook artifacts

Schema and target audit; missingness, distributions, category/target and numeric/target plots, drift; fold scores and OOF comparison; count and row-normalized confusion matrices, classification report, per-class one-vs-rest ROC/PR where defined, confidence distribution, training/validation loss curves for boosting, feature importance, OOF error file, and submission. Record model, fold design, metric, class mapping, seed, versions, and actual CPU/GPU use.

Class probability calibration and cost-sensitive decisions require a separate validation protocol. Do not claim probabilities are calibrated merely because they sum to one.
