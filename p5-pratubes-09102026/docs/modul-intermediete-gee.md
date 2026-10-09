# MODUL PRAKTIKUM MATA KULIAH

# PENGOLAHAN CITRA DIGITAL

# INTERMEDIATE GOOGLE EARTH ENGINE: CLUSTERING, URBAN SPRAWL, DAN FLOOD RISK MODELLING

Logo Politeknik Negeri Bandung

**JURUSAN TEKNIK KOMPUTER DAN INFORMATIKA**

**POLITEKNIK NEGERI BANDUNG**

**2026**

# LEMBAR PERSETUJUAN

**INTERMEDIATE GOOGLE EARTH ENGINE: CLUSTERING, URBAN SPRAWL, DAN FLOOD RISK MODELLING**

| Proses | Jabatan | Nama | Tanda Tangan |
| --- | --- | --- | --- |
| Disusun oleh | Pengampu Praktikum Pengolahan Citra Digital |  |  |
| Diperiksa oleh | Ketua Kelompok Bidang Keahlian (KBK) Multimedia |  |  |
| Disahkan oleh | Ketua Program Sarjana Terapan Teknik Informatika |  |  |

**PUBLISHED BY**

Jurusan Teknik Komputer & Informatika Politeknik Negeri Bandung

Jl. Gegerkalong Hilir, Desa Ciwaruga, Kecamatan Parongpong, Kabupaten Bandung Barat, Jawa Barat 40559

Copyright © 2026 by JTK POLBAN

All rights reserved. No part of the contents of this book may be reproduced or transmitted in any form or by any means without the written permission of the publisher.

|  |  |
| --- | --- |
| Penanggung jawab | : Trisna Gelar |
| Penanggung jawab | : Muhammad Rizqi Sholahuddin |
| Tim Penulis | : Tim Praktikum Pemrograman Geospasial Berbasis Cloud |
| Materi rujukan | : E-book “Intermediate GEE” (Geosoftware.ID, 2025) |

# KATA PENGANTAR

Puji syukur ke hadirat Tuhan Yang Maha Esa, karena berkat karunia dan rida-Nya “INTERMEDIATE GOOGLE EARTH ENGINE: CLUSTERING, URBAN SPRAWL, DAN FLOOD RISK MODELLING” telah selesai disusun.

Penyusunan modul ini bertujuan untuk memberikan petunjuk dan prosedur operasional baku (POB) mengenai proses kegiatan praktikum, mulai dari tahap persiapan, pelaksanaan, pelaporan, dan evaluasi untuk penilaian. Melalui modul ini diharapkan proses praktikum dapat mudah dipahami, baik oleh mahasiswa dan dosen di lingkungan Jurusan Teknik Komputer dan Informatika Politeknik Negeri Bandung.

Dua fenomena kembar kota-kota Asia Tenggara – urbanisasi yang memuai dan banjir yang makin sering – sesungguhnya dapat dibaca dari lintasan satelit yang merekam bumi setiap minggu sejak 1980-an. Masalahnya bukan pada kekurangan data, melainkan pada tangan: memproses puluhan tahun citra Landsat secara konvensional membutuhkan infrastruktur yang mahal. Google Earth Engine (GEE) memindahkan seluruh petabyte arsip tersebut ke cloud computing (komputasi awan) sehingga analisis multi-dekade tinggal ditulis sebagai beberapa lusin baris JavaScript. Modul ini diadaptasi dan dikembangkan dari e-book *Intermediate GEE* (Geosoftware.ID, 2025) menjadi tiga studi kasus bertingkat: (1) analisis tutupan lahan tanpa data latih melalui clustering (Task I), (2) pemetaan ekspansi perkotaan Jabodetabekpunjur tahun 1990–2020 secara multitemporal (Task II–III), dan (3) pemodelan risiko banjir berbasis harkat multikriteria yang menggabungkan kerawanan (hazard), eksposur (exposure), dan kerentanan (vulnerability) (Task IV–V). Setiap potongan kode disertai cara membaca kode dalam bahasa awam, keluaran yang diharapkan, serta Lesson Learnt agar praktikan seperti didampingi instruktur selangkah demi selangkah.

Semoga modul ini bermanfaat untuk memperkuat pelaksanaan pengajaran di Jurusan Teknik Komputer & Informatika Politeknik Negeri Bandung, sehingga transparansi dan akuntabilitas kinerja bidang akademik dapat tercapai.

Bandung, 2026

Tim Praktikum Pemrograman Geospasial Berbasis Cloud

# DAFTAR ISI

| Judul | Halaman |
| --- | --- |
| LEMBAR PERSETUJUAN | i |
| KATA PENGANTAR | iii |
| DAFTAR ISI | iv |
| DAFTAR GAMBAR | v |
| DAFTAR TABEL | vi |
| IDENTITAS MATA KULIAH, PROGRAM STUDI DAN KURIKULUM | vii |
| CAPAIAN PEMBELAJARAN | viii |
| BAGIAN I. BAHAN KAJIAN | 1 |
| I.1. Penggunaan Pedoman | 1 |
| I.2. Ruang Lingkup | 1 |
| I.3. Teknologi | 2 |
| I.4. Studi Kasus | 2 |
| I.5. Konsep yang Digunakan | 3 |
| BAGIAN II. PENYIAPAN PELAKSANAAN PRAKTIKUM (PREPARATION) | 5 |
| II.1. Peralatan Praktikum | 5 |
| II.2. Keamanan & Keselamatan Kerja | 6 |
| BAGIAN III. PROSEDUR PELAKSANAAN PRAKTIKUM (STEP BY STEP) | 8 |
| III.1. Teori Singkat: Arsitektur Google Earth Engine dan Kerangka Analisis | 8 |
| III.2. Environment & Setup Praktikum | 11 |
| III.3. Task I: Filter Citra dan Clustering Tutupan Lahan | 12 |
| III.4. Task II: Komposit Median, Indeks Spektral, dan Pemetaan Lahan Terbangun | 15 |
| III.5. Task III: Iterasi Multitemporal dan Peta Urban Sprawl | 18 |
| III.6. Task IV: Pemodelan Kerawanan Banjir (Hazard) | 22 |
| III.7. Task V: Eksposur, Kerentanan, dan Risiko Banjir | 26 |
| III.8. Kesimpulan Praktikum | 30 |
| III.9. Tugas Praktikum (Mandiri) | 31 |
| III.10. Soal Latihan HOTS: Eksperimen dan Desain Analisis GEE (Kumulatif) | 32 |
| BAGIAN IV. MEDIA DAN MEKANISME PENGUMPULAN | 34 |
| BAGIAN V. PEMBAHASAN DAN EVALUASI HASIL PRAKTIKUM | 35 |
| DAFTAR PUSTAKA | 36 |
| LAMPIRAN | 37 |

# DAFTAR GAMBAR

**Catatan:** Seluruh 20 gambar pada modul ini sengaja tidak disertakan dan **wajib dilengkapi mahasiswa** dari hasil praktikum masing-masing di Earth Engine Code Editor. Instruksi pengambilan setiap gambar tercantum pada blok \[GAMBAR n] di task yang bersangkutan; berkas disimpan dengan nama baku pada folder gambar/ agar laporan mudah diperiksa.

Gambar 1. Hasil Akhir Clustering Tutupan Lahan Terbangun (Purwodadi)

Gambar 2. Tampilan Citra Komposit RGB (SWIR-NIR-Biru) di Code Editor

Gambar 3. Tampilan NDBI (Kiri) dan NDWI (Kanan) Jabodetabekpunjur

Gambar 4. Lahan Terbangun (Merah) dan Air (Biru) Hasil Thresholding

Gambar 5. Citra Landsat Tahun 1990 (Kiri) dan 2020 (Kanan)

Gambar 6. Lahan Terbangun Tahun 1990 (Kiri) dan 2020 (Kanan)

Gambar 7. Peta Urban Sprawl dengan Legenda Tahun Ekspansi

Gambar 8. Grafik Perubahan Luas Lahan Terbangun 1990–2020

Gambar 9. Tampilan Citra Komposit Daerah Kajian Banjir

Gambar 10. NDWI (Kiri) dan Badan Air (Kanan)

Gambar 11. Jarak dari Air (Kiri) dan Harkat Jarak dari Air (Kanan)

Gambar 12. Elevasi SRTM (Kiri) dan Harkat Elevasi (Kanan)

Gambar 13. TPI (Kiri) dan Harkat TPI (Kanan)

Gambar 14. NDVI (Kiri) dan Harkat Vegetasi (Kanan)

Gambar 15. Kerawanan Banjir (Kiri) dan Harkat Kerawanan Banjir (Kanan)

Gambar 16. Penduduk GHSL (Kiri) dan Harkat Penduduk (Kanan)

Gambar 17. Luas Lahan Terbangun (Kiri) dan Harkatnya (Kanan)

Gambar 18. Luas Lahan Pertanian (Kiri) dan Harkatnya (Kanan)

Gambar 19. Eksposur Banjir (Kiri) dan Harkat Eksposur (Kanan)

Gambar 20. Risiko Banjir (Kiri) dan Harkat Risiko (Kanan)

# DAFTAR TABEL

Tabel 1. Pemetaan Capaian Pembelajaran Mata Kuliah (CPMK) Terhadap Modul Praktikum

Tabel 2. Indeks Lahan Terbangun

Tabel 3. Dataset Google Earth Engine yang Digunakan

Tabel 4. Harkat Variabel Kerawanan Banjir

Tabel 5. Harkat Kerawanan Banjir

Tabel 6. Harkat Variabel Eksposur Banjir

Tabel 7. Harkat Eksposur Banjir

Tabel 8. Harkat Variabel Kerentanan Banjir

Tabel 9. Harkat Kerentanan Banjir

Tabel 10. Harkat Risiko Banjir

Tabel 11. Panduan Memilih Pendekatan Pemetaan Lahan Terbangun

Tabel 12. Standar Penamaan Proyek dan Berkas Pengumpulan Praktikum

Tabel 13. Rubrik dan Matriks Kriteria Penilaian Evaluasi Praktikum

# IDENTITAS MATA KULIAH, PROGRAM STUDI DAN KURIKULUM

| Atribut | Keterangan |
| --- | --- |
| Mata Kuliah | : Pemrograman Geospasial Berbasis Cloud (Praktikum) |
| Mata Kuliah (Inggris) | : Cloud-Based Geospatial Programming (Practicum) |
| Kode Mata Kuliah | : (menyesuaikan kurikulum program studi) |
| SKS | : 3 (2 Teori, 1 Praktikum) |
| Sifat Pengambilan | : Pilihan |
| Bentuk Pembelajaran | : Tutorial, Praktik |
| Metode Pembelajaran | : Problem Based Learning, Project Based Learning |
| Media | : Daring (Google Earth Engine Code Editor) |
| Semester | : V |
| Kelompok Mata Kuliah | : Mata Kuliah KBK Multimedia |
| Program Pendidikan | : Sarjana Terapan (D-4) Prodi Teknik Informatika |
| Jurusan | : Teknik Komputer & Informatika |
| Penyusun | : Tim Praktikum Pemrograman Geospasial Berbasis Cloud |

# CAPAIAN PEMBELAJARAN

**Tabel 1. Pemetaan Capaian Pembelajaran Mata Kuliah (CPMK) Terhadap Modul Praktikum**

| CAPAIAN PEMBELAJARAN MATA KULIAH | INTEGRASI DENGAN MODUL PRAKTIKUM |
| --- | --- |
| **CPMK 1** Mahasiswa mampu menjelaskan konsep data raster dan vektor serta arsip data penginderaan jauh pada katalog cloud computing (komputasi awan). | **BAGIAN I, III.1, III.2** |
| **CPMK 2** Mahasiswa mampu menerapkan pemfilteran image collection (koleksi citra), cloud masking (penghapusan awan), dan komposit untuk menghasilkan citra analisis bebas awan. | **III.3, III.4, III.6** |
| **CPMK 3** Mahasiswa mampu menganalisis tutupan lahan menggunakan klasifikasi unsupervised (clustering) dan indeks spektral. | **III.3, III.4** |
| **CPMK 4** Mahasiswa mampu mengimplementasikan analisis multitemporal untuk deteksi perubahan tutupan lahan (urban sprawl) menggunakan JavaScript di Earth Engine. | **III.5** |
| **CPMK 5** Mahasiswa mampu merancang model risiko bencana banjir multikriteria yang mengintegrasikan variabel fisik, sosial, dan ekonomi. | **III.6, III.7** |

