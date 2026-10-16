# Skill: kosakata teknis untuk presentasi kompetisi tabular

Gunakan glosarium ini ketika agent menyiapkan narasi, slide, speaker notes, atau jawaban juri dari notebook klasifikasi tabular. Tujuannya adalah **menjelaskan keputusan teknis secara presisi**. Pilih istilah yang memang relevan; satu istilah yang diikuti bukti lebih kuat daripada sepuluh jargon tanpa hasil.

## Cara memakai

- **[Ada]** berarti notebook bawaan menghasilkan bukti yang bisa ditunjuk. Sebut file, grafik, metrik, dan angka aktual; jangan mengarang nilainya.
- **[Opsional]** berarti konsep atau teknik yang perlu eksperimen/kode tambahan sebelum diklaim sudah dilakukan.
- **[Konsep]** berarti kerangka untuk menjelaskan hasil, bukan hasil yang otomatis dibuktikan notebook.
- Untuk setiap klaim, susun kalimat **keputusan → alasan → bukti → batas**. Contoh: “Kami memilih group CV karena beberapa baris berasal dari entitas sama; fold memisahkan entitas, skor OOF tercatat di `fold_metrics.csv`, dan hasil ini tetap perlu diuji pada distribusi private test.”
- Jangan menyebut korelasi sebagai kausalitas, OOF sebagai hidden-test score, atau skor tertinggi dari banyak percobaan sebagai estimasi tak bias. Jangan menyebut metode yang belum dijalankan seolah sudah ada di notebook.

## 1. Struktur masalah dan kualitas data

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| Unit observasi | Apa yang direpresentasikan satu baris: orang, transaksi, sesi, atau kejadian. | [Konsep] Definisi dataset. |
| Granularitas data | Tingkat detail setiap baris dan kolom. | [Konsep] Risiko duplikat dan agregasi. |
| Population of interest | Populasi yang ingin diprediksi saat model dipakai. | [Konsep] Kesesuaian train, validation, test. |
| Target variable | Label yang dipelajari model. | [Ada] `target` dan target audit. |
| Positive class | Kelas yang dianggap kejadian positif pada biner. | [Ada] `Class mapping`; periksa aturan kompetisi. |
| Class prior / prevalence | Proporsi dasar setiap kelas sebelum melihat fitur. | [Ada] `eda_target.png`. |
| Feature schema | Nama, tipe, dan makna kolom masukan. | [Ada] `train_audit.csv`. |
| Data dictionary | Dokumentasi definisi, unit, dan waktu tersedia tiap fitur. | [Opsional] Buat dari metadata/domain. |
| Semantic type | Peran fitur sebagai nominal, ordinal, kontinu, hitungan, waktu, ID, atau teks. | [Konsep] Pilihan encoding dan validasi. |
| Cardinality | Banyak nilai unik dalam fitur kategorikal. | [Ada] `unique_n` pada audit. |
| Rare category | Level kategori dengan frekuensi sangat kecil. | [Opsional] Hitung frekuensi dan cek stabilitas fold. |
| Sentinel value | Kode seperti `?` atau `N/A` yang berarti data tidak tersedia. | [Ada] `missing_tokens`; pastikan maknanya. |
| Schema drift | Perubahan nama, tipe, atau himpunan kolom antara train dan test. | [Ada] laporan kolom train/test. |
| Distribution drift | Perbedaan distribusi fitur antara train dan test. | [Ada] `eda_numeric_drift.csv`, `eda_categorical_drift.csv`. |
| Support mismatch | Test mengandung wilayah nilai/kategori yang jarang atau tidak ada di train. | [Ada] `unseen_test_fraction`; numerik perlu audit tambahan. |
| Selection bias | Sampel terpilih tidak mewakili populasi tujuan. | [Konsep] Cara pengumpulan dataset. |
| Label noise | Label salah, tidak konsisten, atau ambigu. | [Opsional] Tinjau sampel/duplikat berlabel konflik. |
| Annotation bias | Kesalahan label yang sistematis karena prosedur pelabelan. | [Konsep] Sumber label. |
| Duplicate contamination | Baris sama atau entitas sama muncul pada train dan validation. | [Ada] hitungan duplikat; group CV bila entitas diketahui. |
| Train-test overlap | Entitas atau baris yang muncul di train dan hidden test. | [Opsional] Audit sesuai aturan kompetisi. |
| Post-outcome feature | Fitur yang baru diketahui setelah target terjadi. | [Konsep] Audit manual waktu ketersediaan. |

Kalimat yang aman: “Sebelum memilih model, kami mendefinisikan unit observasi dan mengaudit schema, missingness, serta pergeseran distribusi. Temuan EDA dipakai untuk merancang validasi, bukan untuk menyimpulkan hubungan sebab-akibat.”

