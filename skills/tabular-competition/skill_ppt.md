# Skill: menyiapkan konten presentasi kompetisi tabular per slide

Gunakan panduan ini ketika user meminta **naskah isi slide yang siap dipindahkan ke PowerPoint** untuk proyek klasifikasi tabular. Hasil yang diminta adalah konten terurut per halaman beserta rancangan visual dan catatan presenter. Jangan membuat file `.pptx` kecuali user memintanya. Baca [skill_larp.md](skill_larp.md) hanya untuk memilih istilah yang relevan; bukti tetap berasal dari dataset, notebook, artefak, dan aturan kompetisi yang benar-benar tersedia.

## Masukan dan batas bukti

Sebelum menulis, identifikasi nama kompetisi/dataset, tujuan prediksi, unit observasi, jenis klasifikasi, target dan positive class/urutan kelas, metrik resmi, durasi presentasi, audiens, hasil notebook, serta file gambar/CSV yang tersedia. Baca `CFG`, `train_audit.csv`, `oof_model_comparison.csv`, `fold_metrics.csv`, grafik EDA/evaluasi, dan `submission.csv` bila ada. Bila hanya ada link atau file dataset, lakukan EDA terlebih dahulu memakai [skill_eda.md](skill_eda.md); tulis rancangan slide hasil sebagai **rencana**, bukan hasil yang sudah diperoleh.

Aturan sumber:

- **Angka, pemenang model, peringkat, dan klaim peningkatan** harus diturunkan dari hasil aktual. Cantumkan sumber tepat: nama file, fold, metrik, versi eksperimen, dan tanggal bila relevan. Jangan menciptakan skor contoh di dalam deck final.
- Jika visual belum dihasilkan, sebut **visual yang perlu dibuat**, data/kolom yang dibutuhkan, dan placeholder `[BELUM TERSEDIA]`. Jangan menggambarkan grafik seolah sudah ada.
- Bedakan hasil OOF, public leaderboard, private leaderboard, train score, dan test prediction. Jangan mengubah satu menjadi yang lain.
- Hindari klaim kausal dari korelasi/feature importance. Bila ada banyak iterasi eksperimen, nyatakan bahwa pemilihan pada OOF yang sama dapat membuat skor optimistis.
- Jika aturan kompetisi tidak diketahui, jangan menebak metrik atau skema submission. Tandai `[PERLU CEK ATURAN KOMPETISI]`.
- Gunakan istilah teknis secukupnya. Untuk istilah pada [skill_larp.md](skill_larp.md), hanya klaim yang bertanda `[Ada]` dan punya artefak aktual yang boleh ditulis sebagai pekerjaan yang sudah dilakukan.

## Bentuk keluaran wajib

Awali dengan **ringkasan deck**: audiens, durasi, jumlah slide inti, pesan utama satu kalimat, sumber data/eksperimen, dan daftar fakta yang masih perlu dikonfirmasi. Lanjutkan slide **bernomor tanpa lompatan**. Tiap slide harus memiliki semua field berikut, agar dapat langsung dipindah ke PPT:

```markdown
## Slide 01 — [Judul berupa kesimpulan atau fungsi halaman]

- **Tujuan:** Mengapa halaman ini ada dalam alur cerita.
- **Headline di slide:** Satu kalimat singkat yang menyampaikan takeaway, bukan sekadar nama topik.
- **Teks di slide:** Salinan final untuk judul, subjudul, label, dan maksimal 2–4 poin pendek; gunakan `[ISI ANGKA]` hanya bila nilai belum tersedia.
- **Visual utama:** Jenis (grafik/tabel/diagram/foto), apa yang ditampilkan, sumbu, satuan, kelas/warna, highlight/anotasi, dan ukuran relatif.
- **Sumber visual/data:** Path artefak yang ada atau spesifikasi pembuatan jika belum ada; cantumkan populasi dan metrik (misalnya OOF n=...).
- **Tata letak:** Posisi teks dan visual, urutan baca, serta elemen yang dijadikan fokus.
- **Catatan presenter:** 2–5 kalimat yang menjelaskan alasan, interpretasi, dan satu batas klaim; jangan menyalin teks slide mentah.
- **Transisi:** Satu kalimat yang mengantar slide berikutnya.
```

