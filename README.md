# Toolkit kompetisi tabular Kaggle

Dua notebook standalone untuk klasifikasi tabular, enam panduan use case untuk agent, dan [riset metode](RESEARCH.md). Notebook ditujukan untuk **Kaggle GPU T4 x2**, tetapi setiap fit GBDT memakai satu GPU; jika build GPU bermasalah, kode mencoba CPU. Tidak perlu mengunggah `build_notebooks.py` atau file skill untuk menjalankan notebook.

## File

| File | Fungsi |
| --- | --- |
| [Binary notebook](notebooks/tabular_binary_kaggle.ipynb) | Tepat dua kelas; OOF, ROC/PR, kalibrasi, threshold diagnostic, submission. |
| [Multiclass notebook](notebooks/tabular_multiclass_kaggle.ipynb) | Tiga kelas atau lebih; OOF, laporan per kelas, OvR ROC/PR, submission. |
| [Skill router](skills/tabular-competition/SKILL.md) | Pintu masuk agent; mengarahkan ke panduan binary, multiclass, EDA, cleaning, istilah presentasi, dan konten PPT. |
| [Riset](RESEARCH.md) | Bukti, sumber primer, pilihan metode, batasan. |
| [Generator](build_notebooks.py) | Memelihara isi kedua notebook; notebook hasilnya tetap standalone. |

Panduan agent bernama sesuai permintaan: [skill_binary_classification.md](skills/tabular-competition/skill_binary_classification.md), [skill_multiclass_classification.md](skills/tabular-competition/skill_multiclass_classification.md), [skill_eda.md](skills/tabular-competition/skill_eda.md), [skill_data_cleaning.md](skills/tabular-competition/skill_data_cleaning.md), [skill_larp.md](skills/tabular-competition/skill_larp.md) untuk istilah teknis, dan [skill_ppt.md](skills/tabular-competition/skill_ppt.md) untuk konten presentasi per slide beserta rancangan visual dan catatan presenter.

## Pemakaian cepat

1. Upload notebook yang sesuai ke Kaggle, tambah dataset kompetisi sebagai input, dan pilih **Accelerator → GPU T4 x2**. Internet hanya diperlukan jika paket yang diminta notebook belum tersedia di image Kaggle.
2. Edit **sel `CFG`**: minimal cek `target`, `id_columns`, `primary_metric`, `split_type`, dan format sample submission. Jika lebih dari satu `train.csv` di input, isi path eksplisit. Untuk group/time split, isi kolomnya.
3. Jalankan semua sel. Hasil ada di `/kaggle/working/tabular_outputs/`, termasuk `submission.csv` bila `test.csv` ada. Sebelum submit, cocokkan nama dan urutan kolom dengan sample submission resmi.

`target=None` hanya dapat diinfer bila tepat satu kolom train tidak ada di test. Bila tidak ada test, isi `target` dan `train_path`. Notebook akan menolak jumlah kelas yang salah, split tanpa semua kelas di training, kombinasi SMOTE dengan kategori, dan schema submission ambigu.

## Konfigurasi

| Opsi | Nilai / arti |
| --- | --- |
| `train_path`, `test_path`, `sample_submission_path` | Path CSV atau auto-discovery tunggal di `/kaggle/input`. `test_path` opsional untuk validasi saja. |
| `target`, `id_columns`, `drop_columns` | Label, ID yang tidak dijadikan fitur, dan fitur yang diketahui bocor/tidak diizinkan. |
| `group_column`, `time_column`, `date_columns` | Entitas untuk group CV, urutan waktu, dan tanggal yang diekstrak ke fitur kalender. Kalender harus tersedia saat inference. |
| `split_type`, `n_splits`, `time_gap` | `stratified`, `group`, atau `time`; jumlah fold; embargo dalam **baris** untuk split waktu. |
| `models` | `catboost`, `lightgbm`, `xgboost`, `extratrees`, `logistic`; default dua GBDT pertama. Bisa lebih dari satu untuk perbandingan/ensemble. |
| `primary_metric` | `auto`: ROC AUC untuk binary, log loss untuk multiclass. Binary juga `pr_auc`, `log_loss`, `f1`, `balanced_accuracy`; multiclass juga `f1_macro`, `accuracy`, `balanced_accuracy`. |
| `ensemble` | Rata-rata probabilitas model yang dipilih, dievaluasi di OOF; bukan stacking. |
| `use_gpu` | Coba GPU pertama untuk CatBoost, LightGBM, XGBoost; fallback CPU. ExtraTrees/logistic selalu CPU. |
| `iterations`, `learning_rate`, `early_stopping_rounds` | Anggaran boosting dan early stopping. |
| `eda`, `eda_sample_rows`, `eda_top_features` | Nyalakan visualisasi EDA dan batasi jumlah baris/fitur plot. Audit CSV tetap dibuat. |
| `missing_value_handling`, `missing_value_method`, `missing_indicator`, `numeric_constant`, `categorical_missing_token`, `missing_tokens` | `median`, `mean`, `constant`, atau `native`; statistik imputer di-fit per fold. Native untuk tree yang mendukung. Kategori missing memakai token eksplisit. |
| `strip_string_whitespace`, `drop_duplicate_rows` | Cleaning deterministik; duplikat identik di train dapat dihapus bila diperiksa. |
| `imbalance_class`, `imbalance_method` | `class_weight`, `random_over`, `smote_numeric`; sampling hanya pada training fold. `smote_numeric` menolak kolom kategori. |
| `binary_threshold` | Threshold tetap untuk laporan binary; sweep OOF disimpan sebagai diagnostik saja. |
| `submission_mode` | `auto`, `probability`, `label`. Pada binary satu kolom default probabilitas kelas kedua menurut `LabelEncoder`; cek positive class resmi. |
| `save_models`, `output_dir`, `seed` | Simpan model/preprocessor per fold, direktori hasil, dan seed. |