## 2. EDA dan hubungan antarvariabel

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| Exploratory data analysis (EDA) | Pemeriksaan pola dan anomali sebelum pemodelan. | [Ada] seluruh `eda_*.png`. |
| Univariate analysis | Analisis satu variabel, misalnya histogram atau frekuensi. | [Ada] `eda_numeric_distributions.png`. |
| Bivariate analysis | Hubungan dua variabel, sering fitur dengan target. | [Ada] `eda_relation_num_*.png`, `eda_relation_cat_*.png`. |
| Multivariate analysis | Pola beberapa variabel sekaligus. | [Ada] korelasi; interaksi lebih lanjut opsional. |
| Target-conditioned distribution | Distribusi fitur setelah dipisah menurut kelas target. | [Ada] boxplot per kelas. |
| Missingness pattern | Struktur nilai hilang per fitur dan kelas. | [Ada] `eda_missing_by_target.png`. |
| Missingness as signal | Ketidakhadiran nilai itu sendiri mungkin prediktif. | [Ada] missing indicator; nilai tambah perlu ablation. |
| Skewness | Ketidaksimetrisan distribusi numerik. | [Ada] inspeksi histogram; angka formal opsional. |
| Heavy tail | Lebih banyak nilai ekstrem dibanding distribusi ringan. | [Ada] inspeksi histogram/kuantil tambahan. |
| Outlier | Observasi jauh dari mayoritas; belum tentu kesalahan. | [Konsep] Validasi domain sebelum clipping. |
| Spearman correlation | Korelasi monotonik berdasarkan peringkat. | [Ada] `eda_correlations.png`. |
| Multicollinearity | Fitur saling berkorelasi sehingga interpretasi koefisien/importance sulit. | [Ada] heatmap; VIF opsional. |
| Spurious correlation | Asosiasi yang timbul dari kebetulan atau artefak pengambilan data. | [Konsep] Bandingkan antar fold/waktu. |
| Confounding | Variabel ketiga memengaruhi hubungan fitur-target. | [Konsep] Butuh desain kausal untuk klaim sebab-akibat. |
| Simpson's paradox | Tren agregat bisa berbalik setelah data dikelompokkan. | [Opsional] Analisis subgrup yang relevan. |
| Kolmogorov–Smirnov statistic | Jarak maksimum antarkurva distribusi empiris numerik. | [Ada] `eda_numeric_drift.csv`; statistik, bukan bukti leakage. |
| Population stability index (PSI) | Ringkasan perubahan proporsi pada bin distribusi. | [Opsional] Perlu aturan bin yang tetap. |
| Mutual information | Ketergantungan statistik nonlinier antara fitur dan target. | [Opsional] Estimasi harus dievaluasi hati-hati. |
| Adversarial validation | Klasifier membedakan baris train vs test untuk menilai shift. | [Opsional] Latih terpisah; AUC tinggi perlu diagnosis. |
| Slice analysis | Evaluasi pada subpopulasi bermakna, misalnya wilayah atau kelompok. | [Opsional] Pastikan ukuran sampel cukup. |

Kalimat yang aman: “Kami melihat missingness per kelas dan drift train/test sebagai sinyal risiko distribusi. KS statistic menunjukkan perbedaan marginal numerik; dampaknya pada generalisasi tetap perlu dibuktikan oleh validasi yang sesuai.”

## 3. Validasi, generalisasi, dan leakage

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| Generalization | Kinerja pada observasi baru dari kondisi yang relevan. | [Konsep] OOF dan private test. |
| Inductive bias | Asumsi bawaan metode tentang pola yang mudah dipelajari. | [Konsep] Trees mencari aturan bertingkat; linear model mencari efek aditif linear. |
| IID assumption | Asumsi baris independen dan berasal dari distribusi serupa. | [Konsep] Kapan stratified CV layak. |
| Stratified K-fold | Fold yang menjaga proporsi kelas kira-kira tetap. | [Ada] `split_type="stratified"`. |
| Group K-fold | Entitas yang sama tidak dibagi ke train dan validation. | [Ada] `split_type="group"`. |
| Temporal validation | Model dilatih pada masa lalu dan diuji pada masa depan. | [Ada] `split_type="time"`. |
| Embargo / gap | Jarak antarperiode train-valid untuk mengurangi informasi berdekatan yang bocor. | [Ada] `time_gap` dalam jumlah baris. |
| Out-of-fold (OOF) prediction | Prediksi baris dari model yang tidak melatih pada baris itu. | [Ada] `oof_predictions.csv`. |
| Holdout set | Data yang ditahan dari seluruh pemilihan model untuk evaluasi final. | [Opsional] Belum dibuat terpisah oleh template. |
| Nested cross-validation | CV luar menilai proses pemilihan model, CV dalam menyetel metode. | [Opsional] Saat tuning sangat intensif. |
| Validation leakage | Informasi validation ikut membentuk fitur atau preprocessing training. | [Ada] Imputer/encoder dilatih per fold. |
| Target leakage | Fitur memuat informasi label yang tidak tersedia saat prediksi. | [Konsep] Butuh audit domain. |
| Temporal leakage | Informasi masa depan masuk ke fitur, agregasi, atau split. | [Konsep] Audit waktu ketersediaan. |
| Entity leakage | Rekam entitas sama masuk kedua sisi split. | [Ada] Group CV jika kolom entitas diberikan. |
| Preprocessing leakage | Imputasi/scaling/encoding dipelajari sebelum split. | [Ada] Transformasi per fold. |
| Resampling leakage | Oversampling diterapkan sebelum split atau pada validation. | [Ada] Sampling hanya training fold. |
| Leaderboard overfitting | Strategi terlalu mengikuti public leaderboard sehingga gagal pada private test. | [Konsep] Batasi keputusan dari leaderboard. |
| Hyperparameter selection bias | Skor terbaik dari banyak percobaan pada validation cenderung optimistis. | [Konsep] Simpan holdout/nested CV. |
| Domain shift | Distribusi atau mekanisme target berubah antarlingkungan. | [Konsep] Train/test drift hanya satu petunjuk. |
| Covariate shift | Distribusi fitur berubah, sedangkan hubungan label bersyarat diasumsikan relatif tetap. | [Konsep] Jangan klaim tanpa menguji asumsi. |
| Label shift | Proporsi kelas berubah, sedangkan distribusi fitur bersyarat kelas diasumsikan tetap. | [Konsep] Perlu estimasi khusus; label hidden test tidak diketahui. |
| Concept drift | Hubungan fitur-target berubah dari waktu ke waktu. | [Konsep] Perlu evaluasi temporal berkala. |
| Train-serving skew | Fitur saat melatih berbeda dari fitur saat inference. | [Konsep] Audit pipeline dan waktu ketersediaan. |
| External validity | Apakah hasil berlaku di luar data dan setup validasi. | [Konsep] Nyatakan batas generalisasi. |
| Variance across folds | Perubahan skor antarfold. | [Ada] `fold_metrics.csv`, heatmap. |
| Confidence interval | Rentang ketidakpastian estimasi skor. | [Opsional] Perlu bootstrap/unit sampling yang benar. |

