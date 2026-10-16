"""Generate the two self-contained Kaggle notebook templates."""
import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "notebooks"
OUT.mkdir(exist_ok=True)


def md(value):
    return {"cell_type": "markdown", "metadata": {}, "source": dedent(value).lstrip().splitlines(True)}


def code(value):
    source = dedent(value).lstrip().replace("plt.show()", "plt.show(); plt.close('all')")
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": source.splitlines(True)}


COMMON = [
    md("""
    # Kompetisi klasifikasi tabular — notebook standalone

    Ubah **hanya sel konfigurasi** untuk kebanyakan dataset. Input dicari di `/kaggle/input`, hasil visual dan CSV ditulis ke `/kaggle/working/tabular_outputs`. Jalankan berurutan dari atas. Aktifkan accelerator **GPU T4 x2** di Kaggle; algoritme tree biasanya memakai satu GPU per fit, dan CPU fallback tersedia. Tidak ada data validasi atau test yang digunakan untuk belajar imputasi, encoding, sampling, atau pemilihan threshold.

    Notebook ini menyediakan EDA, audit kualitas data, stratified/group/time CV, CatBoost/LightGBM/XGBoost dan baseline sklearn, OOF, perbandingan model, ensemble, kurva training, confusion matrix, ROC/PR/calibration, feature importance, serta submission. Catatan metodologi dan keterbatasan ada di README.
    """),
    code("""
    # KONFIGURASI — edit di sini
    CFG = {
        "train_path": None,             # contoh: "/kaggle/input/nama-kompetisi/train.csv"; None = auto-discovery
        "test_path": None,              # None = auto-discovery; boleh tanpa test untuk validasi saja
        "sample_submission_path": None,
        "target": None,                 # None = infer satu kolom train yang tidak ada di test
        "id_columns": [],               # contoh: ["id"]; dibuang dari fitur, dipakai di submission
        "drop_columns": [],             # kolom yang diketahui bocor / tidak boleh dipakai
        "group_column": None,           # untuk split_type="group"
        "time_column": None,            # untuk split_type="time"; tidak dipakai sebagai fitur kecuali dibuat eksplisit
        "date_columns": [],             # fitur kalender hanya jika nilainya tersedia saat inference
        "split_type": "stratified",     # stratified | group | time
        "n_splits": 5,
        "time_gap": 0,                  # jumlah baris embargo untuk TimeSeriesSplit
        "seed": 42,
        "models": ["catboost", "lightgbm"],  # catboost | lightgbm | xgboost | extratrees | logistic
        "primary_metric": "auto",       # binary: roc_auc, pr_auc, log_loss, f1, balanced_accuracy; multi: log_loss, f1_macro, accuracy, balanced_accuracy
        "ensemble": True,
        "use_gpu": True,                # fallback CPU jika fit GPU gagal
        "iterations": 700,
        "learning_rate": 0.04,
        "early_stopping_rounds": 80,
        "eda": True,
        "eda_sample_rows": 5000,
        "eda_top_features": 8,
        "missing_value_handling": True,
        "missing_value_method": "median",  # median | mean | constant | native
        "missing_indicator": True,
        "numeric_constant": 0.0,
        "categorical_missing_token": "__MISSING__",
        "missing_tokens": ["?", "NA", "N/A", "null", "None", ""],
        "strip_string_whitespace": True,
        "drop_duplicate_rows": False,   # hanya duplicate identik train; tinjau label konflik lebih dulu
        "imbalance_class": False,
        "imbalance_method": "class_weight",  # class_weight | random_over | smote_numeric
        "binary_threshold": 0.5,       # threshold tetap; pilih dari OOF hanya sebagai analisis, jangan klaim skor CV hasil tuning
        "submission_mode": "auto",     # auto | probability | label
        "save_models": False,
        "output_dir": "/kaggle/working/tabular_outputs",
    }
    """),
    code("""
    import sys, subprocess, importlib.util
    needed = {"numpy":"numpy", "pandas":"pandas", "scipy":"scipy", "sklearn":"scikit-learn",
              "matplotlib":"matplotlib", "seaborn":"seaborn"}
    for model_name in CFG["models"]:
        if model_name in ("catboost", "lightgbm", "xgboost"):
            needed[model_name] = model_name
    if CFG["imbalance_class"] and CFG["imbalance_method"] == "smote_numeric":
        needed["imblearn"] = "imbalanced-learn"
    missing_packages = [package for module, package in needed.items() if importlib.util.find_spec(module) is None]
    if missing_packages:
        print("Installing missing packages:", missing_packages)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *missing_packages])
    """),
    code("""
    import json, os, warnings
    from pathlib import Path
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.stats import ks_2samp
    from sklearn.base import clone
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.metrics import (accuracy_score, balanced_accuracy_score, brier_score_loss,
        classification_report, confusion_matrix, f1_score, log_loss, matthews_corrcoef,
        precision_recall_curve, average_precision_score, roc_auc_score, roc_curve)
    from sklearn.model_selection import StratifiedKFold, StratifiedGroupKFold, TimeSeriesSplit
    from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, label_binarize
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import ExtraTreesClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.utils.class_weight import compute_sample_weight
    try:
        from IPython.display import display
    except ImportError:
        def display(value):
            print(value)

    sns.set_theme(style="whitegrid")
    OUT = Path(CFG["output_dir"])
    OUT.mkdir(parents=True, exist_ok=True)
    np.random.seed(CFG["seed"])
    print("Versions:", {m: __import__(m).__version__ for m in ["numpy", "pandas", "sklearn"]})
    print("Visible CUDA devices:", os.environ.get("CUDA_VISIBLE_DEVICES", "system default"))
    try:
        import torch
        print("Torch GPUs:", torch.cuda.device_count())
    except ImportError:
        pass
    """),
    md("""## 1. Muat dan audit data

    Bila auto-discovery menemukan lebih dari satu `train.csv`, tentukan path eksplisit. Periksa aturan kompetisi, target, ID, metrik resmi, unit observasi, waktu, dan format sample submission sebelum melatih model.
    """),
    code("""
    def find_csv(name, explicit=None, optional=False):
        if explicit:
            path = Path(explicit)
            if not path.exists():
                raise FileNotFoundError(path)
            return path
        found = sorted(Path("/kaggle/input").rglob(name)) if Path("/kaggle/input").exists() else []
        if len(found) == 1:
            return found[0]
        if optional and len(found) == 0:
            return None
        if not found:
            raise FileNotFoundError(f"{name} tidak ditemukan. Isi path di CFG.")
        raise ValueError(f"Ada beberapa {name}: {found}. Isi path eksplisit di CFG.")

    train_path = find_csv("train.csv", CFG["train_path"])
    test_path = find_csv("test.csv", CFG["test_path"], optional=True)
    sample_path = find_csv("sample_submission.csv", CFG["sample_submission_path"], optional=True)
    train = pd.read_csv(train_path, low_memory=False)
    test = pd.read_csv(test_path, low_memory=False) if test_path else None
    sample_submission = pd.read_csv(sample_path) if sample_path else None
    if test is not None and sample_submission is not None and not CFG["id_columns"]:
        for col in sample_submission.columns.intersection(test.columns):
            if (len(test) == len(sample_submission) and test[col].is_unique
                    and test[col].reset_index(drop=True).equals(sample_submission[col].reset_index(drop=True))):
                CFG["id_columns"].append(col)
        if CFG["id_columns"]:
            print("Inferred ID columns from test/sample submission:", CFG["id_columns"])
    if CFG["target"] is None:
        if test is None:
            raise ValueError("Tanpa test.csv, isi CFG['target'].")
        candidates = [c for c in train if c not in test and c not in CFG["drop_columns"]]
        if len(candidates) != 1:
            raise ValueError(f"Target ambigu: {candidates}. Isi CFG['target'].")
        CFG["target"] = candidates[0]
    target = CFG["target"]
    if target not in train:
        raise ValueError(f"Target {target!r} tidak ada di train.")
    if test is not None and target in test:
        test = test.drop(columns=[target])
    print("Train:", train.shape, "Test:", None if test is None else test.shape, "Target:", target)
    display(train.head(3))
    if sample_submission is not None:
        print("Sample submission columns:", list(sample_submission))
    """),
    code("""
    def audit(df, label):
        report = pd.DataFrame({"dtype": df.dtypes.astype(str), "missing_n": df.isna().sum(),
                               "missing_pct": df.isna().mean().round(4),
                               "unique_n": df.nunique(dropna=True),
                               "example": [str(df[c].dropna().iloc[0])[:70] if df[c].notna().any() else "" for c in df]})
        report.to_csv(OUT / f"{label}_audit.csv")
        print(f"{label}: rows={len(df):,}, columns={df.shape[1]}, duplicates={df.duplicated().sum():,}, memory_MB={df.memory_usage(deep=True).sum()/1e6:.1f}")
        display(report.sort_values("missing_pct", ascending=False).head(30))
        return report

    train_audit = audit(train, "train")
    if test is not None:
        test_audit = audit(test, "test")
        print("Train only:", sorted(set(train) - set(test)))
        print("Test only:", sorted(set(test) - set(train)))
    print("Target counts including missing:")
    display(train[target].value_counts(dropna=False).to_frame("count"))
    print("Conflicting labels on identical feature rows require domain review; no automatic label repair is applied.")
    """),
    code("""
    # Deterministic cleaning only. Estimated statistics are fitted inside each CV fold below.
    def clean_frame(df):
        if df is None:
            return None
        out = df.copy().replace([np.inf, -np.inf], np.nan)
        for col in out.select_dtypes(include=["object", "string"]).columns:
            s = out[col].astype("string")
            if CFG["strip_string_whitespace"]:
                s = s.str.strip()
            out[col] = s.replace(CFG["missing_tokens"], pd.NA)
        for col in CFG["date_columns"]:
            if col in out:
                dt = pd.to_datetime(out[col], errors="coerce", utc=True)
                for suffix, part in {"year":dt.dt.year, "month":dt.dt.month, "day":dt.dt.day,
                                     "weekday":dt.dt.dayofweek, "hour":dt.dt.hour}.items():
                    out[f"{col}__{suffix}"] = part.astype(float)
                if col != CFG["time_column"]:
                    out = out.drop(columns=[col])
        return out

    train = clean_frame(train)
    test = clean_frame(test)
    if CFG["drop_duplicate_rows"]:
        before = len(train)
        train = train.drop_duplicates().reset_index(drop=True)
        print("Dropped identical train rows:", before - len(train))
    missing_target = train[target].isna()
    if missing_target.any():
        print("Dropped rows without target:", int(missing_target.sum()))
        train = train.loc[~missing_target].reset_index(drop=True)
    labels = LabelEncoder()
    y = labels.fit_transform(train[target])
    N_CLASSES = len(labels.classes_)
    if N_CLASSES != EXPECTED_CLASSES:
        raise ValueError(f"Notebook expects {EXPECTED_CLASSES} classes; found {N_CLASSES}: {list(labels.classes_)}")
    print("Class mapping:", dict(enumerate(labels.classes_)))
    feature_exclude = set(CFG["id_columns"] + CFG["drop_columns"] + [target])
    if CFG["group_column"]:
        feature_exclude.add(CFG["group_column"])
    if CFG["time_column"]:
        feature_exclude.add(CFG["time_column"])
    features = [c for c in train if c not in feature_exclude]
    if not features:
        raise ValueError("No features remain.")
    if test is not None:
        missing_features = sorted(set(features) - set(test))
        if missing_features:
            raise ValueError(f"Test lacks train features: {missing_features}")
    X = train[features].copy()
    X_test = test.reindex(columns=features).copy() if test is not None else None
    cat_cols = X.select_dtypes(include=["object", "string", "category", "bool"]).columns.tolist()
    num_cols = [c for c in features if c not in cat_cols]
    for col in num_cols:
        X[col] = pd.to_numeric(X[col], errors="coerce")
        if X_test is not None:
            X_test[col] = pd.to_numeric(X_test[col], errors="coerce")
    print(f"Features: {len(features)}; numeric: {len(num_cols)}; categorical: {len(cat_cols)}")
    print("Potential high-cardinality ID-like fields:", [c for c in features
          if (c in cat_cols or "id" in c.lower()) and X[c].nunique(dropna=True) > 0.9 * len(X)])
    """),
    md("""## 2. EDA dan hubungan dengan target

    Plot dibatasi sampel dan jumlah fitur agar notebook tetap dapat dipakai pada data besar. Semua laporan disimpan ke direktori output. Korelasi dan hubungan target bersifat deskriptif; asosiasi tidak membuktikan kausalitas atau aman dari leakage.
    """),
    code("""
    if CFG["eda"]:
        eda = X.sample(min(len(X), CFG["eda_sample_rows"]), random_state=CFG["seed"])
        eda_y = pd.Series(y, index=X.index).loc[eda.index]
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.countplot(x=labels.inverse_transform(eda_y), ax=ax)
        ax.set_title("Target distribution (EDA sample)")
        ax.tick_params(axis="x", rotation=35)
        fig.tight_layout(); fig.savefig(OUT / "eda_target.png", dpi=140); plt.show()
        missing = X.isna().mean().sort_values(ascending=False).head(25)
        if missing.max() > 0:
            fig, ax = plt.subplots(figsize=(9, max(3, len(missing)*0.28)))
            missing[missing > 0].sort_values().plot.barh(ax=ax)
            ax.set_xlabel("Missing fraction"); ax.set_title("Missingness by feature")
            fig.tight_layout(); fig.savefig(OUT / "eda_missing.png", dpi=140); plt.show()
            miss_cols = missing[missing > 0].head(min(10, CFG["eda_top_features"])).index
            miss_by_class = pd.DataFrame({col: X[col].isna().groupby(train[target]).mean() for col in miss_cols})
            miss_by_class.to_csv(OUT / "eda_missing_by_target.csv")
            fig, ax = plt.subplots(figsize=(max(6,len(miss_cols)), max(3,len(miss_by_class)*0.6)))
            sns.heatmap(miss_by_class, annot=True, fmt=".2f", cmap="Reds", ax=ax)
            ax.set_title("Missing fraction by target class")
            fig.tight_layout(); fig.savefig(OUT / "eda_missing_by_target.png", dpi=140); plt.show()
        chosen_num = sorted(num_cols, key=lambda c: X[c].nunique(dropna=True), reverse=True)[:CFG["eda_top_features"]]
        if chosen_num:
            eda[chosen_num].hist(figsize=(12, max(3, 2.5*((len(chosen_num)+2)//3))), bins=30)
            plt.suptitle("Numeric distributions"); plt.tight_layout(); plt.savefig(OUT / "eda_numeric_distributions.png", dpi=140); plt.show()
            corr = eda[chosen_num].corr(method="spearman")
            if len(chosen_num) > 1:
                fig, ax = plt.subplots(figsize=(max(6,len(chosen_num)), max(5,len(chosen_num)*0.8)))
                sns.heatmap(corr, cmap="coolwarm", center=0, annot=len(chosen_num)<=10, ax=ax)
                ax.set_title("Spearman correlations")
                fig.tight_layout(); fig.savefig(OUT / "eda_correlations.png", dpi=140); plt.show()
            rel = eda[chosen_num[:4]].copy(); rel["target"] = labels.inverse_transform(eda_y)
            for col in chosen_num[:4]:
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.boxplot(data=rel, x="target", y=col, showfliers=False, ax=ax)
                ax.tick_params(axis="x", rotation=30)
                ax.set_title(f"{col} by target")
                fig.tight_layout(); fig.savefig(OUT / f"eda_relation_num_{chosen_num.index(col)}.png", dpi=140); plt.show()
        for i, col in enumerate(cat_cols[:min(4, CFG["eda_top_features"])]):
            top = eda[col].fillna("__MISSING__").astype(str).value_counts().head(10).index
            view = pd.DataFrame({"category": eda[col].fillna("__MISSING__").astype(str), "target":labels.inverse_transform(eda_y)})
            view = view[view["category"].isin(top)]
            if not view.empty:
                tab = pd.crosstab(view["category"], view["target"], normalize="index")
                tab.plot.bar(stacked=True, figsize=(9, 4), colormap="tab20")
                plt.ylabel("Class share"); plt.title(f"Target relationship: {col}")
                plt.tight_layout(); plt.savefig(OUT / f"eda_relation_cat_{i}.png", dpi=140); plt.show()
        if X_test is not None:
            cat_drift = []
            for col in cat_cols:
                known = set(X[col].dropna().astype(str))
                observed = X_test[col].dropna().astype(str)
                cat_drift.append({"feature":col, "unseen_test_fraction":float((~observed.isin(known)).mean()) if len(observed) else 0.0,
                                  "train_unique":X[col].nunique(dropna=True), "test_unique":X_test[col].nunique(dropna=True)})
            if cat_drift:
                pd.DataFrame(cat_drift).sort_values("unseen_test_fraction",ascending=False).to_csv(
                    OUT / "eda_categorical_drift.csv",index=False)
            drift = []
            for col in num_cols:
                a, b = X[col].dropna(), X_test[col].dropna()
                if len(a) > 1 and len(b) > 1:
                    a = a.sample(min(len(a), 5000), random_state=CFG["seed"])
                    b = b.sample(min(len(b), 5000), random_state=CFG["seed"])
                    drift.append({"feature":col, "ks_statistic":ks_2samp(a,b).statistic,
                                  "train_missing":X[col].isna().mean(), "test_missing":X_test[col].isna().mean()})
            if drift:
                drift = pd.DataFrame(drift).sort_values("ks_statistic", ascending=False)
                drift.to_csv(OUT / "eda_numeric_drift.csv", index=False)
                display(drift.head(15))
                fig, ax = plt.subplots(figsize=(8, max(3, min(15,len(drift))*0.35)))
                sns.barplot(data=drift.head(15), x="ks_statistic", y="feature", ax=ax)
                ax.set_title("Train/test numeric drift (KS statistic)")
                fig.tight_layout(); fig.savefig(OUT / "eda_train_test_drift.png", dpi=140); plt.show()
    """),
    md("""## 3. Validasi dan pemrosesan per fold

    `stratified` cocok untuk baris independen; `group` menjaga entitas tetap pada satu fold; `time` melatih hanya pada masa lalu. Audit fitur yang dibuat setelah kejadian target tetap harus dilakukan secara manual. Oversampling hanya diterapkan ke baris training fold.
    """),
    code("""
    if CFG["split_type"] == "stratified":
        if np.bincount(y).min() < CFG["n_splits"]:
            raise ValueError("Minority class count must be >= n_splits.")
        splitter = StratifiedKFold(n_splits=CFG["n_splits"], shuffle=True, random_state=CFG["seed"])
        splits = list(splitter.split(X, y))
    elif CFG["split_type"] == "group":
        col = CFG["group_column"]
        if not col or col not in train:
            raise ValueError("Set a valid group_column.")
        groups = train[col].fillna("__MISSING_GROUP__").astype(str)
        splitter = StratifiedGroupKFold(n_splits=CFG["n_splits"], shuffle=True, random_state=CFG["seed"])
        splits = list(splitter.split(X, y, groups))
    elif CFG["split_type"] == "time":
        col = CFG["time_column"]
        if not col or col not in train:
            raise ValueError("Set a valid time_column.")
        dates = pd.to_datetime(train[col], errors="coerce", utc=True)
        if dates.isna().any():
            raise ValueError("time_column contains invalid dates; clean it before CV.")
        order = np.argsort(dates.to_numpy(), kind="stable")
        splitter = TimeSeriesSplit(n_splits=CFG["n_splits"], gap=CFG["time_gap"])
        splits = [(order[a], order[b]) for a,b in splitter.split(order)]
    else:
        raise ValueError("split_type must be stratified, group, or time")
    for i, (a,b) in enumerate(splits, 1):
        print(f"Fold {i}: train={len(a)}, valid={len(b)}, train classes={np.bincount(y[a], minlength=N_CLASSES)}, valid classes={np.bincount(y[b], minlength=N_CLASSES)}")
        if len(np.unique(y[a])) != N_CLASSES:
            raise ValueError(f"Fold {i} training partition lacks a class. Change split strategy.")
    covered = np.unique(np.concatenate([b for _, b in splits]))
    if len(np.unique(y[covered])) != N_CLASSES:
        raise ValueError("OOF validation rows lack a class. Change split strategy or obtain later examples of that class.")

    if CFG["missing_value_method"] not in ("median", "mean", "constant", "native"):
        raise ValueError("Invalid missing_value_method")
    if not CFG["missing_value_handling"] and CFG["missing_value_method"] != "native":
        raise ValueError("Set missing_value_method='native' when missing_value_handling=False.")
    if CFG["imbalance_class"] and CFG["imbalance_method"] not in ("class_weight", "random_over", "smote_numeric"):
        raise ValueError("Invalid imbalance_method")
    if CFG["imbalance_class"] and CFG["imbalance_method"] == "smote_numeric" and cat_cols:
        raise ValueError("smote_numeric requires numeric-only features; use class_weight or random_over for mixed data.")
    if (CFG["imbalance_class"] and CFG["imbalance_method"] == "smote_numeric"
            and (not CFG["missing_value_handling"] or CFG["missing_value_method"] == "native")
            and X[num_cols].isna().any().any()):
        raise ValueError("smote_numeric with missing values needs fold-fitted numeric imputation.")
    """),
    code("""
    def prepared_native(x_train, x_valid, x_test, model_name):
        tr, va = x_train.copy(), x_valid.copy()
        te = x_test.copy() if x_test is not None else None
        for col in cat_cols:
            for frame in (tr, va, te):
                if frame is not None:
                    frame[col] = frame[col].fillna(CFG["categorical_missing_token"]).astype(str)
            if model_name == "lightgbm":
                # categories learned from the training fold only
                cats = pd.Categorical(tr[col]).categories
                for frame in (tr, va, te):
                    if frame is not None:
                        frame[col] = pd.Categorical(frame[col], categories=cats)
        if CFG["missing_value_handling"] and CFG["missing_value_method"] != "native":
            for col in num_cols:
                if CFG["missing_value_method"] == "constant":
                    fill = CFG["numeric_constant"]
                else:
                    fill = tr[col].median() if CFG["missing_value_method"] == "median" else tr[col].mean()
                    if pd.isna(fill):
                        fill = CFG["numeric_constant"]
                for frame in (tr, va, te):
                    if frame is not None:
                        if CFG["missing_indicator"]:
                            frame[col + "__missing"] = frame[col].isna().astype("int8")
                        frame[col] = frame[col].fillna(fill)
        return tr, va, te

    def prepared_encoded(x_train, x_valid, x_test, model_name):
        if not CFG["missing_value_handling"] and model_name in ("extratrees", "logistic"):
            raise ValueError(f"{model_name} requires missing_value_handling=True")
        strategy = CFG["missing_value_method"]
        if strategy == "native" and model_name in ("extratrees", "logistic"):
            raise ValueError(f"{model_name} does not support native missing handling in this notebook")
        if strategy == "native":
            # XGBoost supports NaN; categorical missing is encoded as its own token.
            num_pipe = "passthrough"
        else:
            num_pipe = Pipeline([("imputer", SimpleImputer(strategy=strategy, fill_value=CFG["numeric_constant"],
                        add_indicator=CFG["missing_indicator"], keep_empty_features=True))])
        cat_pipe = Pipeline([("imputer", SimpleImputer(strategy="constant", fill_value=CFG["categorical_missing_token"])),
                             ("onehot", OneHotEncoder(handle_unknown="ignore"))])
        pre = ColumnTransformer([("num", num_pipe, num_cols), ("cat", cat_pipe, cat_cols)],
                                sparse_threshold=0.3)
        tr_frame, va_frame = x_train.copy(), x_valid.copy()
        te_frame = x_test.copy() if x_test is not None else None
        for frame in (tr_frame, va_frame, te_frame):
            if frame is not None:
                for col in cat_cols:
                    frame[col] = frame[col].astype(object).where(frame[col].notna(), np.nan)
        tr = pre.fit_transform(tr_frame)
        va = pre.transform(va_frame)
        te = pre.transform(te_frame) if te_frame is not None else None
        if model_name == "logistic":
            from sklearn.preprocessing import MaxAbsScaler
            scale = MaxAbsScaler()
            tr = scale.fit_transform(tr)
            va = scale.transform(va)
            te = scale.transform(te) if te is not None else None
        return tr, va, te, pre

    def apply_imbalance(tr, yy, seed):
        weights = None
        if not CFG["imbalance_class"]:
            return tr, yy, weights
        method = CFG["imbalance_method"]
        if method == "class_weight":
            weights = compute_sample_weight("balanced", yy)
        elif method == "random_over":
            rng = np.random.default_rng(seed)
            counts = np.bincount(yy, minlength=N_CLASSES)
            selected = [np.arange(len(yy))]
            for k in range(N_CLASSES):
                idx = np.flatnonzero(yy == k)
                selected.append(rng.choice(idx, size=counts.max() - len(idx), replace=True))
            picked = np.concatenate(selected)
            tr = tr.iloc[picked].reset_index(drop=True) if isinstance(tr, pd.DataFrame) else tr[picked]
            yy = yy[picked]
        else:
            from imblearn.over_sampling import SMOTE
            tr, yy = SMOTE(random_state=seed).fit_resample(tr, yy)
        return tr, yy, weights
    """),
    md("""## 4. Training, OOF, dan perbandingan model

    `eval_set` mengendalikan early stopping. Kurva loss yang ditampilkan adalah training/validation loss dari algoritme boosting, bukan loss neural network. Jika banyak eksperimen dicoba berdasarkan OOF, sisihkan validasi final yang tidak dipakai memilih model agar estimasi akhir tidak optimistis.
    """),
    code("""
    def metric_table(y_true, proba, threshold=None):
        p = np.clip(proba, 1e-7, 1-1e-7)
        pred = (p[:,1] >= threshold).astype(int) if N_CLASSES == 2 else p.argmax(axis=1)
        result = {"accuracy":accuracy_score(y_true,pred),
                  "balanced_accuracy":balanced_accuracy_score(y_true,pred),
                  "f1_macro":f1_score(y_true,pred,average="macro",zero_division=0),
                  "f1_weighted":f1_score(y_true,pred,average="weighted",zero_division=0),
                  "log_loss":log_loss(y_true,p,labels=np.arange(N_CLASSES))}
        if N_CLASSES == 2:
            result.update({"f1":f1_score(y_true,pred,zero_division=0),
                           "mcc":matthews_corrcoef(y_true,pred),
                           "brier":brier_score_loss(y_true,p[:,1])})
            if len(np.unique(y_true)) == 2:
                result["roc_auc"] = roc_auc_score(y_true,p[:,1])
                result["pr_auc"] = average_precision_score(y_true,p[:,1])
        else:
            if len(np.unique(y_true)) == N_CLASSES:
                result["roc_auc_ovr_macro"] = roc_auc_score(y_true,p,multi_class="ovr",average="macro")
        return result

    primary = CFG["primary_metric"]
    if primary == "auto":
        primary = "roc_auc" if N_CLASSES == 2 else "log_loss"
    valid_metrics = {"roc_auc", "pr_auc", "log_loss", "f1", "f1_macro", "accuracy", "balanced_accuracy"}
    if primary not in valid_metrics or (N_CLASSES > 2 and primary in {"roc_auc", "pr_auc", "f1"}):
        raise ValueError(f"Invalid primary metric for {N_CLASSES} classes: {primary}")
    print("Primary metric:", primary)

    def train_fold(model_name, xtr, xva, xte, ytr, yva, fold):
        import scipy.sparse as sp
        native = model_name in ("catboost", "lightgbm")
        if native:
            tr, va, te = prepared_native(xtr, xva, xte, model_name)
            pre = None
        else:
            tr, va, te, pre = prepared_encoded(xtr, xva, xte, model_name)
        tr, yfit, weights = apply_imbalance(tr, ytr.copy(), CFG["seed"]+fold)
        history = {}
        gpu_used = False
        if model_name == "catboost":
            from catboost import CatBoostClassifier
            params = dict(iterations=CFG["iterations"], learning_rate=CFG["learning_rate"], depth=6,
                          loss_function="Logloss" if N_CLASSES==2 else "MultiClass", random_seed=CFG["seed"]+fold,
                          verbose=False, allow_writing_files=False, thread_count=4)
            fit_args = dict(cat_features=cat_cols, eval_set=(va,yva), early_stopping_rounds=CFG["early_stopping_rounds"],
                            sample_weight=weights, verbose=False)
            if CFG["use_gpu"]:
                try:
                    model = CatBoostClassifier(**params, task_type="GPU", devices="0")
                    model.fit(tr, yfit, **fit_args)
                    gpu_used = True
                except Exception as exc:
                    warnings.warn(f"CatBoost GPU failed ({str(exc)[:180]}); retrying CPU")
            if not gpu_used:
                model = CatBoostClassifier(**params, task_type="CPU")
                model.fit(tr, yfit, **fit_args)
            history = model.get_evals_result()
        elif model_name == "lightgbm":
            import lightgbm as lgb
            params = dict(n_estimators=CFG["iterations"], learning_rate=CFG["learning_rate"], num_leaves=31,
                          max_depth=-1, colsample_bytree=0.85, subsample=0.85, subsample_freq=1,
                          min_child_samples=20, random_state=CFG["seed"]+fold, n_jobs=4, verbosity=-1)
            fit_args = dict(eval_set=[(tr, yfit), (va,yva)], eval_names=["train", "validation"],
                            eval_metric="binary_logloss" if N_CLASSES==2 else "multi_logloss",
                            sample_weight=weights,
                            callbacks=[lgb.early_stopping(CFG["early_stopping_rounds"], verbose=False), lgb.log_evaluation(0)])
            if CFG["use_gpu"]:
                try:
                    model = lgb.LGBMClassifier(**params, device_type="gpu")
                    model.fit(tr, yfit, **fit_args)
                    gpu_used = True
                except Exception as exc:
                    warnings.warn(f"LightGBM GPU failed ({str(exc)[:180]}); retrying CPU")
            if not gpu_used:
                model = lgb.LGBMClassifier(**params, device_type="cpu")
                model.fit(tr, yfit, **fit_args)
            history = model.evals_result_
        elif model_name == "xgboost":
            from xgboost import XGBClassifier
            params = dict(n_estimators=CFG["iterations"], learning_rate=CFG["learning_rate"], max_depth=6,
                          subsample=0.85, colsample_bytree=0.85, tree_method="hist", random_state=CFG["seed"]+fold,
                          n_jobs=4, objective="binary:logistic" if N_CLASSES==2 else "multi:softprob",
                          eval_metric="logloss" if N_CLASSES==2 else "mlogloss",
                          early_stopping_rounds=CFG["early_stopping_rounds"])
            if N_CLASSES > 2:
                params["num_class"] = N_CLASSES
            if CFG["use_gpu"]:
                try:
                    model = XGBClassifier(**params, device="cuda")
                    model.fit(tr,yfit,eval_set=[(tr,yfit),(va,yva)],sample_weight=weights,verbose=False)
                    gpu_used = True
                except Exception as exc:
                    warnings.warn(f"XGBoost GPU failed ({str(exc)[:180]}); retrying CPU")
            if not gpu_used:
                model = XGBClassifier(**params, device="cpu")
                model.fit(tr,yfit,eval_set=[(tr,yfit),(va,yva)],sample_weight=weights,verbose=False)
            history = model.evals_result()
        elif model_name == "extratrees":
            model = ExtraTreesClassifier(n_estimators=400, min_samples_leaf=2, max_features=0.8,
                                         random_state=CFG["seed"]+fold, n_jobs=4)
            model.fit(tr,yfit,sample_weight=weights)
        elif model_name == "logistic":
            model = LogisticRegression(max_iter=1000, C=1.0, solver="lbfgs")
            model.fit(tr,yfit,sample_weight=weights)
        else:
            raise ValueError(f"Unknown model: {model_name}")
        pred_va = model.predict_proba(va)
        pred_te = model.predict_proba(te) if te is not None else None
        if CFG["save_models"]:
            import joblib
            joblib.dump({"model":model,"preprocessor":pre,"features":features,"classes":labels.classes_}, OUT/f"{model_name}_fold{fold}.joblib")
        return pred_va, pred_te, history, model, gpu_used

    all_oof, all_test, fold_rows, histories, importances = {}, {}, [], {}, []
    for model_name in CFG["models"]:
        print("\\nTraining:", model_name)
        oof = np.full((len(X),N_CLASSES), np.nan)
        test_fold_predictions = []
        for fold,(tr_idx,va_idx) in enumerate(splits,1):
            pv,pt,hist,model,gpu = train_fold(model_name, X.iloc[tr_idx], X.iloc[va_idx], X_test,
                                             y[tr_idx],y[va_idx],fold)
            oof[va_idx] = pv
            if pt is not None:
                test_fold_predictions.append(pt)
            if hist:
                histories[(model_name,fold)] = hist
            if model_name in ("catboost","lightgbm"):
                names = list(model.feature_names_in_) if hasattr(model,"feature_names_in_") else list(model.feature_names_)
                for name,score in zip(names,model.feature_importances_):
                    importances.append({"model":model_name,"fold":fold,"feature":name,"importance":float(score)})
            row = {"model":model_name,"fold":fold,"gpu":gpu, **metric_table(y[va_idx],pv,CFG["binary_threshold"])}
            fold_rows.append(row)
            print(f"  fold {fold}: {primary}={row.get(primary,float('nan')):.5f}, GPU={gpu}")
        all_oof[model_name] = oof
        if test_fold_predictions:
            all_test[model_name] = np.mean(test_fold_predictions, axis=0)
    if CFG["ensemble"] and len(all_oof) > 1:
        all_oof["ensemble"] = np.mean(np.stack(list(all_oof.values())),axis=0)
        if all_test:
            all_test["ensemble"] = np.mean(np.stack(list(all_test.values())),axis=0)
    fold_df = pd.DataFrame(fold_rows)
    fold_df.to_csv(OUT/"fold_metrics.csv",index=False)
    display(fold_df)
    summary = []
    for name,p in all_oof.items():
        mask = np.isfinite(p).all(axis=1)
        summary.append({"model":name,"oof_rows":int(mask.sum()),**metric_table(y[mask],p[mask],CFG["binary_threshold"])})
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(OUT/"oof_model_comparison.csv",index=False)
    display(summary_df.sort_values(primary,ascending=(primary=="log_loss")))
    """),
    md("""## 5. Visualisasi evaluasi dan error analysis

    Semua metrik dan plot memakai prediksi OOF, sehingga setiap baris dinilai oleh model yang tidak dilatih pada baris tersebut. Untuk split waktu, baris awal yang tidak memiliki OOF dikeluarkan dari evaluasi.
    """),
    code("""
    best_name = summary_df.sort_values(primary,ascending=(primary=="log_loss")).iloc[0]["model"]
    best_proba = all_oof[best_name]
    valid_mask = np.isfinite(best_proba).all(axis=1)
    yy, pp = y[valid_mask], best_proba[valid_mask]
    pred = (pp[:,1] >= CFG["binary_threshold"]).astype(int) if N_CLASSES==2 else pp.argmax(axis=1)
    print("Best OOF model:", best_name)
    print(classification_report(yy,pred,labels=np.arange(N_CLASSES),target_names=list(map(str,labels.classes_)),zero_division=0))
    pd.DataFrame({"actual":labels.inverse_transform(yy),"predicted":labels.inverse_transform(pred),
                  "confidence":pp.max(axis=1)}).to_csv(OUT/"oof_errors.csv",index=False)
    pd.DataFrame(best_proba,columns=[f"proba_{str(c)}" for c in labels.classes_]).assign(
        target=train[target].values,has_oof=valid_mask).to_csv(OUT/"oof_predictions.csv",index=False)
    cm = confusion_matrix(yy,pred,labels=np.arange(N_CLASSES))
    fig,axs = plt.subplots(1,2,figsize=(13,5))
    sns.heatmap(cm,annot=True,fmt="d",cmap="Blues",xticklabels=labels.classes_,yticklabels=labels.classes_,ax=axs[0])
    axs[0].set(xlabel="Predicted",ylabel="Actual",title="OOF confusion matrix: counts")
    sns.heatmap(cm/cm.sum(axis=1,keepdims=True).clip(min=1),annot=True,fmt=".2f",cmap="Blues",
                xticklabels=labels.classes_,yticklabels=labels.classes_,ax=axs[1])
    axs[1].set(xlabel="Predicted",ylabel="Actual",title="OOF confusion matrix: row normalized")
    fig.tight_layout(); fig.savefig(OUT/"confusion_matrix.png",dpi=150); plt.show()

    matrix = fold_df.pivot(index="model",columns="fold",values=primary)
    fig,ax = plt.subplots(figsize=(max(6,CFG["n_splits"]*1.2),max(3,len(matrix)*0.7)))
    sns.heatmap(matrix,annot=True,fmt=".4f",cmap="viridis",ax=ax)
    ax.set_title(f"Fold metric matrix: {primary}")
    fig.tight_layout(); fig.savefig(OUT/"fold_metric_matrix.png",dpi=150); plt.show()
    for (name,fold),hist in histories.items():
        fig,ax = plt.subplots(figsize=(8,4))
        for dataset,metrics in hist.items():
            loss_keys = [key for key in metrics if "loss" in key.lower()]
            if loss_keys:
                key = loss_keys[0]
                ax.plot(metrics[key],label=f"{dataset}: {key}")
        if ax.lines:
            ax.legend(); ax.set(xlabel="Iteration",ylabel="Loss",title=f"Training loss: {name} fold {fold}")
            fig.tight_layout(); fig.savefig(OUT/f"training_loss_{name}_fold{fold}.png",dpi=140)
            plt.show()
        else:
            plt.close(fig)
    if importances:
        imp = pd.DataFrame(importances)
        imp.to_csv(OUT/"feature_importance_folds.csv",index=False)
        ranked = imp.groupby(["model","feature"],as_index=False).importance.mean()
        for name,part in ranked.groupby("model"):
            top = part.nlargest(20,"importance")
            fig,ax = plt.subplots(figsize=(9,max(4,len(top)*0.32)))
            sns.barplot(data=top,x="importance",y="feature",ax=ax)
            ax.set_title(f"Feature importance: {name} (model-specific)")
            fig.tight_layout(); fig.savefig(OUT/f"feature_importance_{name}.png",dpi=140); plt.show()
    """),
    code("""
    if N_CLASSES == 2:
        fig,axs = plt.subplots(1,3,figsize=(17,4.5))
        fpr,tpr,_ = roc_curve(yy,pp[:,1])
        axs[0].plot(fpr,tpr,label=f"AUC={roc_auc_score(yy,pp[:,1]):.4f}"); axs[0].plot([0,1],[0,1],"--",color="gray")
        axs[0].set(xlabel="FPR",ylabel="TPR",title="OOF ROC"); axs[0].legend()
        precision,recall,_ = precision_recall_curve(yy,pp[:,1])
        axs[1].plot(recall,precision,label=f"AP={average_precision_score(yy,pp[:,1]):.4f}")
        axs[1].set(xlabel="Recall",ylabel="Precision",title="OOF precision-recall"); axs[1].legend()
        from sklearn.calibration import calibration_curve
        frac,mean = calibration_curve(yy,pp[:,1],n_bins=10,strategy="quantile")
        axs[2].plot(mean,frac,"o-"); axs[2].plot([0,1],[0,1],"--",color="gray")
        axs[2].set(xlabel="Mean predicted probability",ylabel="Observed positive rate",title="OOF calibration")
        fig.tight_layout(); fig.savefig(OUT/"binary_roc_pr_calibration.png",dpi=150); plt.show()
        fig,ax=plt.subplots(figsize=(8,4))
        sns.histplot(x=pp[:,1],hue=labels.inverse_transform(yy),bins=30,stat="density",common_norm=False,ax=ax)
        ax.axvline(CFG["binary_threshold"],color="black",linestyle="--")
        ax.set_title("OOF predicted probability by actual class")
        fig.tight_layout(); fig.savefig(OUT/"binary_score_distribution.png",dpi=140); plt.show()
        thresholds = np.linspace(0.05,0.95,37)
        sweep = pd.DataFrame({"threshold":thresholds,
                              "f1":[f1_score(yy,pp[:,1]>=t,zero_division=0) for t in thresholds],
                              "balanced_accuracy":[balanced_accuracy_score(yy,pp[:,1]>=t) for t in thresholds]})
        sweep.to_csv(OUT/"threshold_sweep_oof_diagnostic.csv",index=False)
        ax=sweep.plot(x="threshold",y=["f1","balanced_accuracy"],figsize=(8,4),title="OOF threshold sensitivity (diagnostic only)")
        ax.axvline(CFG["binary_threshold"],color="black",linestyle="--")
        plt.tight_layout(); plt.savefig(OUT/"binary_threshold_sensitivity.png",dpi=140); plt.show()
    else:
        onehot = label_binarize(yy,classes=np.arange(N_CLASSES))
        fig,axs = plt.subplots(1,2,figsize=(12,5))
        for k,label in enumerate(labels.classes_):
            if len(np.unique(onehot[:,k])) < 2:
                continue
            fpr,tpr,_=roc_curve(onehot[:,k],pp[:,k])
            axs[0].plot(fpr,tpr,label=str(label))
            precision,recall,_=precision_recall_curve(onehot[:,k],pp[:,k])
            axs[1].plot(recall,precision,label=str(label))
        axs[0].set(xlabel="FPR",ylabel="TPR",title="OOF one-vs-rest ROC")
        axs[1].set(xlabel="Recall",ylabel="Precision",title="OOF one-vs-rest PR")
        axs[0].legend(); axs[1].legend(); fig.tight_layout()
        fig.savefig(OUT/"multiclass_ovr_roc_pr.png",dpi=150); plt.show()
        fig,ax=plt.subplots(figsize=(9,4))
        sns.histplot(pp.max(axis=1),bins=30,ax=ax)
        ax.set(xlabel="Maximum predicted class probability",title="OOF confidence distribution")
        fig.tight_layout(); fig.savefig(OUT/"multiclass_confidence.png",dpi=140); plt.show()
    """),
    md("""## 6. Submission

    Format `auto` memakai kolom sample submission. Untuk satu kolom target, binary menghasilkan probabilitas kelas `labels.classes_[1]`; multiclass menghasilkan label. Bila sample submission berisi satu kolom per kelas, probabilitas ditulis menurut nama kelas. Selalu cek metrik dan format resmi kompetisi.
    """),
    code("""
    if X_test is not None:
        ptest = all_test[best_name]
        mode = CFG["submission_mode"]
        if sample_submission is not None:
            if len(sample_submission) != len(ptest):
                raise ValueError("sample_submission length differs from test length")
            submission = sample_submission.copy()
            pred_cols = [c for c in submission if c not in CFG["id_columns"]]
            class_cols = [c for c in submission if str(c) in set(map(str,labels.classes_))]
            if len(class_cols) == N_CLASSES:
                for k,label in enumerate(labels.classes_):
                    submission[str(label)] = ptest[:,k]
            elif len(pred_cols) == 1:
                col = pred_cols[0]
                if mode == "auto":
                    mode = "probability" if N_CLASSES==2 else "label"
                if mode == "probability":
                    if N_CLASSES != 2:
                        raise ValueError("Multiclass probabilities need one sample_submission column per class.")
                    submission[col] = ptest[:,1]
                elif mode == "label":
                    submission[col] = labels.inverse_transform(ptest.argmax(axis=1))
                else:
                    raise ValueError("Invalid submission_mode")
            else:
                raise ValueError(f"Cannot infer submission mapping from columns {pred_cols}; edit this cell for competition format.")
        else:
            submission = pd.DataFrame(index=np.arange(len(ptest)))
            for col in CFG["id_columns"]:
                submission[col] = test[col].values
            if mode == "auto":
                mode = "probability" if N_CLASSES==2 else "label"
            if mode == "probability" and N_CLASSES==2:
                submission[target] = ptest[:,1]
            elif mode == "label":
                submission[target] = labels.inverse_transform(ptest.argmax(axis=1))
            else:
                for k,label in enumerate(labels.classes_):
                    submission[str(label)] = ptest[:,k]
        submission.to_csv(OUT/"submission.csv",index=False)
        display(submission.head())
        print("Saved:",OUT/"submission.csv")
    else:
        print("No test data: OOF evaluation complete; submission skipped.")
    print("All artifacts:")
    for path in sorted(OUT.iterdir()):
        print(path.name)
    """),
]