Untuk setiap visual, jelaskan **apa yang harus dilihat audiens**. Contoh: “Sorot recall kelas minoritas pada baris kedua confusion matrix; tampilkan jumlah kasus dan persentasenya.” Menulis “masukkan confusion matrix” saja belum cukup. Jika grafik gabungan terlalu padat, pisahkan menjadi dua slide dan perbarui nomor berurutan.

Tutup dokumen dengan (1) tabel inventaris visual berisi slide, nama file, status tersedia/perlu dibuat, dan tindakan yang diperlukan; (2) daftar angka yang belum terverifikasi; (3) dua sampai lima pertanyaan juri potensial beserta jawaban berbasis bukti. Tidak perlu membuat PPT pada tahap ini.

## Standar penyajian profesional

- Gunakan rasio **16:9** sebagai asumsi bila user tidak memberi template. Satu slide = satu pesan utama. Judul berbentuk takeaway, misalnya “Group CV menurunkan estimasi yang terlalu optimistis”, bukan hanya “Validation”.
- Teks slide ringkas dan bisa dibaca dari jauh: hindari paragraf, tabel penuh output CSV, screenshot kode, dan grafik dengan label kecil. Detail metodologi ditempatkan di catatan presenter atau appendix.
- Pastikan label sumbu, satuan, jumlah sampel, nama kelas, nama metrik, dan periode/fold tercantum. Jangan memotong sumbu batang sehingga perbedaan kecil tampak besar; bila skala log dipakai, beri label eksplisit.
- Gunakan warna kelas dan model secara konsisten. Jangan mengandalkan merah/hijau saja untuk membedakan kategori. Sorot satu angka atau pola yang mendukung headline; tampilkan baseline atau pembanding bila mengklaim perbaikan.
- Tulis sumber ringkas di footer slide berbasis data, misalnya `Sumber: OOF 5-fold, oof_model_comparison.csv`; simpan detail path/versi di catatan presenter atau appendix.
- Di setiap grafik performa, tulis **basis evaluasi**: OOF atau fold tertentu, jumlah baris valid, primary metric, dan arah metrik (lebih tinggi/lebih rendah lebih baik). Pada split waktu, nyatakan bahwa blok awal tanpa OOF tidak masuk evaluasi.
- Pakai istilah yang dapat dijelaskan dalam satu kalimat. Jika menyebut *inductive bias*, *feature representation*, atau *calibration*, hubungkan langsung ke keputusan dan bukti, bukan sebagai hiasan.
- Jangan memaksakan jumlah slide. Untuk sekitar 5 menit pilih 7–9 slide inti; 10 menit sekitar 11–13; 15 menit sekitar 14–16. Master sequence di bawah adalah katalog terurut. Gabungkan slide berprioritas rendah, pindahkan detail ke appendix, atau pecah grafik yang terlalu padat.

## Master sequence per halaman

Urutan berikut mempertahankan alur **masalah → data → risiko → metode → hasil → keputusan**. Nomor akhir harus dihitung ulang setelah penyesuaian. “Wajib” berarti konsepnya perlu muncul; boleh digabung dengan slide tetangga bila durasi pendek. Jangan memasukkan halaman dengan hasil kosong.

### Halaman 1 — Sampul dan janji presentasi (wajib)

- **Isi:** nama proyek/kompetisi, tujuan satu baris, nama tim/presenter, tanggal atau versi eksperimen. Subjudul dapat menyebut metrik utama bila sudah dikonfirmasi.
- **Visual:** elemen sederhana yang relevan dengan domain, atau diagram mini “data → validasi → prediksi”; jangan memakai grafik hasil tanpa konteks.
- **Tata letak:** judul paling dominan; identitas kecil di bawah; ruang kosong cukup. Hindari foto generik yang tidak membantu pemahaman.
- **Catatan presenter:** buka dengan keputusan yang akan dibuktikan, bukan klaim “kami memakai model terbaik”.

### Halaman 2 — Executive summary: satu temuan dan satu keputusan (wajib)