Kalimat yang aman: “Desain validasi adalah bagian dari model. Bila entitas berulang, stratifikasi acak dapat memberi estimasi terlalu optimistis; karena itu kami memisahkan entitas di tingkat fold dan melaporkan variasi skor antarfold.”

## 4. Representasi fitur dan preprocessing

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| Feature representation | Bentuk numerik/semantik fitur yang dilihat model. | [Konsep] Native category vs one-hot. |
| Feature engineering | Membuat fitur baru dari data yang tersedia saat prediksi. | [Ada] Fitur kalender; fitur domain lain opsional. |
| Native categorical handling | Model memproses kategori tanpa one-hot manual. | [Ada] CatBoost, LightGBM. |
| One-hot encoding | Satu indikator untuk setiap kategori yang dipelajari dari training fold. | [Ada] XGBoost/ExtraTrees/logistic. |
| Unknown-category handling | Cara memperlakukan kategori validation/test yang tidak ada di training. | [Ada] `handle_unknown="ignore"`; LightGBM kategori asing jadi missing. |
| Ordinal encoding | Memberi angka pada kategori berurutan; berbahaya bila nominal diperlakukan ordinal. | [Opsional] Hanya bila urutan bermakna. |
| Target encoding | Mengubah kategori memakai statistik target. | [Opsional] Butuh cross-fitting agar label baris sendiri tidak bocor. |
| Count/frequency encoding | Mengganti kategori dengan banyak/frekuensi kemunculannya. | [Opsional] Statistik dipelajari per fold. |
| Hashing trick | Memetakan kategori ke jumlah kolom tetap dengan kemungkinan collision. | [Opsional] Untuk cardinality tinggi. |
| Embedding | Vektor terlatih yang merepresentasikan kategori atau entitas. | [Opsional] Model neural/foundation. |
| Quantile transform | Mengubah distribusi numerik memakai peringkat. | [Opsional] Sering diuji untuk model neural/linear, bukan wajib untuk tree. |
| Feature scaling | Mengubah skala fitur numerik agar optimisasi model tertentu lebih stabil. | [Ada] Baseline logistic memakai `MaxAbsScaler`. |
| Standardization | Memusatkan nilai pada rata-rata nol dan skala simpangan baku satu. | [Opsional] Tidak dipakai oleh template; fit hanya pada training fold bila ditambahkan. |
| Monotonic transformation | Transformasi yang menjaga urutan, misalnya log pada nilai positif. | [Opsional] Uji efeknya dengan CV. |
| Missing-value imputation | Mengisi nilai kosong dengan aturan yang dipelajari di training fold. | [Ada] Median, mean, constant. |
| Native missing branch | Model memutuskan jalur pemisahan untuk nilai hilang. | [Ada] Mode `native` untuk numerik tree yang mendukung. |
| Missing indicator | Fitur biner yang menandai nilai awalnya hilang. | [Ada] `missing_indicator=True` saat imputasi. |
| All-missing feature | Kolom tanpa nilai teramati pada suatu fold. | [Konsep] Perlu kebijakan yang konsisten. |
| Feature sparsity | Banyak entri nol, umum sesudah one-hot. | [Ada] Encoder dapat menghasilkan matriks sparse. |
| Curse of dimensionality | Representasi berdimensi tinggi membuat kedekatan/estimasi lebih sulit. | [Konsep] Periksa one-hot besar dan metode berbasis jarak. |
| Interaction feature | Fitur yang menangkap gabungan pengaruh dua variabel. | [Opsional] Trees dapat mempelajari interaksi melalui split. |
| Leakage-safe aggregation | Agregasi entitas/waktu dihitung hanya dari informasi yang tersedia pada saat prediksi. | [Opsional] Perlu implementasi khusus dataset. |
| Ablation study | Menambah/menghapus satu komponen untuk mengukur kontribusinya. | [Opsional] Bandingkan CV pada fold yang sama. |