for slug, expected, title in [("binary", 2, "Klasifikasi biner"), ("multiclass", None, "Klasifikasi multikelas")]:
    cells = [dict(cell) for cell in COMMON]
    cells[0] = md(f"# {title}\n\n" + "".join(COMMON[0]["source"]).split("\n", 1)[1])
    constant = "EXPECTED_CLASSES = 2\n" if expected == 2 else "EXPECTED_CLASSES = None  # any number >= 3\n"
    if expected is None:
        constant = "EXPECTED_CLASSES = None\n"
    cells.insert(2, code(constant))
    if expected is None:
        # The shared check uses this sentinel to assert multi-class.
        source = "".join(cells[8]["source"])
        source = source.replace("if N_CLASSES != EXPECTED_CLASSES:", "if N_CLASSES < 3:")
        source = source.replace("Notebook expects {EXPECTED_CLASSES} classes", "Multiclass notebook expects >=3 classes")
        cells[8]["source"] = source.splitlines(True)
    notebook = {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
                                           "language_info":{"name":"python","version":"3.11"}},"nbformat":4,"nbformat_minor":5}
    (OUT/f"tabular_{slug}_kaggle.ipynb").write_text(json.dumps(notebook,ensure_ascii=False,indent=1),encoding="utf-8")
    print(OUT/f"tabular_{slug}_kaggle.ipynb")