- **Isi:** masalah, pendekatan, hasil OOF utama, model/ensemble terpilih, dan satu batas yang paling penting. Gunakan maksimal tiga blok “Tantangan / Bukti / Keputusan”.
- **Visual:** angka utama berlabel jelas, misalnya “OOF ROC AUC = [nilai]”; bila belum ada hasil, gunakan alur eksperimen, bukan kartu skor kosong.
- **Sumber:** `oof_model_comparison.csv` dan aturan metrik. Jangan menampilkan angka leaderboard sebagai OOF.
- **Catatan presenter:** nyatakan bahwa detail split dan hasil per kelas akan ditunjukkan berikutnya.

### Halaman 3 — Masalah, unit prediksi, metrik, dan keberhasilan (wajib)

- **Isi:** “Memprediksi [target] untuk [unit observasi] dengan informasi yang tersedia pada [waktu].” Tulis kelas, positive class jika biner, metrik resmi, dan format submission.
- **Visual:** diagram input → model → output; untuk multiclass, tampilkan contoh vektor probabilitas berlabel kelas **tanpa nilai rekaan** (pakai simbol p(A), p(B), ...).
- **Sumber:** aturan kompetisi, `CFG`, sample submission.
- **Catatan presenter:** jelaskan mengapa metrik itu sesuai tujuan; bila metrik belum dikonfirmasi tandai jelas.

### Halaman 4 — Peta dataset dan kualitas awal (wajib)

- **Isi:** jumlah baris train/test, fitur numerik/kategorikal, target, ID, time/group key, proporsi missing tertinggi, dan jumlah duplikat hanya jika sudah dihitung. Satu takeaway, misalnya “kategori dan missingness memengaruhi pilihan representasi”.
- **Visual:** kartu ringkas schema dan **satu** bar chart missingness top 10; bila tidak ada missing, ganti diagram tipe fitur. Jangan menaruh dump `train.head()` sebagai visual utama.
- **Sumber:** `train_audit.csv`, `test_audit.csv`, `eda_missing.png`; angka duplikat dari log notebook.
- **Catatan presenter:** bedakan masalah kualitas yang benar-benar ada dari hipotesis.

### Halaman 5 — Distribusi target dan konsekuensi metrik (wajib)

- **Isi:** jumlah dan persentase per kelas, rasio minoritas/mayoritas bila penting, serta keputusan metrik pendamping (misalnya PR AUC atau macro F1). Jangan otomatis menyatakan imbalance “parah” tanpa angka.
- **Visual:** grafik batang dengan label jumlah **dan** persen berdasarkan seluruh baris train. `eda_target.png` bawaan memakai sampel EDA; buat ulang dari `train[target].value_counts()` untuk klaim prevalensi dataset penuh, atau tandai eksplisit bahwa grafik hanya sampel.
- **Catatan presenter:** terangkan prevalensi sebagai baseline alami. Biner: sebut positive class. Multiclass: sorot kelas ber-support kecil.

### Halaman 6 — Hubungan fitur–target yang paling informatif (wajib jika EDA tersedia)

- **Isi:** pilih 1–2 temuan yang dapat diuji dan relevan; jelaskan ukuran sampel, arah hubungan, serta potensi confounding/leakage. Jangan menjadikan peta korelasi besar sebagai slide hanya karena tersedia.
- **Visual:** satu boxplot numerik per kelas atau stacked bar kategori-target; beri anotasi pada pola yang benar-benar tampak. Bila perlu bandingkan dua panel yang punya satu pesan sama.
- **Sumber:** `eda_relation_num_*.png`, `eda_relation_cat_*.png`, `eda_correlations.png` sebagai bahan pendukung, bukan bukti kausal.
- **Catatan presenter:** sebut “berasosiasi” atau “membedakan kelas pada sampel”, bukan “menyebabkan”.

### Halaman 7 — Risiko dataset dan strategi validasi (wajib)