Kalimat yang aman: “Representasi fitur disesuaikan dengan inductive bias model: kategori asli untuk boosted trees yang mendukungnya, dan one-hot yang dipelajari per fold untuk baseline linear dan model yang memerlukannya.”

## 5. Model, kapasitas, dan optimisasi

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| Baseline | Titik pembanding sederhana sebelum eksperimen mahal. | [Ada] ExtraTrees/logistic bila dipilih; prevalence baseline perlu ditambah manual. |
| Gradient-boosted decision trees (GBDT) | Ensemble pohon berurutan yang memperbaiki kesalahan model sebelumnya. | [Ada] CatBoost, LightGBM, XGBoost. |
| Bagging | Melatih model pada variasi sampel dan menggabungkan hasil. | [Konsep] ExtraTrees adalah ensemble pohon; template bukan CV bagging penuh. |
| Randomization | Keacakan fitur/split/sampel untuk mengurangi korelasi model. | [Ada] ExtraTrees dan parameter subsampling tertentu. |
| Histogram-based splitting | Kandidat split dari bin fitur untuk efisiensi training. | [Ada] LightGBM/XGBoost. |
| Ordered boosting | Strategi CatBoost untuk mengurangi bias target-statistics/prediction shift. | [Konsep] Jelaskan hanya bila relevan dengan implementasi dan versi. |
| Leaf-wise growth | Pertumbuhan pohon menurut leaf yang memberi gain terbesar. | [Konsep] Ciri LightGBM; perlu regularisasi agar tidak overfit. |
| Level-wise growth | Pertumbuhan pohon secara lebih seragam per kedalaman. | [Konsep] Bandingkan dengan leaf-wise secara hati-hati. |
| Symmetric tree | Pohon dengan aturan split sama pada seluruh node di level yang sama. | [Konsep] Struktur umum CatBoost. |
| Split gain | Perkiraan perbaikan objective dari suatu pemisahan node. | [Konsep] Internal tree model. |
| Loss function | Besaran yang diminimalkan saat training. | [Ada] Log loss pada boosting; kurva `training_loss_*.png`. |
| Evaluation metric | Ukuran kualitas sesuai tujuan kompetisi. | [Ada] `primary_metric`, `fold_metrics.csv`. |
| Optimization objective | Fungsi total yang dioptimalkan, termasuk regularisasi bila ada. | [Konsep] Bedakan dari metrik leaderboard. |
| Learning rate | Besar kontribusi tiap langkah boosting. | [Ada] `learning_rate`. |
| Number of estimators | Jumlah maksimum pohon/iterasi. | [Ada] `iterations`. |
| Early stopping | Menghentikan boosting saat validation tidak membaik setelah beberapa putaran. | [Ada] `early_stopping_rounds`; validation fold. |
| Best iteration | Putaran yang memberi nilai validasi terbaik. | [Ada] Dipilih internal; belum dicatat sebagai tabel terpisah. |
| Tree depth | Kedalaman aturan bertingkat yang dapat dipelajari. | [Ada] Parameter di generator; tuning opsional. |
| Number of leaves | Kapasitas pohon LightGBM. | [Ada] Parameter `num_leaves`; tuning opsional. |
| Regularization | Pembatas kompleksitas untuk mengurangi overfitting. | [Konsep] Depth, leaf size, subsampling, penalti. |
| Bias–variance tradeoff | Keseimbangan model terlalu sederhana vs terlalu sensitif terhadap sampel. | [Konsep] Baca train/valid loss dan fold variance. |
| Underfitting | Model gagal menangkap sinyal train. | [Konsep] Perlu train score/kurva yang mendukung. |
| Overfitting | Model bagus di train tetapi menurun pada validation. | [Ada] Bandingkan training/validation loss; jangan simpulkan dari satu titik. |
| Capacity | Kerumitan pola yang mampu dipelajari model. | [Konsep] Depth/leaves/features. |
| Sample efficiency | Kinerja yang dicapai dengan jumlah data berlabel tertentu. | [Opsional] Butuh learning curve atau eksperimen subsampling. |
| Tabular foundation model | Model pralatih yang dapat dipakai di banyak tabel baru. | [Opsional] Dibahas di riset; tidak menjadi opsi `models` template. |
| In-context learning | Model menyesuaikan prediksi dari contoh yang diberikan saat inferensi tanpa fit biasa. | [Opsional] Relevan untuk keluarga TabPFN tertentu. |
| Pretraining | Pembelajaran awal pada banyak tugas/data sebelum tugas kompetisi. | [Konsep] Berbeda dari training pada dataset lomba. |
| Transfer learning | Pemanfaatan pengetahuan dari tugas awal ke tugas baru. | [Konsep] Perlu cek kesesuaian domain dan lisensi. |
| Meta-learning | Belajar dari banyak tugas agar cepat beradaptasi pada tugas baru. | [Konsep] Salah satu ide di balik model fondasi tabular. |
| Transformer | Arsitektur neural yang memproses token/fitur dengan mekanisme attention. | [Opsional] Tidak dilatih oleh template. |
| Attention mechanism | Bobot konteks yang dipelajari saat memproses representasi. | [Opsional] Bukan penjelasan kausal otomatis. |
| AutoML | Sistem yang mengotomatisasi pemilihan model, parameter, atau ensemble. | [Opsional] AutoGluon dibahas di riset, tidak dijalankan template. |
| TabPFN | Keluarga model fondasi untuk data tabular, kuat terutama pada setup tertentu. | [Opsional] Cek versi, ukuran data, bobot, dan lisensi sebelum klaim. |
| AutoGluon Tabular | Sistem AutoML/ensemble untuk tabel. | [Opsional] Belum diintegrasikan ke dua notebook. |
| Computational budget | Batas waktu, CPU/GPU, RAM, dan disk eksperimen. | [Ada] `use_gpu`, iterasi, jumlah fold/model. |
| Pareto frontier | Kandidat yang tidak kalah sekaligus pada kualitas dan biaya. | [Opsional] Catat waktu, RAM, dan skor untuk klaim. |