# BAGIAN I. BAHAN KAJIAN

## I.1. Penggunaan Pedoman

Pedoman ini memberikan instruksi sistematis mengenai tata cara persiapan, pengoperasian, penyelesaian tugas praktikum analisis geospasial berbasis cloud untuk praktikum Intermediate Google Earth Engine, hingga mekanisme evaluasi.

Alur yang disarankan: (1) baca BAGIAN II untuk memastikan akun Earth Engine dan perangkat siap; (2) kerjakan BAGIAN III secara berurutan dari Task I sambil menyalin dan menjalankan setiap potongan kode di Earth Engine Code Editor; (3) dokumentasikan setiap peta dan keluaran konsol sebagai bahan laporan; (4) uji diri dengan Tugas Praktikum (III.9); (5) tantang kemampuan dengan soal HOTS (III.10). Alokasikan sekitar dua kali 50 menit untuk Task I–III dan dua kali 50 menit untuk Task IV–V, ditambah waktu latihan sesuai selera.

## I.2. Ruang Lingkup

Kegiatan mencakup: penyaringan image collection (koleksi citra) berdasarkan lokasi, waktu, dan metadata; pembacaan metadata; cloud masking (penghapusan awan) berbasis operasi bit pada band QA_PIXEL; scaling (penskalaan) nilai reflektansi; komposit median; klasifikasi unsupervised (tanpa data latih) menggunakan clusterer (pengelompok) k-means ee.Clusterer.wekaKMeans; perhitungan indeks spektral NDBI, NDWI, MNDWI, dan NDVI melalui expression (aljabar peta); thresholding (ambangan) dan masking; iterasi client-side dengan perulangan for dan metode map; pembuatan koleksi citra multitemporal Landsat 4–9; pemetaan urban sprawl (ekspansi perkotaan) dengan komposit minimum; pembuatan legenda ui.Panel dan grafik ui.Chart; serta pemodelan risiko banjir berbasis harkat (penskoran) multikriteria yang menggabungkan jarak dari sungai, elevasi, TPI, NDVI, penduduk, tutupan lahan, PDB, dan IPM.

## I.3. Teknologi

Berikut adalah teknologi yang digunakan pada modul praktikum ini:

- Akun Google yang telah terdaftar Google Earth Engine (gratis untuk penggunaan nonkomersial; pendaftaran di https://code.earthengine.google.com).
- Earth Engine Code Editor, lingkungan pengembangan berbasis peramban dengan bahasa JavaScript (tanpa instalasi apa pun di komputer lokal).
- Katalog data publik Earth Engine: Landsat 4–9 Collection 2 Level-2, SRTM, GHSL Population, ESA WorldCover 10 m, dan dataset gridded GDP/HDI (seluruhnya otomatis tersedia, tanpa perlu mengunggah).
- Peramban modern (Google Chrome / Mozilla Firefox) dan koneksi internet yang stabil.

## I.4. Studi Kasus

Terdapat tiga studi kasus yang meningkat kompleksitasnya. Pertama, pemetaan tutupan lahan terbangun di sekitar Purwodadi, Jawa Timur, menggunakan satu citra Landsat 9 dan clustering k-means tanpa data latih (Task I). Kedua, pemetaan urban sprawl (ekspansi perkotaan) Jabodetabekpunjur (Jakarta, Bogor, Depok, Tangerang, Bekasi, dan Puncak Cianjur) – salah satu wilayah perkotaan terbesar di dunia – dari komposit Landsat tahun 1990, 1995, 2000, 2005, 2010, 2015, dan 2020, dilanjutkan analisis perubahan luas dalam hektar (Task II–III). Ketiga, pemodelan risiko banjir pada sub-DAS di sekitar Batanghari, Jambi, yang menggabungkan kerawanan (jarak sungai, elevasi, TPI, vegetasi), eksposur (penduduk, lahan terbangun, lahan pertanian), dan kerentanan (PDB, IPM) menjadi satu peta harkat risiko 1–5 (Task IV–V).

## I.5. Konsep yang Digunakan

**ee.ImageCollection versus ee.Image:** Koleksi citra adalah album foto berisi ratusan ribu salindia (scene) yang masing-masing tercatat lokasi dan waktunya; satu salindia adalah ee.Image dengan banyak saluran (band) layaknya berkas TIFF multi-band. Praktik yang benar selalu menyaring album dulu – filterBounds (lokasi), filterDate (waktu), filterMetadata (kualitas) – sebelum memprosesnya, supaya server hanya menghitung salindia yang relevan. Ibarat mencari foto liburan: saring berdasarkan album, tahun, dan tempat dulu, jangan minta komputer menonton seluruh perpustakaan foto.

**Cloud Masking dan Komposit Median:** Awan menghalangi permukaan bumi, tetapi band QA_PIXEL pada Landsat menyimpan “catatan kecurigaan” setiap piksel dalam bentuk bit. Operasi bitwiseAnd memeriksa apakah bit tertentu (awan, bayangan awan, cirrus) menyala; piksel yang dicurigai dibuang dengan updateMask. Karena satu salindia jarang bersih penuh, puluhan salindia yang sudah dibersihkan dilebur menjadi satu citra komposit: median() mengambil nilai tengah tiap piksel sehingga sisa awan dan bayangan yang lolos tersingkirkan. Ibarat memotret pemandangan yang sama ratusan kali lalu memilih keadaan “paling umum” tiap titik: penghalang sesaat tidak akan pernah menang melawan mayoritas.

**Clustering (Klasifikasi Tanpa Data Latih):** Clustering mengelompokkan piksel berdasarkan kemiripan nilai spektralnya tanpa memerlukan contoh (label). wekaKMeans(15) mengajarkan model mengenali 15 kelompok dari 500 piksel contoh, lalu seluruh citra ditag ke kelompok terdekat. Penafsiran “kelompok mana yang adalah bangunan” tetap tugas manusia: bandingkan peta cluster dengan citra asli. Ibarat menuangkan sekotak krayon campur ke meja: krayon mengelompok sendiri berdasarkan warna, tetapi hanya Anda yang tahu kelompok mana “merah tua”.

**Indeks Spektral (Aljabar Band):** Indeks spektral adalah rasio selisih dan jumlah dua band yang mementangkan dua objek. NDBI memanfaatkan pantulan SWIR yang tinggi pada atap dan aspal namun rendah pada NIR; NDWI dan MNDWI mementangkan air terhadap vegetasi/tanah; NDVI mementangkan vegetasi hijau (NIR tinggi, merah rendah). Karena berbentuk rasio ternormalisasi, nilainya terkunci di antara  sampai  sehingga ambangan lintas waktu dan lintas sensor lebih stabil dibanding nilai band mentah. Metode expression() memungkinkan rumus ditulis hampir sepenuh teks matematika.

**Thresholding dan Masking:** Indeks kontinu diubah menjadi peta biner (0/1) dengan ambangan, misalnya air = NDWI . selfMask() menyembunyikan piksel nol sehingga peta hanya menampilkan objek yang dipilih; eq, gt, and adalah kalimat logika piksel-demi-piksel.

**Iterasi client-side dan map:** Perulangan for JavaScript berjalan di komputer praktikan; metode map pada daftar dan koleksi server mengirim fungsi untuk dijalankan di server Google. Keduanya dipakai bergantian: daftar tahun dipetakan dengan map menjadi koleksi citra tahunan. Ibarat lini produksi: satu resep (fungsi) diterapkan ke setiap item tanpa menyalin resep berkali-kali.

**Urban Sprawl dengan Komposit Minimum:** Jika piksel lahan terbangun diberi nilai tahun deteksinya, maka min() lintas tahun menagih tahun terawal piksel tersebut menjadi terbangun – peta ekspansi terbentuk tanpa membandingkan pasangan citra secara manual. Warna pada legenda menunjukkan “gelombang” perluasan kota dari pusat ke pinggiran.

**Harkat (Penskoran) Multikriteria Risiko Banjir:** Risiko = kerawanan (hazard) + eksposur (exposure) + kerentanan (vulnerability). Tiap variabel diskor 1 (tidak berbahaya/terdampak/rentan) sampai 5 (sangat), dijumlahkan, lalu diharkat kembali menjadi lima kelas. Pendekatan ini sederhana dan transparan – asumsi dapat diaudit siapa pun – namun sensitif pada pemilihan ambangan kelas. Ibarat menilai kelayakan rumah: jumlahkan skor lokasi, bahan bangunan, dan penghuni; skor tinggi bukan vonis, melainkan bendera untuk ditelusuri lebih lanjut.

**Operasi Ruang Lanjutan:** fastDistanceTransform menghitung jarak setiap piksel ke badan air terdekat (hasilnya jarak kuadrat dalam piksel, sehingga perlu sqrt().multiply(30) menjadi meter); focalMean merata-ratakan elevasi lingkungan sebagai pembanding TPI; reduceResolution meringkas data 10 m WorldCover ke piksel 30 m dengan penjumlahan; ui.Chart.image.series membuat grafik deret waktu tanpa mengekspor data.

# BAGIAN II. PENYIAPAN PELAKSANAAN PRAKTIKUM (PREPARATION)

## II.1. Peralatan Praktikum

Kebutuhan peralatan praktikum dapat dilihat pada daftar berikut:

**Perangkat Keras (Hardware):**

- PC/Laptop (Processor Dual-Core 2.0 GHz+, RAM minimal 4 GB, Ruang Disk minimal 1 GB). Seluruh komputasi berat terjadi di server Google, sehingga spesifikasi rendah tetap memadai.
- Koneksi internet yang stabil (wajib; Code Editor dan peta berjalan sepenuhnya di peramban).

**Perangkat Lunak Sistem (System Software):**

- Sistem Operasi Windows 10/11 64-bit, Linux, atau macOS.

**Development Tools:**

- Akun Google (Gmail) yang telah terdaftar Google Earth Engine. Pendaftaran: buka https://code.earthengine.google.com, masuk dengan akun Google, ikuti wizard pendaftaran (untuk penggunaan riset/pendidikan umumnya langsung disetujui), lalu setujui ketentuan penggunaan saat pertama kali masuk.
- Peramban modern (Google Chrome direkomendasikan / Mozilla Firefox).
- (Opsional) Akun Google Drive/Google Cloud untuk ekspor hasil di luar cakupan modul.

**Pengetahuan Prasyarat:**

- Dasar sintaksis JavaScript (var, fungsi, array, perulangan for) – modul menyegarkan hal ini pada Task III.
- Konsep dasar penginderaan jauh (band, resolusi, reflektansi) pada level modul Basic GEE atau setara.

## II.2. Keamanan & Keselamatan Kerja

Komputer merupakan perangkat teknologi komunikasi dan informasi yang sering digunakan dewasa ini. Pada saat bekerja dengan komputer ada beberapa hal yang harus diperhatikan agar tidak berdampak buruk bagi kesehatan bahkan keselamatan kita. Komputer dapat menyebabkan penggunanya menderita nyeri otot dan tulang terutama bahu, pergelangan tangan, leher, punggung, pinggang bagian bawah, mata merah berair, bahkan gangguan penglihatan.

Beberapa hal yang bisa dilakukan untuk menghindari efek negatif dari bekerja dengan komputer:

- Aturlah posisi tubuh saat bekerja dengan komputer sehingga merasa nyaman.
- Aturlah posisi perangkat komputer dan ruangan sehingga memberi rasa nyaman.
- Makan, minum, dan istirahatlah yang cukup.
- Gerakkan badan untuk mengurangi ketegangan otot dan pikiran, dan olahragalah secara teratur.
- Sesekali alihkan pandangan ke luar ruangan untuk menyegarkan mata.

**Mengatur posisi tubuh:**

- Posisi Kepala & Leher harus tegak lurus dengan wajah menghadap langsung ke komputer, jangan menengadah atau membungkuk.
- Posisi Punggung yang baik adalah tegak, tidak miring ke kanan/kiri, tidak membungkuk dan tidak menyandar terlalu ke belakang.
- Posisi Pundak tidak terlalu terangkat dan tidak terlalu ke bawah, pastikan otot pundak tidak tegang.
- Posisi Lengan & Siku yang baik adalah apabila mengetik dan menggunakan mouse dengan nyaman.
- Posisi Kaki harus bebas, diluruskan sesekali agar aliran darah lancar.

**Mengatur Posisi Komputer:**

- Monitor harus diletakkan di tempat yang tidak memantulkan cahaya lain.
- Letakkan monitor lebih rendah dari garis horizontal mata.
- Aturlah cahaya monitor (kontras/kecerahan) agar tidak terlalu gelap dan terang.
- Sering-seringlah mengedipkan mata (minimal 5 detik setiap 10 menit).

**Istirahat Mata:** Terapkan aturan 20-20-20, yaitu setiap 20 menit alihkan pandangan ke objek yang berjarak 20 kaki (±6 meter) selama 20 detik, untuk mencegah kelelahan mata akibat paparan monitor visual.

**Etika Penggunaan Sumber Daya Cloud:** Earth Engine berbagi kuota komputasi antar seluruh pengguna dunia. Biasakan menyaring koleksi (filterBounds, filterDate) sebelum operasi berat; hindari memanggil getInfo() berulang kali di dalam perulangan; jangan meminta resolusi yang tidak diperlukan. Kebiasaan ini analog dengan tidak menyalakan semua kompor sekaligus hanya untuk merebus satu telur.

# BAGIAN III. PROSEDUR PELAKSANAAN PRAKTIKUM (STEP BY STEP)

## III.1. Teori Singkat: Arsitektur Google Earth Engine dan Kerangka Analisis

Google Earth Engine adalah platform komputasi geospasial skala planet: katalog petabyte berisi lebih dari 40 tahun citra satelit dan dataset siap analisis, dipadu kluster komputasi Google untuk memprosesnya (Gorelick dkk., 2017). Praktikan tidak mengunduh data; praktikan mengirim *deskripsi* komputasi (skrip JavaScript) yang dieksekusi server-side (di sisi server), lalu menerima hasilnya sebagai peta interaktif, angka di konsol, atau grafik. Konsekuensi penting: objek ee.* adalah referensi ke objek di server, bukan datanya. print(image) menampilkan metadata, bukan piksel; nilai piksel baru “ditarik” saat peta dirender atau saat reduksi eksplisit.

**Objek utama:** Vektor diwakili ee.Geometry (bentuk), ee.Feature (bentuk + atribut), dan ee.FeatureCollection (kumpulan fitur, versi GEE dari GeoJSON feature collection). Raster diwakili ee.Image (satu citra multi-band, layaknya TIFF) dan ee.ImageCollection (kumpulan citra bertanda lokasi dan waktu). Pola kerja standar: **filter** (sempitkan koleksi)  **map** (bersihkan tiap citra)  **reduce** (lebur menjadi satu citra/statistik)  **visualize** (tampilkan dengan parameter).

**Indeks lahan terbangun:** Deteksi lahan terbangun (built-up) dapat dilakukan dengan banyak indeks; modul ini memakai NDBI karena rumusnya paling sederhana, sementara alternatifnya dirangkum berikut.

**Tabel 2. Indeks Lahan Terbangun** (sumber: Kaimaris & Patias, 2018)

| No. | Indeks | Rumus |
| --- | --- | --- |
| 1 | Normalized Difference Built-up Index (NDBI) |  |
| 2 | Index-based Built-up Index (IBI) |  |
| 3 | New Built-up Index (NBI) |  |
| 4 | Normalized Difference Impervious Surface Index (NDISI) |  |
| 5 | Band Ratio for Built-up Area (BRBA) |  |
| 6 | Normalized Difference Built-up Area Index (NBAI) |  |
| 7 | Modified Built-up Index (MBI) |  |
| 8 | Built-up Area Extraction Index (BAEI) |  |

Indeks air dan vegetasi yang menyertai modul ini:

- **NDWI** , digunakan untuk masking (penandaan) badan air.
- **MNDWI** , varian yang lebih tahan terhadap latar terbangun (Xu, 2006), dipakai pada analisis multitemporal.
- **NDVI** , indikator kerapatan vegetasi hijau.

**Kerangka risiko banjir:** Risiko banjir adalah gabungan tiga komponen. **Kerawanan (hazard)** adalah bagian wilayah yang secara langsung terkena banjir, misalnya dataran banjir di sisi sungai; semakin sering dan semakin dekat, semakin rawan. **Eksposur (exposure)** mengacu pada aset yang berada di jalur bahaya: penduduk, lahan pertanian, lahan terbangun; semakin banyak yang terdampak, semakin tinggi eksposur. **Kerentanan (vulnerability)** mengacu pada kemampuan bertahan dan memulihkan diri, diwakili PDB (kemampuan ekonomi) dan IPM (kualitas sumber daya manusia); semakin rendah kemampuannya, semakin rentan. Nilai harkat (skor) 1–5 ditetapkan per variabel mengikuti Tabel 4, 6, dan 8 pada task masing-masing; jumlah skor diharkat kembali menjadi lima kelas mengikuti Tabel 5, 7, 9, dan 10.

## III.2. Environment & Setup Praktikum

Praktikum menggunakan **Earth Engine Code Editor** di peramban. Prosedur persiapan:

1. Buka https://code.earthengine.google.com dan masuk dengan akun Google yang sudah terdaftar GEE.
2. Kenali lima panel: **skrip** (kiri tengah), **dokumentasi Docs** (kiri, daftar semua objek ee.\*), **konsol** (kanan atas, keluaran print), **inspektur** (kanan tengah, klik peta untuk membaca nilai piksel), dan **peta** (kanan bawah, dengan pengatur layer dan tombol Run).
3. Uji koneksi dengan skrip pembuka berikut; klik **Run**, lalu pastikan konsol menampilkan nama-nama band.

```
var citraUji = ee.Image('LANDSAT/LC09/C02/T1_L2/LC09_122065_20220119');
print('Band citra uji:', citraUji.bandNames());
```

4. Buat repository skrip praktikum: klik ikon **New** pada panel Scripts, beri nama repositori misalnya praktikum-gee; simpan setiap task sebagai skrip terpisah (task1.js dst.) agar mudah dilanjutkan di pertemuan berikutnya.

Data yang digunakan sepanjang modul dirangkum pada Tabel 3; seluruhnya publik dan otomatis tersedia di katalog.

**Tabel 3. Dataset Google Earth Engine yang Digunakan**

| Dataset | ID Aset | Resolusi | Peran dalam Modul |
| --- | --- | --- | --- |
| Landsat 4 TM | LANDSAT/LT04/C02/T1_L2 | 30 m | Komposit 1990 (SWIR: SR_B5, NIR: SR_B4, dst.) |
| Landsat 5 TM | LANDSAT/LT05/C02/T1_L2 | 30 m | Komposit 1990–2010 |
| Landsat 7 ETM+ | LANDSAT/LE07/C02/T1_L2 | 30 m | Komposit 1995–2010 |
| Landsat 8 OLI | LANDSAT/LC08/C02/T1_L2 | 30 m | Komposit 2015–2020 (SWIR: SR_B6, NIR: SR_B5, dst.) |
| Landsat 9 OLI-2 | LANDSAT/LC09/C02/T1_L2 | 30 m | Task I; komposit 2015–2020 |
| SRTM | USGS/SRTMGL1_003 | 30 m | Elevasi dan TPI (Task IV) |
| GHSL Population | JRC/GHSL/P2023A/GHS_POP | ±100 m | Kepadatan penduduk (Task V) |
| ESA WorldCover v200 | ESA/WorldCover/v200 | 10 m | Kelas 40 = pertanian, 50 = terbangun (Task V) |
| GDP PPP gridded | projects/sat-io/open-datasets/GRIDDED_HDI_GDP/GDP_PPP_1990_2015_5arcmin_v2 | ±5 km | PDB, band b26 = 2015 (Task V) |
| HDI gridded | projects/sat-io/open-datasets/GRIDDED_HDI_GDP/HDI_1990_2015_v2 | ±5 km | IPM, band b26 = 2015 (Task V) |

Perhatikan perbedaan penamaan band antar sensor: pada Landsat 4–7 (TM/ETM+), SWIR adalah SR_B5 dan NIR SR_B4; pada Landsat 8–9 (OLI), SWIR bergeser ke SR_B6 dan NIR ke SR_B5. Modul menyamakan semuanya menjadi nama generik B2–B7 (biru–SWIR) segera setelah cloud masking agar rumus indeks berlaku lintas sensor.

## III.3. Task I: Filter Citra dan Clustering Tutupan Lahan

**TASK I: SINGLE IMAGE, METADATA, DAN CLUSTERING K-MEANS (PURWODADI)**

Task pembuka melatih pola dasar bekerja dengan koleksi citra: menyaring, membaca metadata, mengambil satu citra terbaik, lalu mengelompokkan tutupan lahannya tanpa data latih sama sekali.

1. Panggil koleksi Landsat 9, buat titik kajian di Purwodadi, lalu saring berdasarkan lokasi, metadata tutupan awan, dan urutkan:

```
// 1. Panggil data Landsat 9
var dataset = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2');

// 2. Geometry untuk filter berdasarkan lokasi
var geometry = ee.Geometry.Point([112.05730244401117, -6.897418238470722]);

// 3. Filter lokasi + filter metadata + urutkan tutupan awan
dataset = dataset
  .filterBounds(geometry)
  .filterMetadata('CLOUD_COVER_LAND', 'less_than', 50)
  .sort('CLOUD_COVER_LAND');

// 4. Intip metadata apa saja yang tersimpan pada citra
print('Daftar metadata:', dataset.first().propertyNames());

// 5. Metadata spesifik: tutupan awan di daratan
print('CLOUD_COVER_LAND:', dataset.first().get('CLOUD_COVER_LAND'));

// 6. Ambil satu citra (awan paling tipis karena sudah di-sort)
var img = dataset.first();
```

**Cara membaca kode (bahasa awam):**

- filterBounds(geometry) = ambil hanya salindia yang menutup titik Purwodadi; salindia lain di seluruh dunia tidak disentuh.
- filterMetadata('CLOUD_COVER_LAND', 'less_than', 50) = buang salindia yang tutupan awannya di atas 50%, dibaca langsung dari “kartu identitas” (metadata) tanpa memeriksa piksel.
- sort('CLOUD_COVER_LAND') = susun dari yang paling bersih, sehingga first() pasti mengembalikan citra terbaik.
- propertyNames() = daftar seluruh kolom metadata (tanggal, posisi, persentase awan, dan sebagainya).

Contoh keluaran konsol (nilai bergantung waktu akses):

```
Daftar metadata: ["CLOUD_COVER", "CLOUD_COVER_LAND", "DATE_ACQUIRED", "SUN_ELEVATION", "system:time_start", ...]
CLOUD_COVER_LAND: 4.35
```

2. Tampilkan citra terpilih dengan visual parameter warna asli (komposit true color), lalu jalankan clustering pada wilayah kecil:

```
// 7. Visual parameter true color (merah-hijau-biru)
var imageVisParam = {
  opacity: 1,
  bands: ['SR_B4', 'SR_B3', 'SR_B2'],
  min: 7061,
  max: 14103,
  gamma: 1
};
Map.addLayer(img, imageVisParam, 'Data paling bersih');
Map.centerObject(geometry, 11);

// 8. Poligon batas wilayah kajian clustering
var geometry2 = ee.Geometry.Polygon(
  [[[111.56510661311408, -7.125131151145682],
    [111.56510661311408, -7.178102498857165],
    [111.62192652888557, -7.178102498857165],
    [111.62192652888557, -7.125131151145682]]], null, false);

// 9. Pilih band reflektansi dan potong ke wilayah kajian
var band = ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'];
var img_pilih = img.select(band).clip(geometry2);

// 10. Ambil 500 piksel contoh sebagai bahan latih clusterer
var data_training = img_pilih.sample({
  region: geometry2,
  scale: 30,
  numPixels: 500
});

// 11. Latih model k-means 15 kelompok, lalu terapkan ke seluruh citra
var cluster_model = ee.Clusterer.wekaKMeans(15).train(data_training);
var hasil = img_pilih.cluster(cluster_model);

// 12. Pilih kelompok yang tampak sebagai bangunan, sembunyikan yang lain
var lahan_terbangun = hasil.eq(2).or(hasil.eq(3)).selfMask();

// 13. Tampilkan hasilnya
Map.addLayer(lahan_terbangun, {
  bands: ['cluster'],
  min: 1,
  palette: ['ff7070']
}, 'Bangunan');
```

**Cara membaca kode (bahasa awam):**

- sample({region, scale, numPixels}) = ambil 500 piksel acak sebagai “bahan belajar”; 30 m adalah ukuran piksel asli Landsat.
- wekaKMeans(15) = mesin pengelompok k-means dengan 15 kelompok; jumlah ini dapat diubah sesuai keragaman lahan.
- hasil.eq(2).or(hasil.eq(3)) = kelompok nomor 2 dan 3 ditandai sebagai kandidat lahan terbangun – nomor ini tidak tetap, amati dulu peta cluster mentah (hasil) lalu pilih.
- selfMask() = piksel bernilai 0 (bukan kandidat) disembunyikan agar peta bersih.

> **\[GAMBAR 1 – TANGKAPAN LAYAR PRAKTIKAN] Hasil Akhir Clustering Tutupan Lahan Terbangun (Purwodadi)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Bangunan** (merah) menumpuk layer **Data paling bersih**, arahkan peta pada poligon kajian hingga bercak merah kawasan terbangun Purwodadi terlihat jelas. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-01-clustering.png di folder gambar/.

3. **Tuliskan Lesson Learnt**: clustering tidak membutuhkan data latih berlabel, tetapi penafsiran kelompok tetap tugas manusia; filter metadata sebelum komputasi piksel membuat proses nyaris instan; nomor kelompok k-means bisa berubah setiap dijalankan ulang karena pemilihan titik awal acak.

**Penjelasan:** K-means mengelompokkan berdasarkan jarak spektral di ruang 7 dimensi (tujuh band). Karena atap dan jalan punya tanda tangan spektral serupa, mereka cenderung jatuh pada kelompok yang sama – tetapi lahan kering terang bisa ikut tersangkut, itulah sebabnya hasil clustering selalu perlu pemeriksaan visual dan, dalam praktik profesional, digabung dengan NDWI untuk membuang air.

## III.4. Task II: Komposit Median, Indeks Spektral, dan Pemetaan Lahan Terbangun

**TASK II: CLOUD MASKING QA\_PIXEL, KOMPOSIT MEDIAN, NDBI/NDWI, THRESHOLDING (JABODETABEKPUNJUR)**

Satu citra bersih masih menyisakan masalah: piksel tertutup awan dan bayangan. Task ini melebur banyak citra tahun 2022 menjadi satu komposit median yang hampir bebas awan, lalu menerapkan indeks spektral dan ambangan untuk memisahkan air dan lahan terbangun.

1. Siapkan wilayah kajian (ROI, region of interest) dan saring koleksi Landsat 8 sepanjang 2022:

```
// ROI Jabodetabekpunjur
var roi = ee.Geometry({
  geodesic: false,
  type: 'Polygon',
  coordinates: [[
    [106.53598136542733, -6.6221756519036195],
    [107.23910636542733, -6.6221756519036195],
    [107.23910636542733, -5.928728445061094],
    [106.53598136542733, -5.928728445061094],
    [106.53598136542733, -6.6221756519036195]
  ]]
});

var l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2');
var filtered = l8.filterBounds(roi).filterDate('2022-01-01', '2022-12-31');
```

2. Tulis fungsi cloud masking sekaligus penskalaan dan penyeragaman nama band:

```
function cloudMask(image) {
  var qa = image.select('QA_PIXEL');      // band penanda kualitas piksel
  var dilated = 1 << 1;                   // bit 1: awan melebar
  var cirrus  = 1 << 2;                   // bit 2: awan cirrus (tipis)
  var cloud   = 1 << 3;                   // bit 3: awan
  var shadow  = 1 << 4;                   // bit 4: bayangan awan
  var mask = qa.bitwiseAnd(dilated).eq(0)
    .and(qa.bitwiseAnd(cirrus).eq(0))
    .and(qa.bitwiseAnd(cloud).eq(0))
    .and(qa.bitwiseAnd(shadow).eq(0));
  var rename = image.select(
    ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
    ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']);
  var scaled = rename.multiply(0.0000275).add(-0.2);
  return scaled.updateMask(mask);
}

// Terapkan ke seluruh koleksi + komposit median
var median = filtered.map(cloudMask).median().clip(roi);

// Tampilkan komposit warna palsu: NIR-SWIR-Biru
Map.addLayer(median, {
  bands: ['B5', 'B6', 'B2'],
  min: [0.1, 0.05, 0],
  max: [0.4, 0.3, 0.15]
}, 'Image');
Map.centerObject(roi, 9);
```

**Cara membaca kode (bahasa awam):**

- 1 << 3 = geser angka 1 sebanyak tiga posisi bit, hasilnya 8; bit ke-3 “menyala” dan siap diperiksa.
- qa.bitwiseAnd(cloud).eq(0) = tanya pada tiap piksel: “apakah bit awan Anda mati?”; .and(...) merangkai empat pertanyaan menjadi satu syarat.
- updateMask(mask) = piksel yang gagal syarat ditutup (menjadi kosong), bukan dinolkan.
- multiply(0.0000275).add(-0.2) = resep resmi USGS mengubah angka utuh UInt16 menjadi reflektansi 0–1 agar ambangan indeks bermakna fisis.
- median() = untuk tiap piksel, ambil nilai tengah dari belasan citra; awan yang cuma muncul di beberapa citra kalah suara terbanyak.

> **\[GAMBAR 2 – TANGKAPAN LAYAR PRAKTIKAN] Tampilan Citra Komposit RGB (SWIR-NIR-Biru) di Code Editor**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Image** (komposit NIR-SWIR-Biru tahun 2022) pada ROI Jabodetabekpunjur; pastikan seluruh ROI terbingkai dan warna komposit tidak terlalu gelap/terang. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-02-komposit.png di folder gambar/.

3. Hitung NDBI dan NDWI dengan expression, lalu terapkan ambangan untuk memisahkan air dan lahan terbangun:

```
// Kamus nama variabel -> band citra
var bandMap = {
  NIR:   median.select('B5'),
  SWIR:  median.select('B6'),
  GREEN: median.select('B3')
};

// NDBI: positif = kecenderungan terbangun
var ndbi = median.expression('(SWIR - NIR) / (SWIR + NIR)', bandMap);
Map.addLayer(ndbi, {min: -1, max: 1, palette: ['blue', 'white', 'red']}, 'NDBI');

// NDWI: positif = kecenderungan air
var ndwi = median.expression('(GREEN - NIR) / (GREEN + NIR)', bandMap);
Map.addLayer(ndwi, {min: -1, max: 1, palette: ['red', 'white', 'blue']}, 'NDWI');

// Thresholding
var air = ndwi.gt(0.1);                     // air = NDWI > 0.1
Map.addLayer(air.selfMask(), {palette: 'blue'}, 'Air');

var bangunan = ndbi.gt(-0.1).and(air.eq(0)); // NDBI > -0.1 dan bukan air
Map.addLayer(bangunan.selfMask(), {palette: 'red'}, 'Bangunan');
```

**Cara membaca kode (bahasa awam):**

- expression('(SWIR - NIR) / (SWIR + NIR)', bandMap) = tulis rumus seperti di buku; bandMap menerjemahkan setiap nama di rumus ke band citra sesungguhnya.
- ndwi.gt(0.1) = uji “lebih besar dari” per piksel, hasil peta benar/salah (1/0).
- bangunan = ndbi.gt(-0.1).and(air.eq(0)) = dua syarat digabung: mencurigakan sebagai terbangun DAN tidak tercatat air; perhatikan air kerap menipu NDBI sehingga syarat kedua wajib.

> **\[GAMBAR 3 – TANGKAPAN LAYAR PRAKTIKAN] Tampilan NDBI (Kiri) dan NDWI (Kanan) Jabodetabekpunjur**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **NDBI** dan **NDWI** lalu sajikan dua tangkapan layar berdampingan pada area yang sama (merah pada NDBI = kecenderungan terbangun; biru pada NDWI = air). Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-03-ndbi-ndwi.png di folder gambar/.
>
> **\[GAMBAR 4 – TANGKAPAN LAYAR PRAKTIKAN] Lahan Terbangun (Merah) dan Air (Biru) Hasil Thresholding**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Air** (biru) dan **Bangunan** (merah) secara bersamaan; pilih bingkai area pesisir atau pusat kota agar objek air dan terbangun kontras. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-04-bangunan-air.png di folder gambar/.

4. **Tuliskan Lesson Learnt**: ambangan  pada NDBI dan  pada NDWI bukan konstanta alam, melainkan titik awal yang perlu dikalibrasi per wilayah (gunakan inspektur untuk membaca nilai pada objek yang jelas); NDWI dan NDBI harus dipakai berpasangan karena air sering menyamar sebagai terbangun pada NDBI.

**Penjelasan:** Mengapa median, bukan rata-rata? Awan tersisa pada sebagian kecil citra akan menarik rata-rata (mean) menjauh dari nilai benar, sedangkan median kebal terhadap pencilan (outlier) selama lebih dari separuh citra bersih – pada koleksi setahun, kondisi ini hampir selalu terpenuhi.

## III.5. Task III: Iterasi Multitemporal dan Peta Urban Sprawl

**TASK III: PERULANGAN, KOLEKSI 1990–2020, KOMPOSIT MINIMUM, LEGENDA, DAN GRAFIK**

Task inti modul: mengotomatiskan seluruh resep Task II untuk tujuh titik waktu dan lima satelit sekaligus, lalu membaca ekspansi kota dari hasilnya.

1. Segarkan ingatan iterasi JavaScript (berjalan di komputer praktikan):

```
// For loop umum: cetak angka 0 sampai 29
for (var i = 0; i < 30; i++) {
  print(i);
}

// map pada array: ubah setiap unsur tanpa menyalin-tempel
var names = ['Ahmad', 'Agung', 'Andi'];
var namesNew = names.map(function(name) {
  return name + ' Keren';
});
print(namesNew);   // [Ahmad Keren, Agung Keren, Andi Keren]

var lists = [{name: 'A', year: 2010}, {name: 'B', year: 2011}];
print(lists.map(function(obj) { return obj.name; }));   // [A, B]
```

2. Siapkan lima koleksi Landsat, dua varian cloud mask (TM dan OLI), dan dua fungsi komposit:

```
var l4 = ee.ImageCollection('LANDSAT/LT04/C02/T1_L2');
var l5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2');
var l7 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2');
var l9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2');

var yearList = [1990, 1995, 2000, 2005, 2010, 2015, 2020];

function filterCol(col, roi, date) {
  return col.filterDate(date[0], date[1]).filterBounds(roi);
}

// Cloud mask Landsat 4/5/7 (TM): urutan band beda, tanpa cirrus
function cloudMaskTm(image) {
  var qa = image.select('QA_PIXEL');
  var mask = qa.bitwiseAnd(1 << 1).eq(0)
    .and(qa.bitwiseAnd(1 << 3).eq(0))
    .and(qa.bitwiseAnd(1 << 4).eq(0));
  return image
    .select(['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'],
            ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
    .updateMask(mask);
}

// Cloud mask Landsat 8/9 (OLI): sekelas Task II
function cloudMaskOli(image) {
  var qa = image.select('QA_PIXEL');
  var mask = qa.bitwiseAnd(1 << 1).eq(0)
    .and(qa.bitwiseAnd(1 << 2).eq(0))
    .and(qa.bitwiseAnd(1 << 3).eq(0))
    .and(qa.bitwiseAnd(1 << 4).eq(0));
  return image
    .select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
            ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
    .updateMask(mask);
}

function landsat457(roi, date) {
  var col = filterCol(l4, roi, date)
    .merge(filterCol(l5, roi, date))
    .merge(filterCol(l7, roi, date));
  return col.map(cloudMaskTm).median().clip(roi);
}

function landsat89(roi, date) {
  var col = filterCol(l8, roi, date).merge(filterCol(l9, roi, date));
  return col.map(cloudMaskOli).median().clip(roi);
}
```

**Cara membaca kode (bahasa awam):**

- merge = gabungkan koleksi dari beberapa satelit menjadi satu tumpukan supaya satu tahun cukup sekali dikomposit.
- Dua fungsi cloud mask diperlukan karena urutan band Landsat 4–7 berbeda dari Landsat 8–9; keduanya menyeragamkan hasil akhirnya ke nama B2–B7.
- Pemilihan fungsi dilakukan client-side lewat if (year < 2014): tahun 1990–2010 ditangani TM, 2015–2020 oleh OLI.

3. Petakan daftar tahun menjadi koleksi citra lahan terbangun tahunan:

```
var builtCol = ee.ImageCollection(yearList.map(function(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = ee.Date.fromYMD(year, 12, 31);
  var date = [start, end];

  var landsat = (year < 2014) ? landsat457 : landsat89;

  // Komposit + penskalaan reflektansi
  var image = landsat(roi, date).multiply(0.0000275).add(-0.2);
  Map.addLayer(image, {
    bands: ['B5', 'B6', 'B2'],
    min: [0.1, 0.05, 0],
    max: [0.4, 0.3, 0.15]
  }, 'Landsat_' + year, false);

  // Indeks spektral tahunan
  var bandMapTahun = {
    NIR: image.select('B5'),
    SWIR: image.select('B6'),
    RED: image.select('B4'),
    GREEN: image.select('B3'),
    BLUE: image.select('B2')
  };
  var ndbiTahun = image.expression('(SWIR - NIR) / (SWIR + NIR)', bandMapTahun).rename('NDBI');
  var mndwi = image.expression('(GREEN - SWIR) / (GREEN + SWIR)', bandMapTahun).rename('MNDWI');

  // Lahan terbangun: NILAI PIKSEL = TAHUN deteksi
  var built = ee.Image(0)
    .where(ndbiTahun.gt(-0.1).and(mndwi.lte(0)), year)
    .selfMask()
    .clip(roi);
  Map.addLayer(built, {palette: 'red'}, 'Built-up_' + year, false);

  // Band luas (hektar) untuk grafik
  var area = built.multiply(ee.Image.pixelArea().multiply(0.0001)).rename('area');

  return built.toUint16().rename('built')
    .addBands(area)
    .set('year', year, 'system:time_start', start);
}));
```

**Cara membaca kode (bahasa awam):**

- ee.Image(0).where(syarat, year) = mulai dari kanvas nol; piksel yang memenuhi syarat dicat dengan nilai tahunnya – trik inilah yang membuat peta ekspansi mungkin.
- mndwi.lte(0) = gunakan MNDWI (bukan NDWI) pada analisis multitemporal karena lebih tahan terhadap latar terbangun.
- pixelArea().multiply(0.0001) = luas tiap piksel dalam m persegi dikonversi ke hektar.
- set('year', year, ...) = tempelkan properti tahun agar grafik deret waktu tahu sumbu-x-nya.

> **\[GAMBAR 5 – TANGKAPAN LAYAR PRAKTIKAN] Citra Landsat Tahun 1990 (Kiri) dan 2020 (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Landsat\_1990** dan **Landsat\_2020** (tersembunyi secara default; centang pada panel Layers) lalu sajikan berdampingan pada area yang sama. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-05-lansat-1990-2020.png di folder gambar/.
>
> **\[GAMBAR 6 – TANGKAPAN LAYAR PRAKTIKAN] Lahan Terbangun Tahun 1990 (Kiri) dan 2020 (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Built-up\_1990** dan **Built-up\_2020** berdampingan pada area yang sama; perlihatkan perluasan bercak merah dari tahun ke tahun. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-06-built-1990-2020.png di folder gambar/.

4. Bangun peta urban sprawl dengan komposit minimum lengkap dengan legenda, lalu grafik perubahan luas:

```
// Peta ekspansi: min lintas tahun = tahun TERAWAL piksel menjadi terbangun
var dict = {
  built_class_values: yearList,
  built_class_palette: ['800080', '0000FF', '00FFFF', '008000', 'FFFF00', 'FFA500', 'FF0000']
};
var urbanExpansion = builtCol.select('built').min().set(dict);
Map.addLayer(urbanExpansion, {}, 'Urban_expansion');

// Legenda panel kiri-bawah
var legend = ui.Panel(
  [ui.Label('Urban expansion')],
  ui.Panel.Layout.flow('vertical'),
  {position: 'bottom-left'});
yearList.map(function(year, index) {
  legend.add(ui.Panel([
    ui.Label('', {
      width: '20px', height: '20px',
      backgroundColor: dict.built_class_palette[index],
      border: '0.5px solid black'
    }),
    ui.Label(String(year))
  ], ui.Panel.Layout.flow('horizontal')));
});
Map.add(legend);

// Grafik luas lahan terbangun (Ha) per tahun
var areaChart = ui.Chart.image.series(builtCol.select('area'), roi, ee.Reducer.sum(), 30, 'year')
  .setChartType('AreaChart')
  .setOptions({
    title: 'Urban area (Ha)',
    hAxis: {title: 'Year'},
    vAxis: {title: 'Area (Ha)'}
  });
print(areaChart);
```

**Cara membaca kode (bahasa awam):**

- builtCol.select('built').min() = bandingkan tujuh peta lahan terbangun piksel-demi-piksel dan simpan nilai terkecil = tahun pertama kali terbangun; inilah peta urban sprawl sekaligus.
- ui.Panel + ui.Label = rangkai kotak legenda dari panel dan label; Map.add(legend) menempelkannya ke peta.
- ui.Chart.image.series(...) = minta server menjumlahkan luas tiap tahun lalu menggambarkannya sebagai grafik area – tanpa satu pun angka diunduh manual.

> **\[GAMBAR 7 – TANGKAPAN LAYAR PRAKTIKAN] Peta Urban Sprawl dengan Legenda Tahun Ekspansi**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Urban\_expansion** lengkap dengan panel legenda kiri-bawah berisi tahun 1990–2020; pastikan seluruh ROI Jabodetabekpunjur terlihat. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-07-urban-sprawl.png di folder gambar/.
>
> **\[GAMBAR 8 – TANGKAPAN LAYAR PRAKTIKAN] Grafik Perubahan Luas Lahan Terbangun 1990–2020**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Setelah print(areaChart), tangkap grafik AreaChart “Urban area (Ha)” yang muncul di konsol; pastikan judul serta sumbu Year dan Area (Ha) terbaca jelas. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-08-grafik.png di folder gambar/.

5. **Tuliskan Lesson Learnt**: satu fungsi yang dipetakan lewat map menggantikan tujuh skrip salinan-tempel; komposit min() pada peta bernilai tahun menghasilkan peta “gelombang ekspansi”; grafik menunjukkan pertumbuhan yang selalu naik – diskusikan mengapa luas tidak pernah turun dalam metode ini (jawaban: metode mencatat status terbangun pertama, bukan kehilangan status).

**Penjelasan:** Membaca peta ekspansi: warna ungu (1990) memetakan inti kota lama; cincin warna menuju merah (2020) memetakan sabuk pinggiran yang menyusul terbangun. Jika suatu piksel terdeteksi terbangun pada 1995 lalu “hilang” pada 2000 (misalnya salah deteksi), nilai 1995 tetap dipertahankan oleh min() – metode ini karenanya cenderung optimis terhadap keluasan awal, dan itulah pentingnya kalibrasi ambangan pada Task II.

## III.6. Task IV: Pemodelan Kerawanan Banjir (Hazard)

**TASK IV: JARAK DARI SUNGAI, ELEVASI, TPI, VEGETASI, DAN HARKAT KERAWANAN (BATANGHARI, JAMBI)**

Beralih dari urban ke bencana: kerawanan banjir dimodelkan dari empat variabel fisik yang masing-masing diharkat 1–5 mengikuti Tabel 4, lalu dijumlahkan dan diharkat kembali (Tabel 5).

**Tabel 4. Harkat Variabel Kerawanan Banjir**

| No. | Variabel | Keterangan | Harkat |
| --- | --- | --- | --- |
| 1 | Jarak dari sungai | > 200 m | 1 |
|  |  | 150–200 m | 2 |
|  |  | 100–149 m | 3 |
|  |  | 50–99 m | 4 |
|  |  | < 50 m | 5 |
| 2 | Elevasi | > 20 m | 1 |
|  |  | 15–20 m | 2 |
|  |  | 10–14 m | 3 |
|  |  | 5–9 m | 4 |
|  |  | < 5 m | 5 |
| 3 | TPI | > 0 | 1 |
|  |  | -0.25 s.d. 0 | 2 |
|  |  | -0.5 s.d. -0.25 | 3 |
|  |  | -0.75 s.d. -0.5 | 4 |
|  |  | < -0.75 | 5 |
| 4 | Vegetasi (NDVI) | > 0.5 | 1 |
|  |  | 0.25–0.5 | 2 |
|  |  | 0–0.25 | 3 |
|  |  | -0.25–0 | 4 |
|  |  | < -0.25 | 5 |

**Tabel 5. Harkat Kerawanan Banjir**

| Harkat jumlah variabel | Harkat Kerawanan Banjir | Keterangan |
| --- | --- | --- |
| < 4 | 1 | Sangat tidak berkerawanan |
| 4–8 | 2 | Tidak berkerawanan |
| 9–12 | 3 | Sedang |
| 13–16 | 4 | Berkerawanan |
| > 16 | 5 | Sangat berkerawanan |

1. Siapkan komposit Landsat 8 tahun 2022 pada ROI Batanghari (resep sama dengan Task II):

```
var roi = ee.Geometry({
  geodesic: false,
  type: 'Polygon',
  coordinates: [[
    [103.47443690212873, -1.7079691352593016],
    [103.7202559939256, -1.7079691352593016],
    [103.7202559939256, -1.469108505971908],
    [103.47443690212873, -1.469108505971908],
    [103.47443690212873, -1.7079691352593016]
  ]]
});

var filtered = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
  .filterBounds(roi)
  .filterDate('2022-01-01', '2022-12-31');

// Fungsi cloudMask identik Task II -- salin ke skrip ini
var image = filtered.map(cloudMask).median().clip(roi);

Map.addLayer(image, {bands: ['B5', 'B6', 'B2'], min: [0.1, 0.05, 0], max: [0.4, 0.3, 0.15]}, 'Image');
Map.centerObject(roi, 11);

var bandMap = {
  NIR: image.select('B5'),
  SWIR: image.select('B6'),
  GREEN: image.select('B3'),
  RED: image.select('B4'),
  BLUE: image.select('B2')
};
```

> **\[GAMBAR 9 – TANGKAPAN LAYAR PRAKTIKAN] Tampilan Citra Komposit Daerah Kajian Banjir**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Image** pada ROI Batanghari (Jambi); pastikan jalur sungai/badan air yang menjadi fokus analisis ikut terlihat. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-09-komposit-jambi.png di folder gambar/.

2. Deteksi badan air dengan NDWI, lalu hitung jarak setiap piksel ke air terdekat dan harkatnya:

```
// Badan air
var ndwi = image.expression('(GREEN - NIR) / (GREEN + NIR)', bandMap);
var air = ndwi.gt(0.1);
var bukanAir = air.eq(0);
Map.addLayer(air, {palette: ['black', 'blue'], min: 0, max: 1}, 'Air', false);

// Jarak dari air (meter)
var jarakAir = air.fastDistanceTransform()
  .sqrt().multiply(30)      // jarak kuadrat-piksel -> meter
  .updateMask(bukanAir)
  .clip(roi)
  .reproject('EPSG:4326', null, 30);
Map.addLayer(jarakAir, {min: 0, max: 1000, palette: ['red', 'yellow', 'green']}, 'Jarak dari air', false);

// Harkat jarak (Tabel 4)
var harkatJarakAir = jarakAir.where(jarakAir.gt(200), 1)
  .where(jarakAir.gt(150).and(jarakAir.lte(200)), 2)
  .where(jarakAir.gt(100).and(jarakAir.lte(150)), 3)
  .where(jarakAir.gt(50).and(jarakAir.lte(100)), 4)
  .where(jarakAir.lte(50), 5);
Map.addLayer(harkatJarakAir, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat jarak dari air', false);
```

**Cara membaca kode (bahasa awam):**

- fastDistanceTransform() = banjiri peta dari piksel air dan ukur jarak merambat ke semua tetangga; keluaran aslinya jarak **kuadrat** dalam satuan **piksel**, sehingga sqrt().multiply(30) mengubahnya menjadi meter pada piksel 30 m (koreksi terhadap skrip e-book sumber, lihat Lampiran B).
- reproject('EPSG:4326', null, 30) = kunci perhitungan pada grid 30 m agar nilai jarak konsisten, bukan dihitung pada zoom berapa pun.
- Rantai .where(kondisi, nilai) menimpa nilai band dengan harkat kelas; urutan dari kelas longgar ke ketat menentukan kelas akhir.

> **\[GAMBAR 10 – TANGKAPAN LAYAR PRAKTIKAN] NDWI (Kiri) dan Badan Air (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **NDWI** (gradasi merah-putih-biru) dan **Air** (biner hitam-biru) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-10-ndwi-air.png di folder gambar/.
>
> **\[GAMBAR 11 – TANGKAPAN LAYAR PRAKTIKAN] Jarak dari Air (Kiri) dan Harkat Jarak dari Air (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Jarak dari air** (gradasi merah–hijau) dan **Harkat jarak dari air** (kelas 1–5) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-11-jarak.png di folder gambar/.

3. Tambahkan topografi (elevasi SRTM dan TPI) beserta harkatnya:

```
// Elevasi
var srtm = ee.Image('USGS/SRTMGL1_003').clip(roi).updateMask(bukanAir);
Map.addLayer(srtm, {min: 0, max: 200, palette: ['green', 'yellow', 'red']}, 'Elevasi', false);

var harkatElevasi = srtm.where(srtm.gt(20), 1)
  .where(srtm.gt(15).and(srtm.lte(20)), 2)
  .where(srtm.gt(10).and(srtm.lte(15)), 3)
  .where(srtm.gt(5).and(srtm.lte(10)), 4)
  .where(srtm.lte(5), 5);
Map.addLayer(harkatElevasi, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat elevasi', false);

// TPI = elevasi dikurangi rata-rata elevasi lingkungannya
var tpi = srtm.subtract(srtm.focalMean(3))
  .reproject('EPSG:4326', null, 30)
  .updateMask(bukanAir)
  .clip(roi);
Map.addLayer(tpi, {min: -10, max: 10, palette: ['blue', 'yellow', 'red']}, 'TPI', false);

var harkatTPI = tpi.where(tpi.gt(0), 1)
  .where(tpi.gt(-0.25).and(tpi.lte(0)), 2)
  .where(tpi.gt(-0.5).and(tpi.lte(-0.25)), 3)
  .where(tpi.gt(-0.75).and(tpi.lte(-0.5)), 4)
  .where(tpi.lte(-0.75), 5);
Map.addLayer(harkatTPI, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat TPI', false);
```

**Cara membaca kode (bahasa awam):**

- focalMean(3) = rata-rata elevasi pada lingkaran radius 3 piksel (±90 m); TPI positif berarti titik lebih tinggi dari sekitarnya (punggungan), negatif berarti lebih rendah (cekungan, jalur genangan alami).
- updateMask(bukanAir) = hilangkan badan air dari analisis topografi supaya sungai tidak ikut dinilai “cekungan”.

> **\[GAMBAR 12 – TANGKAPAN LAYAR PRAKTIKAN] Elevasi SRTM (Kiri) dan Harkat Elevasi (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Elevasi** (SRTM) dan **Harkat elevasi** (kelas 1–5) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-12-elevasi.png di folder gambar/.
>
> **\[GAMBAR 13 – TANGKAPAN LAYAR PRAKTIKAN] TPI (Kiri) dan Harkat TPI (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **TPI** (biru = cekungan, merah = punggungan) dan **Harkat TPI** (kelas 1–5) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-13-tpi.png di folder gambar/.

4. Tutup kerawanan dengan vegetasi (NDVI), jumlahkan seluruh harkat variabel, dan harkatkan hasilnya:

```
// Vegetasi
var ndvi = image.expression('(NIR - RED) / (NIR + RED)', bandMap).updateMask(bukanAir);
Map.addLayer(ndvi, {min: -1, max: 1, palette: ['blue', 'white', 'green']}, 'NDVI', false);

var harkatNDVI = ndvi.where(ndvi.gt(0.5), 1)
  .where(ndvi.gt(0.25).and(ndvi.lte(0.5)), 2)
  .where(ndvi.gt(0).and(ndvi.lte(0.25)), 3)
  .where(ndvi.gt(-0.25).and(ndvi.lte(0)), 4)
  .where(ndvi.lte(-0.25), 5);
Map.addLayer(harkatNDVI, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat NDVI', false);

// Jumlah harkat keempat variabel (4 s.d. 20) lalu harkat kembali (Tabel 5)
var kerawanan = harkatJarakAir.add(harkatElevasi).add(harkatTPI).add(harkatNDVI);
Map.addLayer(kerawanan, {min: 1, max: 20, palette: ['green', 'yellow', 'red']}, 'Kerawanan', false);

var harkatKerawanan = kerawanan.where(kerawanan.gt(16), 5)
  .where(kerawanan.gt(12).and(kerawanan.lte(16)), 4)
  .where(kerawanan.gt(8).and(kerawanan.lte(12)), 3)
  .where(kerawanan.gt(4).and(kerawanan.lte(8)), 2)
  .where(kerawanan.lte(4), 1);
Map.addLayer(harkatKerawanan, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat kerawanan', false);
```

> **\[GAMBAR 14 – TANGKAPAN LAYAR PRAKTIKAN] NDVI (Kiri) dan Harkat Vegetasi (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **NDVI** (biru-putih-hijau) dan **Harkat NDVI** (kelas 1–5) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-14-ndvi.png di folder gambar/.
>
> **\[GAMBAR 15 – TANGKAPAN LAYAR PRAKTIKAN] Kerawanan Banjir (Kiri) dan Harkat Kerawanan Banjir (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Kerawanan** (jumlah harkat 4–20) dan **Harkat kerawanan** (kelas 1–5) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-15-kerawanan.png di folder gambar/.

5. **Tuliskan Lesson Learnt**: empat variabel dengan satuan berbeda (meter, meter, indeks tak berdimensi, indeks) dapat dijumlahkan hanya setelah seragam diharkat 1–5; TPI memberi informasi yang tak tergantikan elevasi – dua titik setinggi 12 m bisa berbeda nasib bila satu di punggungan dan satu di cekungan.

**Penjelasan:** Metode penjumlahan harkat setara dengan weighted overlay dengan bobot seragam. Bila suatu variabel dianggap lebih menentukan (misalnya jarak sungai), pengembangan wajar adalah pembobotan: harkatJarakAir.multiply(2).add(...) dengan rentang kelas disesuaikan, atau metode analitik lain (mis. AHP) yang berada di luar cakupan modul ini.

## III.7. Task V: Eksposur, Kerentanan, dan Risiko Banjir

**TASK V: PENDUDUK, WORLDCOVER, PDB/IPM, DAN PETA RISIKO FINAL**

Tahap penutup memindahkan fokus dari “di mana bahayanya” ke “siapa dan apa yang terdampak” serta “seberapa siap mereka”, lalu melebur ketiganya menjadi peta risiko.

**Tabel 6. Harkat Variabel Eksposur Banjir**

| No. | Variabel | Keterangan | Harkat |
| --- | --- | --- | --- |
| 1 | Penduduk | < 10 jiwa | 1 |
|  |  | 10–100 jiwa | 2 |
|  |  | 101–200 jiwa | 3 |
|  |  | 201–300 jiwa | 4 |
|  |  | > 300 jiwa | 5 |
| 2 | Luas lahan terbangun | < 40 m persegi | 1 |
|  |  | 40–60 m persegi | 2 |
|  |  | 61–80 m persegi | 3 |
|  |  | 81–100 m persegi | 4 |
|  |  | > 100 m persegi | 5 |
| 3 | Luas lahan pertanian | < 40 m persegi | 1 |
|  |  | 40–60 m persegi | 2 |
|  |  | 61–80 m persegi | 3 |
|  |  | 81–100 m persegi | 4 |
|  |  | > 100 m persegi | 5 |

**Tabel 7. Harkat Eksposur Banjir**

| Harkat jumlah variabel | Harkat Eksposur Banjir | Keterangan |
| --- | --- | --- |
| < 3 | 1 | Sangat tidak terekspos |
| 3–6 | 2 | Tidak terekspos |
| 7–9 | 3 | Sedang |
| 10–12 | 4 | Terekspos |
| > 12 | 5 | Sangat terekspos |

**Tabel 8. Harkat Variabel Kerentanan Banjir**

| No. | Variabel | Keterangan | Harkat |
| --- | --- | --- | --- |
| 1 | PDB | > 40 juta USD | 1 |
|  |  | 31–40 juta USD | 2 |
|  |  | 21–30 juta USD | 3 |
|  |  | 10–20 juta USD | 4 |
|  |  | < 10 juta USD | 5 |
| 2 | IPM | > 0.85 | 1 |
|  |  | 0.8–0.85 | 2 |
|  |  | 0.75–0.8 | 3 |
|  |  | 0.7–0.75 | 4 |
|  |  | < 0.7 | 5 |

**Tabel 9. Harkat Kerentanan Banjir**

| Harkat jumlah variabel | Harkat Kerentanan Banjir | Keterangan |
| --- | --- | --- |
| < 2 | 1 | Sangat tidak rentan |
| 2–4 | 2 | Tidak rentan |
| 5–6 | 3 | Sedang |
| 7–8 | 4 | Rentan |
| > 8 | 5 | Sangat rentan |

**Tabel 10. Harkat Risiko Banjir**

| Harkat jumlah variabel | Harkat Risiko Banjir | Keterangan |
| --- | --- | --- |
| < 3 | 1 | Sangat tidak berisiko |
| 3–6 | 2 | Tidak berisiko |
| 7–9 | 3 | Sedang |
| 10–12 | 4 | Berisiko |
| > 12 | 5 | Sangat berisiko |

1. Hitung harkat penduduk dari dataset GHSL (ambil epok terbaru dengan sort waktu menurun lalu first()):

```
var penduduk = ee.ImageCollection('JRC/GHSL/P2023A/GHS_POP')
  .sort('system:time_start', false)
  .first().updateMask(bukanAir).clip(roi);
Map.addLayer(penduduk, {min: 0, max: 250, palette: ['black', 'red', 'white']}, 'Penduduk', false);

var harkatPenduduk = penduduk.where(penduduk.gt(300), 5)
  .where(penduduk.gt(200).and(penduduk.lte(300)), 4)
  .where(penduduk.gt(100).and(penduduk.lte(200)), 3)
  .where(penduduk.gt(10).and(penduduk.lte(100)), 2)
  .where(penduduk.lte(10), 1);
Map.addLayer(harkatPenduduk, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat penduduk', false);
```

2. Ambil luas lahan terbangun dan pertanian per piksel dari WorldCover 10 m, ringkas ke 30 m dengan reduceResolution, lalu harkatkan:

```
var wc = ee.ImageCollection('ESA/WorldCover/v200').first().clip(roi).updateMask(bukanAir);

var lahanTerbangun = wc.eq(50);   // kelas 50 = built-up
var pertanian = wc.eq(40);        // kelas 40 = cropland

var area = ee.Image.pixelArea();

// Luas terbangun per piksel 30 m (m persegi)
var lahanTerbangunArea = lahanTerbangun.multiply(area)
  .reduceResolution(ee.Reducer.sum(), true)
  .reproject('EPSG:4326', null, 30);
Map.addLayer(lahanTerbangunArea, {min: 0, max: 100, palette: ['black', 'red', 'white']}, 'Luas lahan terbangun', false);

var harkatLahanTerbangun = lahanTerbangunArea.where(lahanTerbangunArea.gt(100), 5)
  .where(lahanTerbangunArea.gt(80).and(lahanTerbangunArea.lte(100)), 4)
  .where(lahanTerbangunArea.gt(60).and(lahanTerbangunArea.lte(80)), 3)
  .where(lahanTerbangunArea.gt(40).and(lahanTerbangunArea.lte(60)), 2)
  .where(lahanTerbangunArea.lte(40), 1);

// Luas pertanian per piksel 30 m + harkat
var pertanianArea = pertanian.multiply(area)
  .reduceResolution(ee.Reducer.sum(), true)
  .reproject('EPSG:4326', null, 30);

var harkatPertanian = pertanianArea.where(pertanianArea.gt(100), 5)
  .where(pertanianArea.gt(80).and(pertanianArea.lte(100)), 4)
  .where(pertanianArea.gt(60).and(pertanianArea.lte(80)), 3)
  .where(pertanianArea.gt(40).and(pertanianArea.lte(60)), 2)
  .where(pertanianArea.lte(40), 1);
```

**Cara membaca kode (bahasa awam):**

- wc.eq(50) = WorldCover menyimpan kode kelas; 50 berarti built-up (terbangun), 40 berarti cropland (pertanian) – layaknya membaca peta legenda bernomor.
- reduceResolution(ee.Reducer.sum(), true) = lebur 9 piksel kecil 10 m menjadi 1 piksel 30 m dengan cara menjumlahkan isinya; hasilnya “berapa meter persegi terbangun di dalam tiap sel 30 m”.

> **\[GAMBAR 16 – TANGKAPAN LAYAR PRAKTIKAN] Penduduk GHSL (Kiri) dan Harkat Penduduk (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Penduduk** (GHSL) dan **Harkat penduduk** (kelas 1–5) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-16-penduduk.png di folder gambar/.
>
> **\[GAMBAR 17 – TANGKAPAN LAYAR PRAKTIKAN] Luas Lahan Terbangun (Kiri) dan Harkatnya (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Luas lahan terbangun** dan **Harkat lahan terbangun** (kelas 1–5) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-17-terbangun.png di folder gambar/.
>
> **\[GAMBAR 18 – TANGKAPAN LAYAR PRAKTIKAN] Luas Lahan Pertanian (Kiri) dan Harkatnya (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Luas pertanian** dan **Harkat pertanian** (kelas 1–5) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-18-pertanian.png di folder gambar/.

3. Jumlahkan ketiga harkat menjadi eksposur lalu harkat kembali sesuai Tabel 7:

```
var eksposur = harkatPenduduk.add(harkatLahanTerbangun).add(harkatPertanian);
Map.addLayer(eksposur, {min: 1, max: 15, palette: ['green', 'yellow', 'red']}, 'Eksposur', false);

var harkatEksposur = eksposur.where(eksposur.gt(12), 5)
  .where(eksposur.gt(9).and(eksposur.lte(12)), 4)
  .where(eksposur.gt(6).and(eksposur.lte(9)), 3)
  .where(eksposur.gt(3).and(eksposur.lte(6)), 2)
  .where(eksposur.lte(3), 1);
Map.addLayer(harkatEksposur, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat eksposur', false);
```

4. Bangun kerentanan dari PDB dan IPM (band b26 = tahun 2015), jumlahkan, dan harkatkan (Tabel 8–9):

```
// PDB per piksel (USD)
var pdb = ee.Image('projects/sat-io/open-datasets/GRIDDED_HDI_GDP/GDP_PPP_1990_2015_5arcmin_v2')
  .select('b26').clip(roi).updateMask(bukanAir);
Map.addLayer(pdb, {min: 0, max: 1e8, palette: ['black', 'green', 'white']}, 'PDB', false);

var harkatPDB = pdb.where(pdb.gt(40 * 1e6), 1)
  .where(pdb.gt(30 * 1e6).and(pdb.lte(40 * 1e6)), 2)
  .where(pdb.gt(20 * 1e6).and(pdb.lte(30 * 1e6)), 3)
  .where(pdb.gt(10 * 1e6).and(pdb.lte(20 * 1e6)), 4)
  .where(pdb.lte(10 * 1e6), 5);
Map.addLayer(harkatPDB, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat PDB', false);

// IPM (0--1)
var ipm = ee.Image('projects/sat-io/open-datasets/GRIDDED_HDI_GDP/HDI_1990_2015_v2')
  .select('b26').clip(roi).updateMask(bukanAir);
Map.addLayer(ipm, {min: 0.5, max: 1, palette: ['black', 'blue', 'white']}, 'IPM', false);

var harkatIPM = ipm.where(ipm.gt(0.85), 1)
  .where(ipm.gt(0.8).and(ipm.lte(0.85)), 2)
  .where(ipm.gt(0.75).and(ipm.lte(0.8)), 3)
  .where(ipm.gt(0.7).and(ipm.lte(0.75)), 4)
  .where(ipm.lte(0.7), 5);
Map.addLayer(harkatIPM, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat IPM', false);

var kerentanan = harkatPDB.add(harkatIPM);
Map.addLayer(kerentanan, {min: 1, max: 10, palette: ['green', 'yellow', 'red']}, 'Kerentanan', false);

var harkatKerentanan = kerentanan.where(kerentanan.gt(8), 5)
  .where(kerentanan.gt(6).and(kerentanan.lte(8)), 4)
  .where(kerentanan.gt(4).and(kerentanan.lte(6)), 3)
  .where(kerentanan.gt(2).and(kerentanan.lte(4)), 2)
  .where(kerentanan.lte(2), 1);
Map.addLayer(harkatKerentanan, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat kerentanan', false);
```

5. Akhiri dengan peta risiko: jumlahkan harkat kerawanan dan eksposur (aktifkan kerentanan untuk skema tiga komponen penuh), lalu harkatkan (Tabel 10):

```
var risiko = harkatKerawanan.add(harkatEksposur);   // .add(harkatKerentanan);
Map.addLayer(risiko, {min: 1, max: 10, palette: ['green', 'yellow', 'red']}, 'Risiko banjir', false);

var harkatRisiko = risiko.where(risiko.gt(8), 5)
  .where(risiko.gt(6).and(risiko.lte(8)), 4)
  .where(risiko.gt(4).and(risiko.lte(6)), 3)
  .where(risiko.gt(2).and(risiko.lte(4)), 2)
  .where(risiko.lte(2), 1);
Map.addLayer(harkatRisiko, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat risiko', false);
```

> **\[GAMBAR 19 – TANGKAPAN LAYAR PRAKTIKAN] Eksposur Banjir (Kiri) dan Harkat Eksposur (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Eksposur** (jumlah harkat 3–15) dan **Harkat eksposur** (kelas 1–5) lalu sajikan berdampingan. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-19-eksposur.png di folder gambar/.
>
> **\[GAMBAR 20 – TANGKAPAN LAYAR PRAKTIKAN] Risiko Banjir (Kiri) dan Harkat Risiko (Kanan)**
>
> Gambar ini sengaja tidak disertakan pada modul dan **wajib dilengkapi oleh mahasiswa** dari hasil praktikum sendiri. Aktifkan layer **Risiko banjir** dan **Harkat risiko** (kelas 1–5); ini keluaran akhir praktikum – pastikan legenda kelas terbaca jelas. Sertakan konteks antarmuka Code Editor (panel Layers/konsol) pada bingkai tangkapan layar, lalu simpan sebagai modul-gee-20-risiko.png di folder gambar/.

6. **Tuliskan Lesson Learnt**: perhatikan arah harkat PDB dan IPM yang **dibalik** dari variabel fisik – nilai variabel tinggi justru diberi harkat 1, karena kemampuan ekonomi dan manusia yang tinggi menurunkan kerentanan; .add(harkatKerentanan) sengaja dijadikan komentar pada skrip sumber agar dicoba dahulu dua komponen – aktifkan dan jelaskan efeknya terhadap sebaran kelas risiko.

**Penjelasan:** Resolusi data sosial-ekonomi (±5 km untuk PDB/IPM, ±100 m penduduk) jauh lebih kasar daripada variabel fisik (30 m); GEE otomatis menginterpolasi nilai kasar ke grid analisis. Artinya, kerentanan nyaris seragam dalam skala kota kecil dan pembeda utama risiko pada ROI modul adalah kerawanan dan eksposur – kesenjangan resolusi seperti ini penting diungkap dalam laporan profesional, bukan disembunyikan.

## III.8. Kesimpulan Praktikum

**Tabel 11. Panduan Memilih Pendekatan Pemetaan Lahan Terbangun**

| Situasi | Rekomendasi | Alasan |
| --- | --- | --- |
| Tidak ada data latih, wilayah kecil, butuh cepat | Clustering k-means (Task I) | Tanpa label; hasil perlu verifikasi visual dan nomor cluster tidak stabil |
| Butuh konsisten lintas 30+ tahun dan lintas sensor | Indeks + threshold (Task II) | NDBI/MNDWI ternormalisasi lebih stabil lintas sensor; ambangan perlu kalibrasi |
| Latar sangat urban, air sering salah deteksi | MNDWI sebagai penyaring (Task III) | MNDWI lebih tahan latar terbangun daripada NDWI (Xu, 2006) |
| Butuh peta “kapan mulai terbangun” | Nilai-tahun + komposit min (Task III) | Satu peta meringkas seluruh sejarah ekspansi |
| Butuh justifikasi kebijakan multikriteria | Harkat 1–5 bertingkat (Task IV–V) | Transparan dan dapat diaudit; sensitif pada pemilihan ambangan |

Dari seluruh task dapat disimpulkan bahwa: (1) pola dasar GEE – filter, map, reduce, visualize – berlaku pada semua studi kasus, dari satu citra hingga koleksi 35 tahun; (2) clustering menjawab “kelompok apa saja yang ada” tanpa label, sedangkan indeks + threshold menjawab “di mana persisnya kelas tertentu” dengan asumsi yang eksplisit; (3) iterasi lewat map mengubah analisis satu waktu menjadi analisis deret waktu tanpa duplikasi kode; (4) model risiko harkat menggabungkan data fisik dan sosial-ekonomi dalam satu kerangka yang sederhana namun wajib disertai pernyataan asumsi ambangan; dan (5) kualitas keluaran ditentukan oleh kualitas masukan: kalibrasi ambangan, pemilihan epok waktu, dan kesadaran akan perbedaan resolusi antarvariabel.

## III.9. Tugas Praktikum (Mandiri)

Kerjakan pada skrip GEE masing-masing, dokumentasikan tangkapan layar dan penjelasan, dan jadikan bahan diskusi pertemuan berikutnya.

1. **Sensitivitas clustering.** Pada Task I, ubah jumlah kelompok menjadi 5, 10, dan 20 serta ulang pelatihan beberapa kali. Bandingkan luas kelas kandidat lahan terbangun (gunakan reduceRegion dengan ee.Reducer.sum() pada pixelArea() di geometry2) dan jelaskan efek jumlah kelompok serta kestabilan nomor cluster.
2. **Kalibrasi ambangan.** Pada Task II, gunakan inspektur untuk mengambil nilai NDBI pada 5 lokasi yang jelas terbangun dan 5 yang jelas bukan. Tentukan ambangan baru dari data tersebut, bandingkan peta hasilnya dengan ambangan , dan laporkan perubahan luas terbangun (Ha).
3. **Urban sprawl kota lain.** Pindahkan ROI Task III ke satu kota pilihan Anda (misalnya Kota Bandung atau Kabupaten Sleman), tambahkan tahun 2024 pada yearList, dan sajikan peta ekspansi beserta grafik luas. Jelaskan pola ekspansi yang terbaca.
4. **Risiko tiga komponen.** Pada Task V, aktifkan .add(harkatKerentanan) pada perhitungan risiko. Bandingkan peta harkat risiko sebelum dan sesudah, hitung luas tiap kelas risiko (1–5) dengan ee.Reducer.histogram() atau reduceRegion bertingkat, dan diskusikan mengapa komponen kerentanan mengubah (atau tidak mengubah) peringkat risiko di ROI modul.

## III.10. Soal Latihan HOTS: Eksperimen dan Desain Analisis GEE (Kumulatif)

Soal-soal berikut menuntut berpikir tingkat tinggi (HOTS) level C4–C6 dan merangkum seluruh task. Kerjakan mandiri; sertakan skrip, tangkapan layar, dan argumen pada laporan.

**Problem A. Detektif Bit QA \[C4 Analisis · Task II]**

Alih-alih menolak piksel bila salah satu bit menyala, tulis fungsi maskAwanKustom(image) yang hanya menolak piksel bila **minimal dua** dari empat bit (dilated, cirrus, cloud, shadow) menyala. Terapkan pada koleksi 2022 Jabodetabekpunjur, bandingkan jumlah piksel valid hasilnya dengan cloudMask bawaan modul (petunjuk: jumlahkan hasil bitwiseAnd(...).gt(0) lalu uji gte(2)), dan diskusikan trade-off kehilangan piksel versus retensi data.

**Problem B. Duel Indeks Air \[C4 Analisis · Task II]**

Bandingkan NDWI dan MNDWI pada komposit yang sama: hitung luas air (Ha) tiap indeks dengan ambangan 0.1 menggunakan reduceRegion dengan ee.Reducer.sum(), selisihkan, lalu tumpang-tunjukkan peta selisih. Identifikasi tipe tutupan pada wilayah tempat keduanya berbeda pendapat, dan jelaskan mengapa MNDWI unggul di latar terbangun (rujuk Xu, 2006).

**Problem C. Skala TPI \[C5 Evaluasi · Task IV]**

Jalankan TPI dengan radius focalMean 1, 3, 5, dan 9, harkatkan masing-masing, dan hitung luas kelas 5 (paling cekungan) untuk tiap radius. Buat tabel radius–luas, jelaskan arah perubahannya, dan putuskan radius mana yang paling sesuai untuk mendeteksi dataran banjir sungai pada ROI modul beserta alasannya.

**Problem D. Banjir vs Bukan Banjir \[C5 Evaluasi · Task IV–V]**

Lakukan validasi sederhana peta harkat kerawanan: gunakan inspektur untuk mencatat nilai harkat pada minimal 10 titik yang menurut berita/pengalaman diketahui pernah banjir dan 10 titik yang tidak, di dalam ROI (atau ROI kota Anda sendiri). Hitung akurasi sederhana pada ambangan harkat 4 ke atas, lalu usulkan satu perbaikan ambangan variabel yang paling memperbaiki pemisahan kedua kelompok.

**Problem E. Perancang Model Risiko \[C6 Mencipta · Task IV–V]**

Rancang model risiko banjir versi Anda untuk satu kecamatan pilihan: ganti atau tambah minimal satu variabel (misalnya kemiringan lereng dari SRTM: ee.Terrain.slope, atau curah hujan CHIRPS), tetapkan sendiri kelas harkatnya dengan justifikasi literatur atau data, susun bobot bila diperlukan, dan sajikan peta risiko final beserta tabel asumsi lengkap. Nilai tertinggi diberikan pada keterbukaan asumsi dan uji sensitivitas, bukan pada kerumitan model.

# BAGIAN IV. MEDIA DAN MEKANISME PENGUMPULAN

## IV.1. Media Pengumpulan

Media pengumpulan menggunakan Microsoft Teams (MS Teams) yang dapat diakses pada link berikut:

https://teams.microsoft.com

Kemudian masuk ke dalam Tim (Team) khusus untuk mata kuliah Pemrograman Geospasial Berbasis Cloud.

## IV.2. Mekanisme Pengumpulan

Mekanisme proses pengumpulan untuk modul praktikum ini mengikuti tahapan berikut:

1. **Format penamaan berkas:** gunakan format standar berikut.

- **Tabel 12. Standar Penamaan Proyek dan Berkas Pengumpulan Praktikum**

| Kode | Penjelasan |
| --- | --- |
| GEE2026 | Praktikum GEE tahun 2026 |
| 5A/5B | Kelas |
| D4 | Prodi D-4 Sarjana Terapan |
| 2024 | Angkatan |
| ModulGEE | Kode Modul |
| 001 | 3 Digit NIM Terakhir |

- Format berkas: \[GEE2026_5A_D4_2024]\_ModulGEE_001.zip

2. Simpan seluruh skrip tiap task di repositori skrip GEE Anda, kemudian klik **Get Link** pada tiap skrip dan kumpulkan daftar tautannya di laporan (pastikan tautan dapat dilihat penguji).

3. Susun **Laporan Praktikum (.pdf)** yang mencakup:

   - Tangkapan layar (screenshot) peta tiap task beserta panel Layers terlihat.
   - Potongan kode (code snippet) JavaScript beserta penjelasan fungsinya.
   - Analisis hasil (**Lesson Learnt**) untuk tiap task.
   - Jawaban Tugas Praktikum (III.9) dan minimal dua Problem HOTS pilihan (III.10).

4. Kompresi seluruh berkas menjadi satu arsip .zip sesuai format penamaan di atas.

5. Unggah arsip tersebut pada slot Tugas (Assignment) “Pengumpulan Praktikum Intermediate GEE” di Microsoft Teams sebelum batas waktu berakhir.

# BAGIAN V. PEMBAHASAN DAN EVALUASI HASIL PRAKTIKUM

Penilaian pada praktikum berdasarkan kriteria berikut:

**Tabel 13. Rubrik dan Matriks Kriteria Penilaian Evaluasi Praktikum**

| Kriteria Penilaian | Skor ≥ 80 (A) | Skor 70–79.99 (AB/B) | Skor 60–69.99 (BC/C) | Skor < 60 (D/E) |
| --- | --- | --- | --- | --- |
| **Clustering Tutupan Lahan** (20%) | Filter metadata benar, clustering berjalan, pemilihan cluster diverifikasi visual dengan argumen spektral. | Clustering berjalan namun pemilihan cluster tanpa verifikasi. | Clustering berjalan namun filter koleksi keliru. | Clustering gagal berjalan. |
| **Komposit dan Indeks Spektral** (20%) | Cloud masking benar (bit QA dipahami), komposit median dan kedua indeks tepat, ambangan dikalibrasi dengan inspektur. | Komposit dan indeks benar tanpa kalibrasi ambangan. | Indeks benar namun scaling atau penamaan band keliru. | Komposit gagal dibentuk. |
| **Urban Sprawl Multitemporal** (25%) | Koleksi 7 tahun benar lintas sensor, peta ekspansi dan grafik benar, pola ekspansi dianalisis kritis. | Peta ekspansi benar, analisis pola permukaan. | Sebagian tahun gagal komposit atau legenda/grafik keliru. | Iterasi multitemporal gagal berjalan. |
| **Flood Risk Modelling** (25%) | Seluruh harkat variabel dan komponen benar termasuk arah harkat PDB/IPM; asumsi ambangan dibahas. | Peta risiko benar tanpa pembahasan asumsi. | Sebagian variabel keliru harkatnya. | Model risiko gagal dibentuk. |
| **Pelaporan & Lesson Learnt** (10%) | Laporan sangat lengkap: screenshot, analisis kode, lesson learnt mendalam, jawaban tugas benar semua. | Laporan lengkap dengan screenshot dan penjelasan kode standar. | Laporan kurang detail, sebagian lesson learnt tidak dicantumkan. | Tidak mengumpulkan laporan / tidak sesuai format. |

# DAFTAR PUSTAKA

Geosoftware.ID Team. (2025). *Intermediate GEE*. Geosoftware.ID. https://geosoftwareid.com

Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment*, 202, 18–27.

Kaimaris, D., & Patias, P. (2018). Built-up area detection from satellite imagery using high-resolution image indices. *Journal of the Optical Society of America A*, 35(1), 35–48.

Pesaresi, M., & Freire, S. (2016). *GHS Settlement grid following the REGIO model 2014 in application to GHSL Landsat and Sentinel-1 data*. JRC Technical Report, European Commission.

USGS. (2021). *Landsat Collection 2 Level-2 Science Product Guide*. U.S. Geological Survey.

Xu, H. (2006). Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. *International Journal of Remote Sensing*, 27(14), 3025–3033.

Zanaga, D., Van De Kerchove, R., De Keersmaecker, W., dkk. (2021). *ESA WorldCover 10 m 2020 v200*. Zenodo.

Zha, Y., Gao, J., & Ni, S. (2003). Use of normalized difference built-up index in automatically mapping urban areas from TM imagery. *International Journal of Remote Sensing*, 24(3), 583–594.

# LAMPIRAN

## Lampiran A. Catatan Koreksi terhadap E-book Sumber

Modul ini mengadaptasi skrip e-book *Intermediate GEE* (Geosoftware.ID, 2025) dengan perbaikan teknis berikut agar skrip berjalan benar:

1. **Task II (bandMap NDWI):** kamus band pada skrip sumber belum memuat GREEN sehingga expression gagal dijalankan; band GREEN (B3) ditambahkan.
2. **Task IV (penamaan variabel):** skrip sumber menamai komposit median tetapi menggunakannya sebagai image; diseragamkan menjadi image.
3. **Task IV (jarak dari air):** fastDistanceTransform() menghasilkan jarak kuadrat dalam piksel; ditambahkan .sqrt().multiply(30) agar keluaran berupa meter dan ambang harkat 50–200 m bermakna.
4. **Task IV (harkat NDVI):** kelas 5 pada skrip sumber (ndvi.lte(0)) menimpa kelas 4; disesuaikan menjadi ndvi.lte(-0.25) sesuai Tabel 4.
5. **Task III (legenda):** ui.Label(year) menerima angka pada skrip sumber; dikonversi ke String(year).

## Lampiran B. Pengisian Gambar oleh Mahasiswa

Modul ini tidak menyertakan gambar hasil; setiap Gambar 1–20 adalah **slot kosong yang wajib diisi mahasiswa** sebagai bukti pelaksanaan praktikum. Ketentuan:

1. Sumber tangkapan layar adalah Earth Engine Code Editor milik mahasiswa sendiri saat menjalankan task yang bersangkutan (bukan hasil salin dari internet).
2. Ikuti instruksi pada blok \[GAMBAR n] di setiap task: layer yang diaktifkan, area yang dibingkai, dan penyajian berdampingan bila diminta.
3. Setiap tangkapan layar harus memperlihatkan panel Layers (atau konsol untuk grafik) agar penguji dapat memastikan layer yang tampil benar.
4. Simpan berkas dengan nama baku yang tercantum pada tiap blok (contoh: modul-gee-01-clustering.png) pada folder gambar/, lalu rujuk dalam laporan.
5. Gambar yang blur, terpotong, atau tanpa konteks layer akan dianggap tidak lengkap pada penilaian komponen Pelaporan.

## Lampiran C. Glosarium

| Istilah | Penjelasan |
| --- | --- |
| Band (saluran) | Satu lapis data spektral pada citra, misalnya merah atau inframerah dekat |
| Bitwise operation (operasi bit) | Pemeriksaan status bit pada band QA untuk mendeteksi awan/bayangan |
| Cloud masking | Menutup piksel yang teridentifikasi awan/bayangan agar tidak ikut dianalisis |
| Clustering (unsupervised) | Pengelompokan piksel berdasarkan kemiripan spektral tanpa data latih |
| Composite (komposit) | Citra gabungan dari banyak salindia, misalnya lewat median |
| Exposure (eksposur) | Aset/penduduk yang berada di jalur bahaya banjir |
| Harkat | Nilai skor kelas 1–5 pada model risiko multikriteria |
| Hazard (kerawanan) | Bagian wilayah yang secara langsung terkena bahaya banjir |
| Image collection | Kumpulan citra satelit bertanda lokasi dan waktu di katalog GEE |
| Median composite | Komposit yang mengambil nilai tengah tiap piksel; tahan pencilan |
| Multi temporal | Analisis lintas beberapa titik waktu |
| Reduce resolution | Ringkasan nilai dari grid halus ke grid lebih kasar (mis. 10 m ke 30 m) |
| Self masking | Menyembunyikan piksel bernilai nol dari tampilan peta |
| Thresholding | Mengubah nilai kontinu menjadi biner dengan ambangan |
| TPI | Topographic Position Index; posisi elevasi relatif terhadap lingkungan |
| Vulnerability (kerentanan) | Kemampuan bertahan/memulihkan diri pihak yang terdampak |
