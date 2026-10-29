# Progress Pra-Tubes

Topik: pemetaan genangan banjir pasca-Siklon Senyar di Aceh Utara dan Lhokseumawe dari Sentinel-1. proposal lengkap di `proposal-pratubes.md`

| minggu | tanggal | yang dikerjakan | hasil utama |
| --- | --- | --- | --- |
| 1 | 22 Oktober 2026 | proposal topik, notebook preprocessing sampai peta genangan | 27.285 ha genangan baru, OA 0,886 dan kappa 0,711 terhadap Sentinel-2 |
| 2 | 29 Oktober 2026 | uji sensitivitas tiga parameter preprocessing | filter speckle paling berpengaruh (9,0%), ambang selisih dan MMU di bawah 2,2% |

---

## 22 Oktober 2026, Proposal dan Notebook Preprocessing

Notebook `notebook/pratubes-banjir-senyar.ipynb` mengerjakan pencarian scene, konversi dB, perbandingan filter speckle, Otsu, change detection, masking, morfologi, penggabungan dua orbit, dan validasi dengan MNDWI Sentinel-2. semua data dibaca dari Planetary Computer tanpa akun GEE

Hasilnya 27.285 ha genangan baru pada 27 sampai 28 November 2025, 85% di lahan pertanian. terhadap Sentinel-2 29 November: OA 0,886, kappa 0,711, presisi 0,905, recall 0,697

## 29 Oktober 2026, Uji Sensitivitas Parameter

Notebook `notebook/sensitivitas-parameter.ipynb` menjalankan ulang pipeline dengan 27 kombinasi: ambang selisih (-2, -3, -4 dB), MMU (5, 10, 20 piksel), dan filter (Lee 5x5, Lee 7x7, median 5x5). data dibaca dari cache, jadi tidak ada unduhan baru

| parameter diubah | rentang luas | perubahan dari dasar |
| --- | --- | --- |
| ambang selisih -2 sampai -4 dB | 26.888 sampai 27.467 ha | 2,1% |
| MMU 5 sampai 20 piksel | 26.955 sampai 27.439 ha | 1,8% |
| filter Lee 5x5, Lee 7x7, median 5x5 | 27.285 sampai 29.748 ha | 9,0% |

![sensitivitas](../gambar/07-sensitivitas-parameter.png)

Ambang selisih dan MMU hampir tidak menggeser hasil, jadi nilai di notebook utama aman dipertahankan. filter yang paling menentukan. median 5x5 memberi luas sekitar 9% lebih besar dengan presisi terhadap Sentinel-2 yang sama (0,911 dan 0,913) dan recall lebih tinggi (0,635 dan 0,589), jadi alasan memilih Lee 7x7 di notebook utama perlu ditinjau ulang. notebook utama belum diubah karena referensi MNDWI memakai band SWIR 20 m yang juga tidak bisa melihat pematang sempit

Rencana berikutnya: durasi genangan dari scene 3, 9, dan 10 Desember 2025, lalu luas genangan per kecamatan