- **Isi:** risiko utama: entitas berulang, waktu, missingness, distribusi test, atau post-outcome feature. Lalu jelaskan split yang dipilih: stratified, group, atau time, alasan, jumlah fold, dan gap bila ada.
- **Visual:** diagram fold sederhana; untuk group tampilkan kelompok tidak menyeberang fold, untuk time tampilkan garis waktu train → gap → valid. Tambahkan satu plot drift/missingness hanya bila langsung menguatkan keputusan.
- **Sumber:** `CFG`, `fold_metrics.csv` untuk jumlah fold; `eda_train_test_drift.png`, `eda_missing_by_target.png` bila relevan.
- **Catatan presenter:** jelaskan jenis leakage yang dicegah dan jenis yang masih memerlukan audit domain. Jangan klaim “bebas leakage” absolut.

### Halaman 8 — Pipeline preprocessing dan feature representation (wajib)

- **Isi:** urutan “clean deterministik → split → fit imputer/encoder/sampler pada train fold → validasi → OOF”. Tulis metode missing, kategori, imbalance yang benar-benar diaktifkan. Jelaskan mengapa CatBoost/LightGBM native category atau one-hot dipakai sesuai model.
- **Visual:** flowchart kiri-ke-kanan dengan garis pemisah train vs validation; beri tanda tebal bahwa validation hanya melewati transformasi `transform`, bukan `fit`. Bila satu metode tidak diaktifkan, hapus bloknya.
- **Sumber:** `CFG` dan sel preprocessing notebook. **Jangan** menulis SMOTE jika `imbalance_class=False` atau metode lain dipilih.
- **Catatan presenter:** gunakan satu istilah dari glosarium—misalnya *feature representation*—lalu terjemahkan ke pilihan konkret.

### Halaman 9 — Kandidat model dan rancangan eksperimen (wajib)

- **Isi:** model yang benar-benar dijalankan, baseline pembanding, primary metric, seed/fold sama, dan anggaran training/early stopping. Jika hanya satu model, jangan menulis “benchmark lintas model”.
- **Visual:** matriks kompak “Model × alasan diuji × kategori/missing × komputasi”. Hindari daftar hyperparameter penuh; hanya parameter yang menentukan kapasitas atau fairness perbandingan.
- **Sumber:** `CFG`, `fold_metrics.csv`, log versi dan kolom `gpu`.
- **Catatan presenter:** jelaskan bahwa benchmark publik memberi kandidat, sedangkan OOF dataset ini menentukan pilihan.

### Halaman 10 — Hasil utama OOF dan konsistensi fold (wajib)

- **Isi:** tabel model, primary metric OOF, metrik pendamping, cakupan OOF, dan keputusan model. Untuk log loss gunakan arah **lebih rendah lebih baik**; metrik lain sesuai definisinya. Jangan menyebut selisih kecil “signifikan” tanpa analisis ketidakpastian.
- **Visual:** bar/dot plot skor model dengan baseline, plus heatmap kecil fold metric jika masih terbaca. Bila banyak model, tampilkan 3–5 yang relevan dan pindahkan sisanya ke appendix.
- **Sumber:** `oof_model_comparison.csv`, `fold_metric_matrix.png`, `fold_metrics.csv`.
- **Catatan presenter:** bedakan skor OOF agregat dari rata-rata fold; tunjukkan variasi, bukan hanya skor terbaik.

### Halaman 11 — Dinamika training dan diagnosis overfitting (wajib jika boosting dijalankan)

- **Isi:** satu temuan dari kurva train vs validation: apakah gap membesar, apakah early stopping aktif, atau apakah loss stabil. Bila kurva tidak tersedia, gunakan tabel ringkas fold/best iteration yang benar-benar dicatat, atau pindahkan halaman ini ke appendix.
- **Visual:** satu kurva loss yang representatif dengan label fold/model, garis atau anotasi titik terbaik bila dapat dihitung dari data. Jangan gabungkan kurva puluhan fold di satu sumbu.
- **Sumber:** `training_loss_<model>_fold<n>.png`; periksa file aktual dan skala loss.
- **Catatan presenter:** kurva satu fold bukan bukti universal; cocokkan dengan variasi skor antarfold.

### Halaman 12 — Jenis kesalahan yang masih terjadi (wajib)

