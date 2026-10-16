"""Small end-to-end execution of both notebook templates on synthetic CSVs."""
import json
import os
import tempfile
from pathlib import Path

os.environ["MPLBACKEND"] = "Agg"

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification


ROOT = Path(__file__).resolve().parents[1]


def run(slug, n_classes, models, overrides=None, numeric_only=False, scenario="default"):
    overrides = overrides or {}
    rng = np.random.default_rng(42)
    x, y = make_classification(n_samples=165, n_features=5, n_informative=4,
                               n_redundant=0, n_classes=n_classes,
                               n_clusters_per_class=1, random_state=42)
    frame = pd.DataFrame(x, columns=[f"numeric_{i}" for i in range(5)])
    if not numeric_only:
        frame["category"] = rng.choice(["east", "west", "north"], size=len(frame)).astype(object)
        frame.loc[rng.choice(len(frame), 12, replace=False), "category"] = None
    if overrides.get("split_type") == "group":
        frame["account_id"] = np.arange(len(frame)) // 3
    if overrides.get("split_type") == "time":
        frame["event_time"] = pd.date_range("2025-01-01", periods=len(frame), freq="h").astype(str)
    frame.loc[rng.choice(len(frame), 15, replace=False), "numeric_0"] = np.nan
    frame["id"] = np.arange(len(frame))
    classes = ["A", "B", "C"][:n_classes]
    frame["target"] = np.array(classes)[y]
    train = frame.iloc[:135].copy()
    test = frame.iloc[135:].drop(columns="target").copy()
    with tempfile.TemporaryDirectory(prefix=f"tabular_{slug}_") as temporary:
        folder = Path(temporary)
        train.to_csv(folder / "train.csv", index=False)
        test.to_csv(folder / "test.csv", index=False)
        if n_classes == 2:
            sample = pd.DataFrame({"id": test["id"], "target": np.zeros(len(test))})
        else:
            sample = pd.DataFrame({"id": test["id"], **{c: np.zeros(len(test)) for c in classes}})
        sample.to_csv(folder / "sample_submission.csv", index=False)
        nb = json.loads((ROOT / "notebooks" / f"tabular_{slug}_kaggle.ipynb").read_text(encoding="utf-8"))
        context = {"__name__": "__main__"}
        for i, cell in enumerate(nb["cells"]):
            if cell["cell_type"] != "code":
                continue
            if i == 3:  # dependency installation cell; packages must already be installed for the test
                continue
            exec(compile("".join(cell["source"]), f"{slug}:cell_{i}", "exec"), context)
            if i == 1:
                context["CFG"].update(train_path=str(folder / "train.csv"), test_path=str(folder / "test.csv"),
                    sample_submission_path=str(folder / "sample_submission.csv"), output_dir=str(folder / "out"),
                    target="target", n_splits=2, models=models, iterations=45, early_stopping_rounds=10,
                    use_gpu=False, eda=True, eda_sample_rows=130, save_models=False)
                context["CFG"].update(overrides)
        submission = pd.read_csv(folder / "out" / "submission.csv")
        assert submission.shape == sample.shape, (submission.shape, sample.shape)
        assert submission["id"].equals(test["id"].reset_index(drop=True))
        assert (folder / "out" / "confusion_matrix.png").exists()
        assert (folder / "out" / "fold_metric_matrix.png").exists()
        assert (folder / "out" / "oof_model_comparison.csv").exists()
        if n_classes > 2:
            assert np.allclose(submission[classes].sum(axis=1), 1, atol=1e-4)
        print(f"PASS {slug}/{scenario}: {models}")


if __name__ == "__main__":
    if os.environ.get("SMOKE_QUICK") == "1":
        run("binary", 2, ["lightgbm", "extratrees", "logistic"])
        run("multiclass", 3, ["lightgbm"])
    else:
        run("binary", 2, ["catboost", "lightgbm", "xgboost", "extratrees", "logistic"])
        run("multiclass", 3, ["catboost", "lightgbm"])
    if os.environ.get("SMOKE_VARIANTS") == "1":
        run("binary", 2, ["catboost"], {"split_type":"group", "group_column":"account_id",
            "imbalance_class":True, "imbalance_method":"class_weight", "eda":False}, scenario="group_weight")
        run("binary", 2, ["lightgbm"], {"split_type":"time", "time_column":"event_time",
            "date_columns":["event_time"], "imbalance_class":True,
            "imbalance_method":"random_over", "eda":False}, scenario="time_over")
        run("binary", 2, ["lightgbm"], {"imbalance_class":True,
            "imbalance_method":"smote_numeric", "eda":False}, numeric_only=True, scenario="smote_numeric")
        run("binary", 2, ["catboost"], {"missing_value_handling":False,
            "missing_value_method":"native", "eda":False}, scenario="native_missing")