Kalimat yang aman: “Kami membandingkan tiga keluarga GBDT pada fold identik. Early stopping membatasi jumlah pohon menurut validasi per fold; kurva train-valid loss membantu melihat apakah kapasitas model terlalu besar untuk data ini.”

## 6. Imbalance, probabilitas, dan keputusan

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| Class imbalance | Proporsi kelas tidak seimbang. | [Ada] Target audit dan `eda_target.png`. |
| Class weighting | Bobot loss lebih besar untuk kelas tertentu. | [Ada] `imbalance_method="class_weight"`. |
| Random oversampling | Mengulang sampel minoritas pada training fold. | [Ada] `imbalance_method="random_over"`. |
| SMOTE | Membuat sampel sintetis melalui interpolasi tetangga minoritas. | [Ada] Hanya `smote_numeric`, fitur numerik. |
| SMOTENC | Varian SMOTE untuk fitur numerik dan kategorikal. | [Opsional] Tidak diimplementasikan template. |
| Cost-sensitive learning | Optimisasi yang menghukum jenis kesalahan secara berbeda. | [Opsional] Butuh matriks biaya/aturan kompetisi. |
| Decision threshold | Batas probabilitas untuk label positif. | [Ada] `binary_threshold`. |
| Threshold tuning | Mencari batas yang memaksimalkan metrik keputusan. | [Ada] Sweep diagnostik OOF; estimasi final butuh split terpisah. |
| Probability calibration | Kesesuaian probabilitas prediksi dengan frekuensi kejadian. | [Ada] Plot kalibrasi; pemasangan kalibrator belum ada. |
| Reliability diagram | Plot probabilitas prediksi vs frekuensi aktual. | [Ada] `binary_roc_pr_calibration.png`. |
| Discrimination | Kemampuan memberi skor lebih tinggi pada kasus positif daripada negatif. | [Ada] ROC AUC. |
| Ranking quality | Mutu urutan sampel menurut skor prediksi. | [Ada] ROC/PR AUC; bukan kalibrasi. |
| Base-rate effect | Precision dipengaruhi prevalensi kelas positif. | [Konsep] Saat membandingkan PR lintas distribusi. |
| Precision–recall tradeoff | Perubahan precision dan recall ketika threshold digeser. | [Ada] Kurva PR dan sweep threshold. |
| False-positive cost | Kerugian akibat prediksi positif yang salah. | [Konsep] Perlu biaya nyata untuk keputusan. |
| False-negative cost | Kerugian akibat luput mendeteksi positif. | [Konsep] Perlu biaya nyata untuk keputusan. |
| Selective prediction | Hanya memberi keputusan otomatis pada prediksi dengan keyakinan cukup. | [Opsional] Butuh kebijakan abstain dan evaluasi. |

Kalimat yang aman: “Karena prevalensi positif rendah, akurasi tunggal kurang informatif. Kami tampilkan PR AUC, confusion matrix, dan sensitivitas threshold; threshold terbaik pada OOF kami perlakukan sebagai eksplorasi, bukan kenaikan skor validasi yang tak bias.”