- **Isi:** kesalahan dominan, kelas yang paling sulit, dan satu implikasi praktis. Untuk biner sebut false positive/false negative dan threshold yang dipakai. Untuk multiclass sebut pasangan kelas yang paling sering tertukar.
- **Visual:** `confusion_matrix.png`; potong atau buat ulang sebagai satu panel sesuai pesan, tetapi selalu tampilkan count dan/atau persentase dengan penyebut jelas. Bisa tambah 2 contoh error anonim bila aturan data mengizinkan.
- **Sumber:** `confusion_matrix.png`, `oof_errors.csv`, `classification_report` notebook.
- **Catatan presenter:** jangan menafsirkan biaya FP/FN tanpa informasi domain.

### Halaman 13A — Diagnostik probabilitas biner (pilih untuk binary)

- **Isi:** ROC AUC/average precision, perbandingan dengan prevalensi, kalibrasi secara deskriptif, dan threshold tetap yang dipakai laporan. Jika kompetisi menilai probabilitas, prioritaskan log loss/Brier dan reliability; jika menilai label, prioritaskan precision–recall/threshold.
- **Visual:** pilih paling banyak dua panel dari `binary_roc_pr_calibration.png`, ditambah `binary_threshold_sensitivity.png` hanya jika keputusan threshold relevan. Labeli OOF dan kelas positif.
- **Catatan presenter:** plot kalibrasi bukan bukti kalibrator telah dilatih. Sweep threshold pada OOF bersifat diagnostik.

### Halaman 13B — Diagnostik per kelas multikelas (pilih untuk multiclass)

- **Isi:** kelas dengan recall/precision terendah, support-nya, dan apakah confidence model menurun pada kasus sulit. ROC/PR OvR dipakai sebagai pelengkap, bukan menggantikan metrik resmi.
- **Visual:** pilih plot OvR untuk 2–4 kelas yang paling relevan dari `multiclass_ovr_roc_pr.png`, atau buat grafik batang per-class F1 dari `classification_report`. Jika kelas banyak, jangan memaksakan seluruh legenda.
- **Sumber:** `multiclass_ovr_roc_pr.png`, `multiclass_confidence.png`, classification report.
- **Catatan presenter:** sebut setiap OvR membandingkan satu kelas melawan kelas lain yang digabung.

### Halaman 14 — Interpretasi fitur dan pemeriksaan kewajaran (wajib jika importance tersedia)

- **Isi:** 5–10 fitur tertinggi menurut model terpilih, apakah urutannya stabil antarfold, dan satu risiko proxy/leakage yang perlu ditinjau. Jangan mengklaim importance sebagai efek kausal.
- **Visual:** bar horizontal dari `feature_importance_<model>.png` atau rangkum `feature_importance_folds.csv`; beri unit/definisi fitur yang tidak jelas. Untuk model tanpa importance tersedia, ganti slide dengan error analysis yang lebih rinci.
- **Catatan presenter:** CatBoost dan LightGBM memakai definisi importance yang dapat berbeda; jangan bandingkan angka mentah antarjenis model tanpa normalisasi/metode sebanding.

### Halaman 15 — Ensemble, keputusan final, dan submission (wajib bila hasil final ada)

- **Isi:** bandingkan single best dan ensemble pada primary metric **hanya jika keduanya diuji**. Nyatakan pilihan final, jenis output (probabilitas/label), class-order alignment, dan status file submission.
- **Visual:** tabel kecil dua baris “single vs ensemble” serta diagram `predict_proba` → pemetaan kolom sample submission → `submission.csv`; tidak perlu screenshot CSV panjang.
- **Sumber:** `oof_model_comparison.csv`, `submission.csv`, sample submission, `CFG["submission_mode"]`.
- **Catatan presenter:** ensemble template adalah rata-rata probabilitas, bukan stacking; prediksi test dirata-ratakan antarfold. Jika tidak ada test, ubah judul menjadi “Keputusan model dan rencana submission”.

### Halaman 16 — Kesimpulan, batas, dan langkah berikutnya (wajib)