## Visualisasi dan berkas keluaran

| Keluaran | Isi |
| --- | --- |
| `eda_target.png`, `eda_missing.png`, `eda_missing_by_target.png`, `eda_numeric_distributions.png`, `eda_correlations.png` | Komposisi kelas, missingness keseluruhan dan per kelas, distribusi numerik, korelasi Spearman. Yang tidak relevan pada dataset tertentu tidak dibuat. |
| `eda_relation_num_*.png`, `eda_relation_cat_*.png` | Hubungan numerik/kategori dengan kelas target. |
| `eda_train_test_drift.png`, `eda_numeric_drift.csv`, `eda_categorical_drift.csv`, `eda_missing_by_target.csv` | Statistik KS numerik, kategori test yang belum pernah terlihat, dan missingness per kelas. Sinyal shift, bukan tes kebocoran otomatis. |
| `train_audit.csv`, `test_audit.csv` | Dtype, missing, cardinality, contoh nilai; log ringkas duplikat dan schema ditampilkan di notebook. |
| `fold_metrics.csv`, `fold_metric_matrix.png`, `oof_model_comparison.csv` | Skor per fold, heatmap metrik utama, dan perbandingan OOF. |
| `training_loss_<model>_fold<n>.png` | Kurva training/validation loss untuk model boosting; baseline sklearn tidak punya loss iteratif. |
| `confusion_matrix.png`, `oof_errors.csv`, `oof_predictions.csv` | Confusion count/normalized, prediksi OOF dan error untuk ditinjau. |
| `feature_importance_<model>.png`, `feature_importance_folds.csv` | Importance internal CatBoost/LightGBM; model-specific, bukan kausal. |
| `binary_roc_pr_calibration.png`, `binary_score_distribution.png`, `binary_threshold_sensitivity.png`, `threshold_sweep_oof_diagnostic.csv` | Diagnostik khusus binary. |
| `multiclass_ovr_roc_pr.png`, `multiclass_confidence.png` | Diagnostik khusus multiclass. |
| `submission.csv` | Prediksi test menurut sample submission atau format default. |

## Keputusan penting dan batas

- Untuk data dengan entitas berulang atau urutan waktu, ubah `split_type` sebelum membandingkan model. EDA tidak bisa mengetahui kapan sebuah fitur dikumpulkan; tinjau metadata kompetisi untuk mencegah target leakage.
- `missing_value_handling=False` mensyaratkan `missing_value_method="native"` untuk numerik; kategori kosong tetap diberi token eksplisit agar CatBoost dan encoder dapat membacanya.
- Paket ini tidak mengklaim satu preprocessing atau model sebagai terbaik universal. `AutoGluon` dan `TabPFN` dibahas di riset sebagai eksperimen lanjutan, tetapi **belum menjadi opsi `models`** pada notebook karena ketergantungan, bobot/lisensi, dan pola validasi yang berbeda.
- `sample_submission.csv` dengan kolom kelas ambigu memerlukan pemetaan manual. Multiclass probability submission hanya otomatis bila nama kolom kelas sama dengan label target.
- Fold waktu tidak memberi OOF pada blok awal; perbandingan hanya memakai baris yang punya OOF. Jika kelas absen pada validation fold, beberapa metrik tidak terdefinisi. Angka dari banyak percobaan pada OOF yang sama dapat terlalu optimistis; gunakan holdout final atau nested CV untuk evaluasi akhir.
- Notebook menginstal paket yang belum ada. Jika Kaggle Internet Off dan paket tidak tersedia, unggah wheel/dataset dependency atau pilih model yang sudah tersedia.

## Pengembangan

Ubah `build_notebooks.py`, lalu jalankan `python build_notebooks.py` untuk menyegarkan kedua notebook. Validasi sintaks dan smoke test ada di `tests/smoke_notebooks.py`.