## 7. Metrik evaluasi dan artefak

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| Accuracy | Proporsi prediksi label yang benar. | [Ada] `fold_metrics.csv`. |
| Balanced accuracy | Rata-rata recall antarkelas. | [Ada] `fold_metrics.csv`. |
| Precision | Dari prediksi positif, berapa yang benar positif. | [Ada] `classification_report`. |
| Recall / sensitivity | Dari positif sebenarnya, berapa yang terdeteksi. | [Ada] `classification_report`. |
| Specificity | Dari negatif sebenarnya, berapa yang benar negatif. | [Opsional] Turunkan dari confusion matrix. |
| F1 score | Rata-rata harmonik precision dan recall. | [Ada] `f1`, `f1_macro`, `f1_weighted`. |
| Macro averaging | Rata-rata metrik per kelas dengan bobot sama. | [Ada] `f1_macro`. |
| Weighted averaging | Rata-rata metrik per kelas menurut ukuran kelas. | [Ada] `f1_weighted`. |
| Micro averaging | Agregasi keputusan dari seluruh kelas sebelum menghitung metrik. | [Opsional] Belum sebagai kolom terpisah. |
| Matthews correlation coefficient (MCC) | Ringkasan empat sel confusion matrix pada biner. | [Ada] Kolom `mcc` biner. |
| ROC curve | TPR terhadap FPR di seluruh threshold. | [Ada] `binary_roc_pr_calibration.png`; OvR untuk multiclass. |
| ROC AUC | Luas ROC; ukuran diskriminasi berbasis ranking. | [Ada] `roc_auc` biner, `roc_auc_ovr_macro` multiclass. |
| Precision–recall curve | Precision terhadap recall di seluruh threshold. | [Ada] Plot biner/OvR. |
| Average precision (AP) | Ringkasan area PR menurut definisi average precision. | [Ada] `pr_auc` biner memakai `average_precision_score`. |
| One-vs-rest (OvR) | Satu kelas dibanding gabungan kelas lain. | [Ada] ROC/PR multiclass. |
| Log loss / cross-entropy | Penalti probabilitas salah, sangat berat untuk kesalahan percaya diri. | [Ada] `log_loss`, kurva training. |
| Brier score | Rata-rata kuadrat selisih probabilitas positif dan outcome biner. | [Ada] `brier` biner. |
| Confusion matrix | Hitungan prediksi vs label sebenarnya. | [Ada] `confusion_matrix.png`. |
| Row-normalized confusion matrix | Proporsi prediksi per kelas sebenarnya. | [Ada] Panel kedua `confusion_matrix.png`. |
| Per-class support | Jumlah contoh tiap kelas pada evaluasi. | [Ada] `classification_report`. |
| OOF coverage | Berapa baris memiliki prediksi OOF valid. | [Ada] `oof_rows`; split waktu mengecualikan blok awal. |
| Fold stability | Konsistensi metrik dari fold ke fold. | [Ada] `fold_metric_matrix.png`. |
| Calibration error (ECE) | Ringkasan gap probabilitas vs frekuensi empiris per bin. | [Opsional] Plot ada, ECE numerik belum dihitung. |
| Expected utility | Nilai keputusan menurut manfaat/biaya dunia nyata. | [Opsional] Butuh matriks utilitas. |

Kalimat yang aman: “Metrik utama mengikuti aturan kompetisi. Kami tetap melaporkan confusion matrix dan metrik per kelas karena skor agregat yang sama dapat menyembunyikan jenis kesalahan yang berbeda.”

## 8. Ensemble dan eksperimen

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| Model diversity | Model membuat kesalahan yang berbeda sehingga gabungan berpotensi membantu. | [Opsional] Perlu korelasi/error OOF antarmodel. |
| Probability averaging | Rata-rata probabilitas beberapa model. | [Ada] `ensemble=True`. |
| Weighted blend | Rata-rata probabilitas dengan bobot tak sama. | [Opsional] Butuh bobot dari validasi terpisah/nested. |
| Stacking | Meta-model belajar menggabungkan prediksi dasar. | [Opsional] Tidak diimplementasikan; jangan sebut ensemble template stacking. |
| Bagging across folds | Melatih model pada beberapa subset dan merata-ratakan prediksi test. | [Ada] Prediksi test dirata-ratakan antarfold. |
| Seed ensemble | Merata-ratakan fit dari beberapa random seed. | [Opsional] Template memakai seed dasar plus nomor fold. |
| OOF blending | Membandingkan gabungan model memakai prediksi OOF. | [Ada] Baris `ensemble` di `oof_model_comparison.csv`. |
| Error correlation | Seberapa sering dua model salah pada baris yang sama. | [Opsional] Hitung dari OOF per model. |
| Complementarity | Keuntungan gabungan karena model berbeda dalam kesalahan. | [Opsional] Perlu ablation blend dan error analysis. |
| Hyperparameter optimization (HPO) | Pencarian konfigurasi model secara sistematis. | [Opsional] Template memberi parameter awal, bukan HPO otomatis. |
| Search space | Rentang pilihan parameter yang hendak diuji. | [Opsional] Definisikan sebelum tuning. |
| Bayesian optimization | Pemilihan percobaan baru dari model probabilistik performa. | [Opsional] Tidak diimplementasikan. |
| Trial budget | Batas jumlah eksperimen yang boleh dipakai. | [Konsep] Cegah overfitting validation dan boros waktu. |
| Reproducibility | Kemampuan mengulang hasil dengan data, kode, versi, seed, dan setup sama. | [Ada] Seed dan versi dicetak; GPU tertentu bisa nondeterministik. |
| Experiment tracking | Pencatatan konfigurasi, skor, artefak, dan keputusan tiap percobaan. | [Opsional] Simpan CFG bersama output untuk pelacakan penuh. |
| Statistical significance | Apakah selisih teramati cukup kuat terhadap variasi sampling. | [Opsional] Jangan simpulkan dari selisih satu run kecil. |