- **Isi:** jawab tujuan awal dalam satu kalimat, sebut hasil OOF dan keputusan final, lalu 2–3 batas nyata: representativitas split, shift, ketidakpastian, tuning pada OOF, atau akses GPU. Langkah berikutnya harus terukur, misalnya holdout temporal, ablation missing indicator, atau pemeriksaan high-confidence errors.
- **Visual:** tiga blok “Terbukti / Belum teruji / Langkah berikutnya”, bukan grafik baru. Jika ada leaderboard resmi, letakkan di sini dengan label publik/private dan tanggal, bukan menggantikan OOF.
- **Catatan presenter:** tutup dengan kalimat yang mudah diingat, lalu siap untuk Q&A.

## Appendix yang dipilih sesuai kebutuhan

Pindahkan detail yang terlalu teknis ke belakang, tetap bernomor setelah slide inti: tabel semua fold/model, distribusi dan korelasi tambahan, audit missing lengkap, parameter model, analisis drift per fitur, ablation preprocessing/imbalance, kasus salah prediksi anonim, metrik lengkap per kelas, versi paket/seed/komputasi, serta sumber dan aturan kompetisi. Buat appendix hanya bila ada data yang mendukung atau pertanyaan juri yang masuk akal.

## Peta artefak notebook → bahan slide

| Artefak | Slide yang mungkin | Pemeriksaan sebelum dipakai |
| --- | --- | --- |
| `train_audit.csv`, `test_audit.csv` | 4 | Pastikan hitungan dan tipe berasal dari versi data yang sama dengan training. |
| `eda_target.png` | 5 | Grafik bawaan berasal dari sampel EDA; buat ulang dari seluruh train untuk prevalensi penuh atau beri label sampel. |
| `eda_missing.png`, `eda_missing_by_target.png` | 4 atau 7 | Jangan menyebut missingness penyebab target. |
| `eda_relation_num_*.png`, `eda_relation_cat_*.png` | 6 | Pilih maksimal dua pola, cek jumlah sampel dan kategori langka. |
| `eda_numeric_drift.csv`, `eda_categorical_drift.csv`, `eda_train_test_drift.png` | 7 | Drift marginal tidak otomatis berarti performa turun. |
| `fold_metrics.csv`, `fold_metric_matrix.png` | 7 dan 10 | Labeli fold dan arah metrik. |
| `oof_model_comparison.csv` | 2, 10, 15, 16 | Bandingkan OOF pada baris valid yang sama; jangan campur metrik. |
| `training_loss_*.png` | 11 | Sebut model dan fold; pilih kurva yang representatif. |
| `confusion_matrix.png`, `oof_errors.csv` | 12 | Periksa urutan kelas dan denominator normalisasi. |
| `binary_roc_pr_calibration.png`, `binary_threshold_sensitivity.png` | 13A | Nyatakan positive class dan threshold. |
| `multiclass_ovr_roc_pr.png`, `multiclass_confidence.png` | 13B | Pilih kelas, jangan penuhi slide dengan semua kurva. |
| `feature_importance_*.png`, `feature_importance_folds.csv` | 14 | Tuliskan bahwa importance bersifat model-specific. |
| `submission.csv` dan sample submission | 15 | Verifikasi nama, jumlah, urutan kelas, dan jenis output. |

## Pemeriksaan akhir sebelum menyerahkan naskah slide

1. Setiap slide memiliki satu headline yang dapat diuji dan satu visual yang benar-benar menjawab headline itu.
2. Semua angka dan grafik dapat ditelusuri ke artefak, aturan kompetisi, atau ditandai belum tersedia.
3. Urutan slide membentuk cerita; tidak ada slide metode sebelum masalah/validasi diperkenalkan, dan tidak ada kesimpulan tanpa hasil pendukung.
4. Jumlah slide sesuai durasi; grafik dapat dibaca; warna, kelas, metrik, satuan, dan format angka konsisten.
5. Catatan presenter mengandung interpretasi dan batas klaim, bukan sekadar membacakan slide.
6. Binary memakai 13A; multiclass memakai 13B; slide lain yang tidak relevan dihapus atau digabung, lalu nomor diperbarui.
