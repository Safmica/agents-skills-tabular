# Riset metode kompetisi ML tabular

**Diperiksa 17 Oktober 2026.** Fokus: klasifikasi biner dan multikelas pada Kaggle T4 x2. SOTA di sini berarti bukti benchmark terkini, bukan jaminan menang pada dataset tertentu. Semua klaim metode di bawah merujuk ke sumber primer; versi dan batas lisensi harus dicek kembali saat memakai model baru.

## 1. Apa yang benar-benar kuat saat ini

| Kandidat | Bukti dan kecocokan | Biaya / batas | Keputusan praktis |
| --- | --- | --- | --- |
| CatBoost | Boosted trees tetap kuat pada benchmark [TabArena](https://proceedings.neurips.cc/paper_files/paper/2025/hash/1697e3fb412da11dc9488249f9e7bbc9-Abstract-Datasets_and_Benchmarks_Track.html); kategori ditangani internal dengan statistik berurutan, [tanpa one-hot manual](https://catboost.ai/docs/en/features/categorical-features). | GPU kadang gagal bergantung build dan kategorikal; fit CPU lebih lambat. | Baseline pertama untuk fitur campuran dan kategori ber-cardinality tinggi. |
| LightGBM | Alternatif GBDT cepat, dengan [kategori dan NaN native](https://lightgbm.readthedocs.io/en/latest/Advanced-Topics.html). | Paket Kaggle bisa tidak dibangun dengan dukungan GPU; fallback CPU perlu diuji. | Baseline kedua dan kandidat ensemble. |
| XGBoost | GBDT mapan; dokumentasi menyediakan [`tree_method="hist"`, `device="cuda"`](https://xgboost.readthedocs.io/en/stable/gpu/index.html). | Encoding kategorikal perlu diputuskan; satu GPU per fit pada template. | Baseline pembanding dan kandidat ensemble. |
| AutoGluon Tabular | [Dokumentasi 1.6](https://auto.gluon.ai/stable/tutorials/tabular/tabular-essentials.html) menguraikan preset `best`, `extreme`, dan `noncommercial`; [TabArena](https://github.com/autogluon/tabarena) menekankan validasi dan ensemble lintas model. | Instalasi, RAM, disk, dan runtime jauh lebih besar; model tertentu memiliki batas lisensi. | Eksperimen lanjutan pada anggaran memadai, setelah CV dan baseline benar. Belum otomatis ada di dua template ringan. |
| TabPFN family dan model fondasi tabular | [Nature 2025](https://www.nature.com/articles/s41586-024-08328-6) menunjukkan keuntungan pada data kecil; [TabArena](https://proceedings.neurips.cc/paper_files/paper/2025/hash/1697e3fb412da11dc9488249f9e7bbc9-Abstract-Datasets_and_Benchmarks_Track.html) juga menempatkan foundation models kuat pada dataset kecil. Versi lebih baru muncul cepat. | Skalabilitas, VRAM, latensi inferensi, dan lisensi berbeda antarversi; unduhan bobot mungkin tak tersedia pada Kaggle tanpa internet. | Kandidat opsional untuk data kecil/menengah; cek dokumentasi versi tepat, lisensi, aturan kompetisi, dan akses bobot. |
| ExtraTrees / regresi logistik | Bukan klaim SOTA; pembanding yang menguji apakah boosting memberi keuntungan nyata. | Perlu encoding/imputasi; regresi logistik perlu skala. | Sanity check dan diversitas ensemble. |

**Interpretasi:** [TabArena](https://proceedings.neurips.cc/paper_files/paper/2025/hash/1697e3fb412da11dc9488249f9e7bbc9-Abstract-Datasets_and_Benchmarks_Track.html) menunjukkan GBDT masih kuat; deep learning menyamai atau melampaui pada sebagian setup dengan anggaran besar dan ensemble; foundation models menonjol pada data kecil; ensemble lintas metode bisa meningkatkan performa. Tidak ada satu model terbaik untuk semua tabel. Benchmark IID tidak otomatis mewakili kompetisi dengan shift waktu, grup, atau kebocoran. [TabReD](https://proceedings.neurips.cc/paper_files/paper/2024/file/ae00e5ce7142d02e30a8235ede1ec6fc-Paper-Datasets_and_Benchmarks_Track.pdf) menyoroti perlunya evaluasi temporal yang realistis.

## 2. Preprocessing yang paling dapat dipertanggungjawabkan

- **Split lebih dulu; fit transformasi hanya pada fold training.** [Scikit-learn](https://scikit-learn.org/stable/modules/compose.html) secara eksplisit menyebut test-informed imputation/scaling sebagai leakage. Untuk baris independen pakai stratified CV; untuk entitas berulang gunakan [StratifiedGroupKFold](https://scikit-learn.org/stable/modules/cross_validation.html); untuk prediksi masa depan gunakan [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) atau split khusus kompetisi.
- **Encoding sesuai model.** CatBoost lebih baik diberi fitur kategorikal asli [menurut dokumentasinya](https://catboost.ai/docs/en/features/categorical-features). LightGBM memakai pandas `category` dan NaN native. Model linear, ExtraTrees, dan template XGBoost memakai [OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html) per fold dengan kategori asing aman. One-hot untuk high-cardinality dapat membengkakkan memori; bandingkan native category atau encoding dengan cross-fitting jika perlu.
- **Missing value sederhana dahulu.** NaN native pada tree yang mendukung, atau median/mean/constant plus indikator missing. [Scikit-learn](https://scikit-learn.org/stable/modules/impute.html) menjelaskan indikator missing dapat membawa sinyal. Imputer kompleks seperti [ReMasker](https://arxiv.org/abs/2309.13793) menjanjikan pada rekonstruksi, tetapi kualitas imputasi bukan jaminan metrik kompetisi lebih baik. Pilih dengan CV.
- **Imbalance.** Evaluasi tanpa koreksi dahulu, lalu class/sample weights dan random oversampling hanya dalam training fold. [Imbalanced-learn](https://imbalanced-learn.org/stable/common_pitfalls.html) menunjukkan resampling sebelum split menghasilkan skor optimistis. SMOTE polos tidak sesuai untuk fitur kategori campuran; template membatasi `smote_numeric` pada data numerik.
- **Kalibrasi dan threshold.** ROC AUC tidak tergantung threshold; log loss/Brier menguji probabilitas; F1 bergantung threshold. [Scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html) mengharuskan data terpisah untuk fitting kalibrator. Sweep threshold pada OOF yang sama bersifat diagnostik, bukan estimasi final tak bias.

## 3. EDA dan cleaning: tidak ada satu algoritme SOTA universal

[REIN](https://arxiv.org/abs/2302.04702) membandingkan berbagai metode cleaning dan menunjukkan masalahnya berbeda: missing, outlier, duplikat, pelanggaran pola, inkonsistensi. Karena itu EDA harus memetakan *jenis kesalahan* dan *dampaknya pada label serta validation*, bukan otomatis menghapus seluruh baris bermasalah.

Urutan diagnosis yang bernilai tinggi: (1) pahami unit baris, target, metrik, sample submission, dan batas waktu label; (2) audit schema, missing, sentinel, parse, duplicate, label konflik, rentang dan satuan; (3) cek hubungan fitur-target dan missing-target; (4) cek kesamaan entitas antar fold dan potensi target leakage; (5) cek shift train/test dan kelas per fold; (6) lakukan ablation per tindakan cleaning menggunakan CV tetap. Plot distribusi atau feature importance adalah petunjuk; bukan bukti kausal. [Permutation importance pada validation](https://scikit-learn.org/stable/modules/permutation_importance.html) lebih tepat untuk menguji kontribusi prediksi dibanding impurity importance, walaupun fitur yang saling berkorelasi tetap dapat menyesatkan.

**Cleaning yang aman secara default:** normalisasi whitespace/sentinel yang benar-benar diketahui, konversi numerik yang dapat diaudit, parsing tanggal eksplisit, deteksi duplikat dan label konflik. Jangan memperbaiki label secara otomatis, menghapus semua outlier tanpa bukti, atau membuat agregasi dengan informasi setelah waktu prediksi.

## 4. Implikasi T4 x2 dan notebook

[Dokumentasi Kaggle](https://www.kaggle.com/docs/notebooks) mencantumkan T4 x2 sebagai pilihan akselerator dan batas runtime/disk; ketersediaan, paket pra-instal, kuota, dan internet dapat berubah. Dua T4 **tidak berarti** satu fit CatBoost/LightGBM/XGBoost otomatis memakai keduanya. Template memakai GPU pertama saat tersedia, lalu CPU fallback; ia tidak menjanjikan percepatan 2×. Opsi model fondasi/AutoGluon tidak menjadi default karena kebutuhan paket, bobot, lisensi, dan anggaran dapat berbeda pada setiap kompetisi.

## 5. Prioritas eksperimen yang rasional

1. Tetapkan metrik resmi, split, positive class/class order, dan format submission. Buat baseline sederhana dan skor OOF yang dapat direproduksi.
2. Bandingkan CatBoost dan LightGBM pada CV identik; tambahkan XGBoost. Perhatikan mean, variasi fold, durasi, dan error per kelas.
3. Uji satu perubahan per eksperimen: missing strategy, class weights, feature engineering berbasis domain, regularisasi, atau blending. Simpan konfigurasi dan OOF untuk semua percobaan.
4. Jika dana komputasi ada, pertimbangkan AutoGluon/TabPFN sesuai batas dataset dan lisensi, lalu bandingkan dengan baseline pada split yang sama.
5. Buat submission hanya setelah memeriksa urutan kelas/kolom dan aturan kompetisi; leaderboard publik tidak menggantikan validasi lokal.

## Batas paket ini

Dua notebook mendukung klasifikasi biner/multikelas dengan model GBDT dan baseline sklearn. Regresi, multi-label, learning-to-rank, survival, gambar/teks bebas, relasi antartabel, custom metric, dan feature engineering temporal berstate membutuhkan notebook tersendiri. EDA dan audit yang luas tidak dapat menjamin menemukan setiap leakage semantik. Contoh Kaggle harus diuji lagi pada dataset aktual karena schema, metrik, dan submission bisa sangat khusus.