Kalimat yang aman: “Ensemble di template adalah probability averaging yang sederhana. Kami mempertahankannya hanya jika skor OOF pada fold yang sama membaik; kami tidak menyebutnya stacking karena tidak ada meta-model.”

## 9. Interpretasi dan diagnosis kesalahan

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| Feature importance | Skor kontribusi fitur menurut definisi model tertentu. | [Ada] `feature_importance_*.png`. |
| Gain importance | Jumlah peningkatan objective dari split fitur. | [Opsional] Tergantung metode importance/model. |
| Permutation importance | Penurunan skor setelah satu fitur diacak pada validation. | [Opsional] Tidak dihitung template. |
| SHAP value | Atribusi prediksi pada fitur menurut kerangka Shapley. | [Opsional] Tidak dihitung template. |
| Partial dependence (PDP) | Rata-rata prediksi saat satu fitur divariasikan. | [Opsional] Perlu hati-hati pada fitur berkorelasi. |
| ICE plot | Kurva dampak fitur untuk masing-masing baris. | [Opsional] Perlu inspeksi tambahan. |
| Counterfactual explanation | Perubahan input yang cukup untuk mengubah keputusan model. | [Opsional] Harus memenuhi batas perubahan yang realistis. |
| Error analysis | Meninjau baris dan subgrup yang salah diprediksi. | [Ada] `oof_errors.csv`. |
| High-confidence error | Prediksi salah dengan probabilitas tinggi. | [Ada] `confidence` di `oof_errors.csv`. |
| False-positive analysis | Pola kasus negatif yang diprediksi positif. | [Ada] Filter `oof_errors.csv` biner. |
| False-negative analysis | Pola kasus positif yang terlewat. | [Ada] Filter `oof_errors.csv` biner. |
| Residual pattern | Struktur yang tertinggal pada kesalahan model. | [Opsional] Kelompokkan error menurut fitur/waktu. |
| Shortcut learning | Model memakai proxy mudah yang tidak stabil atau tidak sahih. | [Konsep] Periksa ID, post-outcome field, shift, dan slice. |
| Proxy feature | Fitur yang mewakili konsep lain secara tidak langsung. | [Konsep] Butuh pengetahuan domain untuk menilai risiko. |
| Causal claim | Klaim bahwa perubahan fitur menyebabkan perubahan outcome. | [Konsep] Tidak terbukti dari importance/EDA prediktif. |
| Sensitivity analysis | Menguji apakah kesimpulan bertahan saat asumsi/konfigurasi berubah. | [Opsional] Bandingkan split, fitur, atau imputasi. |

Kalimat yang aman: “Importance model membantu prioritas inspeksi, tetapi bukan bukti sebab-akibat. Kami meninjau prediksi salah berkepercayaan tinggi untuk mencari label bermasalah, fitur bocor, atau subpopulasi yang belum tertangani.”

## 10. Komputasi, submission, dan batas klaim

| Istilah | Makna ringkas | Kaitkan dengan |
| --- | --- | --- |
| GPU acceleration | Menjalankan operasi model tertentu pada GPU. | [Ada] Kolom `gpu` per fold; `use_gpu` tidak menjamin GPU berhasil. |
| CPU fallback | Melatih ulang di CPU bila jalur GPU gagal. | [Ada] Implementasi notebook. |
| Multi-GPU utilization | Pemakaian lebih dari satu GPU secara nyata. | [Opsional] T4 x2 tersedia, tetapi template memakai GPU pertama per fit. |
| VRAM constraint | Batas memori per GPU. | [Konsep] Model tidak otomatis berbagi memori antar-T4. |
| Training latency | Waktu pelatihan satu percobaan. | [Opsional] Template belum mencatat durasi per fit. |
| Inference latency | Waktu untuk menghasilkan prediksi test. | [Opsional] Perlu benchmark tersendiri. |
| Memory footprint | Besar RAM/VRAM yang dipakai model dan fitur. | [Opsional] Audit CSV memberi memori data awal, bukan peak RAM. |
| Carbon/compute efficiency | Hasil per sumber daya komputasi yang dipakai. | [Opsional] Perlu pengukuran biaya/energi. |
| Submission schema | Urutan dan nama kolom yang diminta kompetisi. | [Ada] Pemeriksaan `sample_submission.csv`. |
| Class-order alignment | Kesesuaian indeks `predict_proba` dengan nama kelas output. | [Ada] `Class mapping` dan pemetaan submission. |
| Public/private leaderboard | Skor pada bagian test publik vs tersembunyi. | [Konsep] Keduanya berbeda dari OOF lokal. |
| Refit on full data | Melatih model final pada seluruh train setelah pemilihan metode. | [Opsional] Template menggabungkan prediksi model fold, belum full-data refit. |
| Model card | Ringkasan tujuan, data, metrik, batas, dan risiko model. | [Opsional] Bisa dibuat dari output notebook. |
| Audit trail | Jejak keputusan yang dapat diperiksa ulang. | [Ada] CFG, CSV metrik, audit, OOF; simpan versi notebook. |

Kalimat yang aman: “Notebook dapat berjalan pada lingkungan T4 x2, tetapi satu fit tree memakai satu GPU; kolom `gpu` menunjukkan fold mana yang benar-benar terakselerasi. Submission mengikuti sample template dan urutan kelas yang diaudit.”

## Template narasi singkat untuk juri

1. **Masalah:** “Unit observasinya adalah [isi], targetnya [isi], dan metrik resmi [isi]. Kami mendefinisikan positive class/urutan kelas sebelum membuat submission.”
2. **Validasi:** “Kami memakai [stratified/group/time] CV karena [alasan struktural]. Ini mengurangi risiko [jenis leakage], meskipun [batas yang masih ada].”
3. **Representasi:** “Kategori ditangani secara native pada [model], sedangkan baseline [model] memakai encoding per fold. Statistik missing tidak dipelajari dari validation atau test.”
4. **Model:** “Kami membandingkan [model yang benar-benar dijalankan] pada fold identik. Metrik OOF [angka dari CSV] dan variasi antarfold [angka dari CSV] menjadi dasar keputusan.”
5. **Diagnosis:** “Confusion matrix menunjukkan [kesalahan dominan]. Kurva loss [temuan nyata]; error analysis memprioritaskan [subgrup/baris nyata].”
6. **Submission:** “Kami memakai [label/probabilitas] menurut format kompetisi, memeriksa mapping kelas dan sample submission, lalu menyimpan `submission.csv`.”

## Pertanyaan juri yang sering muncul

| Pertanyaan | Jawaban yang kuat |
| --- | --- |
| “Mengapa model ini?” | “Kami membandingkannya pada split dan metrik yang sama; pilihannya mengikuti skor OOF, variasi fold, dan biaya komputasi, bukan reputasi model saja.” |
| “Mengapa CV Anda dapat dipercaya?” | “Unit observasi, grup, dan urutan waktu menentukan split; preprocessing dan sampling selalu di dalam fold. Risiko tersisa adalah [sebutkan yang nyata].” |
| “Apakah feature importance membuktikan faktor penyebab?” | “Tidak. Importance menjelaskan perilaku prediksi menurut metode tertentu; klaim kausal memerlukan desain lain.” |
| “Apakah threshold ini optimal?” | “Plot OOF menunjukkan sensitivitas threshold. Threshold yang disetel pada OOF yang sama belum mempunyai estimasi final tak bias; kami perlu holdout atau nested CV.” |
| “Apakah dua T4 dipakai?” | “Lingkungannya menyediakan dua T4, tetapi template memakai satu GPU per fit. Saya hanya mengklaim akselerasi pada fold dengan `gpu=True`.” |
| “Bagaimana menghadapi kelas minoritas?” | “Kami ukur prevalensi dan metrik per kelas, lalu membandingkan tanpa koreksi terhadap weights/resampling yang hanya diterapkan di training fold.” |

## Larangan kalimat yang mudah dipatahkan

- “Model kami SOTA karena memakai CatBoost/TabPFN.” **Ganti:** “Model ini kandidat kuat menurut benchmark; pada dataset ini kami menilainya lewat OOF dengan split yang relevan.”
- “Kami menggunakan dua GPU.” **Ganti:** “Notebook dijalankan di T4 x2; fit yang berhasil memakai GPU pertama, sesuai log fold.”
- “Fitur ini menyebabkan target.” **Ganti:** “Fitur ini berkaitan dengan prediksi; mekanisme kausal belum diuji.”
- “Semua missing value sudah teratasi.” **Ganti:** “Kami menguji metode missing tertentu dan menyimpan audit; makna missing tetap bergantung domain.”
- “Skor OOF ini pasti sama dengan private leaderboard.” **Ganti:** “OOF memperkirakan performa pada skema validasi yang dipilih; private test dapat berbeda distribusi.”
- “Ensemble kami stacking.” **Ganti:** “Kami memakai probability averaging antarmodel dan antarfold.”
- “Threshold hasil sweep meningkatkan CV.” **Ganti:** “Sweep menunjukkan potensi tradeoff; evaluasi kenaikan yang tak bias memerlukan data terpisah.”

Saat membuat slide, ambil maksimum 5–8 istilah inti yang benar-benar didukung grafik/CSV. Letakkan angka dan batas klaim di samping istilah tersebut; sisanya gunakan sebagai jawaban cadangan saat tanya jawab.
