# Todo Praktikum Intermediate Google Earth Engine

Daftar kerja ini disusun dari `modul-intermediete-gee.md`. Setiap butir berisi langkah dan alasannya, supaya jelas apa yang dikerjakan dan kenapa itu perlu.

Blok kode disalin apa adanya dari modul pada langkah yang membutuhkannya. Tugas Mandiri dan Soal HOTS tidak punya kode di modul, jadi kodenya ditulis sendiri.

Bobot penilaian (Tabel 13): Clustering 20%, Komposit & Indeks 20%, Urban Sprawl 25%, Flood Risk 25%, Pelaporan 10%.

---

## Tautan

| Keperluan | Tautan |
| --- | --- |
| Earth Engine Code Editor | https://code.earthengine.google.com |
| Registrasi Earth Engine (non-komersial) | https://code.earthengine.google.com/register |
| Aktifkan Earth Engine API di Google Cloud Console (perlu login) | https://console.cloud.google.com/apis/library/earthengine.googleapis.com |
| Panduan Earth Engine | https://developers.google.com/earth-engine/guides |
| Dokumentasi API (semua fungsi `ee.*`) | https://developers.google.com/earth-engine/apidocs |
| Landsat 9 Level-2 (`LANDSAT/LC09/C02/T1_L2`) | https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2 |
| Landsat 8 Level-2 (`LANDSAT/LC08/C02/T1_L2`) | https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2 |
| Landsat 7 Level-2 (`LANDSAT/LE07/C02/T1_L2`) | https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_L2 |
| Landsat 5 Level-2 (`LANDSAT/LT05/C02/T1_L2`) | https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2 |
| Landsat 4 Level-2 (`LANDSAT/LT04/C02/T1_L2`) | https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT04_C02_T1_L2 |
| SRTM (`USGS/SRTMGL1_003`) | https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003 |
| GHSL Population (`JRC/GHSL/P2023A/GHS_POP`) | https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_POP |
| ESA WorldCover v200 (`ESA/WorldCover/v200`) | https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200 |
| GDP PPP dan HDI gridded (`projects/sat-io/open-datasets/GRIDDED_HDI_GDP/...`) | https://gee-community-catalog.org/projects/gridded_gdp_hdi/ (halaman ini mendokumentasikan versi 3.0; aset versi 2 yang dipakai modul tetap bisa dibaca, sudah diuji) |
| CHIRPS Daily (opsional, Problem E) | https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY |
| `ee.Clusterer.wekaKMeans` | https://developers.google.com/earth-engine/apidocs/ee-clusterer-wekakmeans |
| `ee.Image.reduceRegion` | https://developers.google.com/earth-engine/apidocs/ee-image-reduceregion |
| `ee.Reducer.histogram` | https://developers.google.com/earth-engine/apidocs/ee-reducer-histogram |
| `ee.Image.focalMean` | https://developers.google.com/earth-engine/apidocs/ee-image-focalmean |
| `ee.Image.fastDistanceTransform` | https://developers.google.com/earth-engine/apidocs/ee-image-fastdistancetransform |
| `ee.Image.reduceResolution` | https://developers.google.com/earth-engine/apidocs/ee-image-reduceresolution |
| `ee.Terrain.slope` (opsional, Problem E) | https://developers.google.com/earth-engine/apidocs/ee-terrain-slope |
| Xu (2006), MNDWI (rujukan Problem B; DOI cocok dengan daftar pustaka modul, halaman penerbit memakai verifikasi anti-bot) | https://doi.org/10.1080/01431160600589179 |
| Microsoft Teams (pengumpulan) | https://teams.microsoft.com |
| Materi rujukan modul (E-book *Intermediate GEE*, Geosoftware.ID) | https://geosoftwareid.com |

---

## 0. Persiapan

- [v] **Daftar dan masuk Earth Engine Code Editor** di [code.earthengine.google.com](https://code.earthengine.google.com)
  - Akun Google harus sudah disetujui GEE. Tanpa ini tidak ada task yang bisa dijalankan.
- [v] **Uji koneksi dengan skrip uji koleksi** (pengganti skrip pembuka modul)
  - Skrip pembuka di modul memakai satu ID scene (`LC09_122065_20220119`) yang tidak ditemukan di katalog, jadi bukan ukuran akun bermasalah. Skrip ini memfilter koleksi, sehingga tidak bergantung pada satu scene.
  - Kalau konsol menampilkan jumlah citra dan daftar band, akun, project, dan katalog sudah beres. Kalau muncul error izin atau "not registered", selesaikan [registrasi project Earth Engine](https://code.earthengine.google.com/register) dan aktifkan [Earth Engine API](https://console.cloud.google.com/apis/library/earthengine.googleapis.com) di Google Cloud Console.

  ```js
  var koleksi = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')
    .filterDate('2022-01-01', '2022-03-01')
    .limit(1);
  print('Jumlah citra:', koleksi.size());
  print('Band citra uji:', koleksi.first().bandNames());
  ```
- [v] **Buat repository skrip `praktikum-gee`** di [Code Editor](https://code.earthengine.google.com), simpan tiap task sebagai `task1.js` sampai `task5.js`
  - Tautan *Get Link* tiap skrip nanti wajib masuk laporan, jadi skrip harus rapi dan terpisah per task.
  - Sudah dibuat: `users/vermilion10/praktikum-gee`, berisi `task0-uji-koneksi` (skrip uji koneksi dan uji aset GDP/HDI).
- [ ] **Pahami ketergantungan antar skrip**, karena kode Task III–V memakai variabel dari task sebelumnya
  - `task1.js` berdiri sendiri.
  - `task2.js` mendefinisikan `roi`, `l8`, `cloudMask`, `median`, `bandMap`.
  - `task3.js` butuh `roi` dan `l8` dari Task II.
  - `task4.js` memakai ROI Batanghari yang baru dan butuh `cloudMask` dari Task II.
  - `task5.js` = isi `task4.js` + kode Task V (butuh `roi`, `bukanAir`, `harkatKerawanan`).
- [v] **Siapkan folder `gambar/`** untuk 20 tangkapan layar, dengan nama berpola `modul-gee-NN-nama.png` (contoh: `modul-gee-01-clustering.png`)
  - Modul tidak menyertakan gambar. Semua Gambar 1–20 adalah slot kosong yang harus diisi sendiri (Lampiran B).
- [ ] **Catat aturan tangkapan layar** yang berlaku untuk semua gambar
  - Panel Layers (atau konsol untuk grafik) harus terlihat, tidak blur, tidak terpotong. Gambar yang melanggar dianggap tidak lengkap di komponen Pelaporan.

---

## 1. Task I: Filter Citra dan Clustering (Purwodadi), bobot 20%

- [v] **Langkah 1: Panggil Landsat 9, buat titik kajian di Purwodadi, saring dengan `filterBounds`, metadata tutupan awan, dan urutkan**
  - Menyaring dulu supaya server hanya menghitung scene yang relevan. Ini juga syarat nilai A (filter metadata benar).
  - Dataset: [Landsat 9 Level-2](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2).

  ```js
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
- [v] **Langkah 2: Tampilkan true color, lalu jalankan `ee.Clusterer.wekaKMeans(15)` pada wilayah kecil**
  - K-means mengelompokkan piksel berdasarkan kemiripan spektral tanpa data latih. Modelnya dilatih dari 500 piksel contoh, lalu diterapkan ke seluruh citra.
  - Dokumentasi: [`ee.Clusterer.wekaKMeans`](https://developers.google.com/earth-engine/apidocs/ee-clusterer-wekakmeans).
  - Angka cluster di `hasil.eq(2).or(hasil.eq(3))` hanyalah contoh dan berubah tiap dijalankan. Tampilkan dulu cluster mentahnya (tambahan, bukan dari modul): `Map.addLayer(hasil.randomVisualizer(), {}, 'Cluster mentah');`, lalu ganti angkanya sesuai cluster yang tampak sebagai bangunan.

  ```js
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
- [v] **Verifikasi visual: tentukan cluster mana yang lahan terbangun** dengan membandingkan peta cluster dan citra asli
  - Komputer tidak tahu cluster mana yang bangunan. Nilai A mensyaratkan pemilihan cluster diverifikasi dan dijelaskan dengan argumen spektral.
  - **Hasil (9 Oktober 2026, skrip `task1`)**: citra terpilih punya `CLOUD_COVER_LAND` 0,06. Cluster 2 dan 3 bawaan modul tidak cocok di run ini: cluster 2 justru bervegetasi. Dipilih **cluster 9 dan 11** berdasarkan statistik di poligon kajian dan cek visual:

    | Cluster | Rata-rata NDBI | Rata-rata NDVI | Piksel | Hasil cek visual |
    | --- | --- | --- | --- | --- |
    | 2 (bawaan modul) | −0,163 | 0,359 | 2243 | vegetasi, bukan bangunan |
    | 3 (bawaan modul) | 0,015 | 0,169 | 3012 | bercak besar di sawah atau lahan kering |
    | 9 (dipilih) | 0,058 | 0,110 | 323 | titik terang di dalam kota (atap) |
    | 10 | 0,043 | 0,137 | 2496 | campuran kota dan lahan terbuka, tidak dipakai |
    | 11 (dipilih) | 0,031 | 0,154 | 5205 | mengumpul di pusat kota dan permukiman |
    | 5 | 0,010 | 0,200 | 4323 | tanah terbuka di sawah |

  - Argumen spektral untuk laporan: atap dan aspal memantulkan SWIR lebih tinggi daripada NIR (NDBI positif) dan hampir tanpa vegetasi (NDVI rendah). Tanah kering juga ber-NDBI positif, jadi cluster yang bercaknya ada di sawah dibuang meski angkanya mirip.
  - Catatan lokasi: poligon kajian modul (111,57–111,62 BT; 7,13–7,18 LS) jatuh di **Cepu**, di tepi Bengawan Solo (perbatasan Jawa Tengah dan Jawa Timur), bukan Purwodadi. Label peta di Code Editor menunjukkan Cepu. Sebutkan ini di laporan.
- [v] **Tangkapan layar Gambar 1**: layer `Bangunan` (merah) di atas `Data paling bersih`, dibingkai pada poligon kajian
  - Tersimpan di `gambar/modul-gee-01-clustering.png` (layer `Bangunan` di atas `Data paling bersih`, panel Layers, editor, dan konsol terlihat).
- [ ] **Tulis Lesson Learnt Task I**
  - Poin yang perlu muncul: clustering tidak butuh label tapi penafsiran tetap manual, filter metadata mempercepat proses, nomor cluster bisa berubah tiap dijalankan ulang.
  - Draf (belum dipoles, sunting dulu sebelum masuk laporan):

    Clustering k-means mengelompokkan piksel tanpa data latih, tapi nomor cluster hasilnya tidak punya arti apa apa sebelum dicocokan ke citra. modul memakai `hasil.eq(2).or(hasil.eq(3))` sebagai lahan terbangun, sementara di run ini cluster 2 punya rata-rata NDBI −0,163 dan NDVI 0,359, jadi isinya vegetasi. cluster 3 juga meleset, bercaknya jatuh di sawah dan lahan kering. Kalau nomor dari modul dipakai begitu saja, layer `Bangunan` terlihat masuk akal sekilas walau sebagian merahnya bukan bangunan

    Penggantinya dipilih dari dua arah. Statistik per cluster di `geometry2` memberi kandidat dengan NDBI positif dan NDVI rendah (cluster 9, 10, 11, dan 3), lalu tiap kandidat ditampilkan dengan warna berbeda di atas `Data paling bersih`. cluster 11 mengumpul di pusat kota dan permukman sepanjang jalan, cluster 9 berupa titik terang di dalam kota, sementara cluster 10 dan 3 tersebar juga di lahan terbuka. Yang dipakai akhirnya cluster 9 dan 11.

    Tanah kering ikut punya NDBI positif karena pantulan SWIR-nya tinggi, jadi NDBI saja tidak cukup memisahkan atap dari lahan terbuka. pemeriksaan visual tetap perlu, dan kalau hasilnya mau dipakai lebih jauh clustering sebaiknya digabung dengan indeks lain seperti NDWI atau dengan data latih

    `filterBounds`, `filterMetadata('CLOUD_COVER_LAND', 'less_than', 50)`, dan `sort` bekerja di metadata, belum menyentuh piksel. Citra pertama sesudah sort sudah yang paling bersih dengan `CLOUD_COVER_LAND` 0,06, jadi `first()` langsung mengambil citra terbaik tanpa memeriksa citra satu satu.

    Lokasi juga perlu dicek sendiri. Titik filter di modul ada di sekitar 112,06 BT, sementara poligon kajiannya sekitar 58 km ke barat daya, di Cepu tepi Bengawan Solo, bukan di Purwodadi seperti judul task. label peta di Code Editor yang menunjukkan ini, jadi nama lokasi di laporan mengikuti peta, bukan judul modul

## 2. Task II: Cloud Masking, Komposit Median, NDBI/NDWI (Jabodetabekpunjur), bobot 20%

- [v] **Langkah 1: Tentukan ROI Jabodetabekpunjur, saring Landsat 8 sepanjang 2022**
  - Satu scene jarang bersih penuh, jadi diperlukan banyak scene dalam setahun untuk digabung.
  - Dataset: [Landsat 8 Level-2](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2).

  ```js
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
- [v] **Langkah 2: Tulis fungsi cloud mask QA_PIXEL (bitwiseAnd + `updateMask`), scaling reflektansi, dan penyeragaman nama band ke B2–B7**
  - Bit QA menandai awan, bayangan, cirrus. Penamaan generik membuat rumus indeks berlaku lintas sensor, ini dipakai lagi di Task III.
  - Blok ini juga sudah memuat komposit `median()` dan layer `Image` untuk Gambar 2.

  ```js
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
- [v] **Buat komposit `median()`**
  - Median kebal terhadap sisa awan dan outlier, selama lebih dari separuh citra bersih.
  - Kodenya sudah ada di blok kode Langkah 2 di atas.
- [v] **Tangkapan layar Gambar 2**: komposit NIR-SWIR-Biru 2022, seluruh ROI terbingkai
  - Tersimpan di `gambar/modul-gee-02-komposit.png` (hanya layer `Image`, seluruh ROI terbingkai).
- [v] **Langkah 3: Hitung NDBI dan NDWI dengan `expression()`**
  - Keduanya rasio ternormalisasi. NDBI menonjolkan atap dan aspal, NDWI menonjolkan air.
  - Blok ini juga sudah memuat threshold (`air`, `bangunan`) untuk Gambar 3 dan 4. Tambahkan `Map.addLayer` terpisah kalau ingin menyajikan NDBI dan NDWI berdampingan.

  ```js
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
- [v] **Terapkan threshold dan `selfMask()`** untuk memisahkan air dan terbangun
  - Mengubah indeks kontinu menjadi peta biner yang bisa dihitung luasnya.
  - Kodenya sudah ada di blok kode Langkah 3 di atas.
- [v] **Kalibrasi ambangan dengan Inspector**: baca nilai NDBI/NDWI pada objek yang jelas terbangun dan jelas air
  - Ambangan bawaan hanya titik awal. Kalibrasi adalah pembeda nilai A dan B pada rubrik.
  - Hasil kalibrasi (9 Oktober 2026), memakai ESA WorldCover v200 sebagai acuan, skala 60 m di seluruh ROI. Persentase piksel tiap kelas yang lolos ambang:

    | kelas WorldCover | NDBI > −0,15 | NDBI > −0,10 | NDBI > −0,05 | NDBI > 0 | NDWI > 0,1 |
    | --- | --- | --- | --- | --- | --- |
    | 10 pohon | 13% | 7% | 3% | 1% | 0% |
    | 30 rumput | 34% | 18% | 8% | 3% | 0% |
    | 40 pertanian | 14% | 6% | 2% | 0% | 0% |
    | 50 terbangun | 89% | 78% | 63% | 46% | 0% |
    | 60 lahan terbuka | 80% | 68% | 46% | 19% | 0% |
    | 80 air | 2% | 1% | 1% | 0% | 86% |

    | ambang NDBI | presisi (yang lolos memang kelas 50) | recall kelas 50 |
    | --- | --- | --- |
    | > −0,15 | 77% | 89% |
    | > −0,10 (modul) | 85% | 78% |
    | > −0,05 | 91% | 63% |
    | > 0 | 96% | 46% |

  - Keputusan: ambang modul (NDBI > −0,1, NDWI > 0,1) dipertahankan karena paling seimbang antara presisi dan recall. Kode `task2` tidak diubah. Lahan terbuka (kelas 60) paling sering tertukar dengan bangunan.
  - Catatan: WorldCover sendiri hasil klasifikasi (tahun 2021), jadi angka di atas perkiraan, bukan kebenaran lapangan.
  - Cek Inspector (9 Oktober 2026, sekitar Ragunan dan Jakarta Selatan). Tiap titik dicek ulang di basemap Satellite, dan hanya titik yang jelas yang dipakai:

    | titik | koordinat | di citra satelit | NDBI | NDWI | lolos `Bangunan`? |
    | --- | --- | --- | --- | --- | --- |
    | T1 | 106.86540, −6.28235 | permukiman padat | 0,076 | −0,391 | ya |
    | T2 | 106.85682, −6.33354 | permukiman padat | 0,139 | −0,257 | ya |
    | T3 | 106.84223, −6.31733 | permukiman padat tepi sungai | 0,103 | −0,356 | ya |
    | T4 | 106.91573, −6.29348 | permukiman padat (Komp. Ardhini) | 0,076 | −0,312 | ya |
    | T5 | 106.86234, −6.28717 | permukiman padat | 0,151 | −0,206 | ya |
    | V1 | 106.82163, −6.31136 | hutan Ragunan | −0,343 | −0,682 | tidak |
    | V2 | 106.81994, −6.30935 | hutan Ragunan | −0,336 | −0,702 | tidak |
    | V3 | 106.91089, −6.32501 | taman hijau besar | −0,398 | −0,685 | tidak |
    | V4 | 106.88929, −6.28427 | lapangan golf | −0,299 | −0,469 | tidak |
    | V5 | 106.90818, −6.32812 | tepi taman berumput | −0,107 | −0,551 | tidak (nyaris) |

  - Kesepuluh titik terpisah benar dengan ambang −0,1, jadi ambang modul dipertahankan. V5 hanya 0,007 di bawah ambang, sejalan dengan 18% piksel rumput WorldCover yang lolos.
  - Titik yang dibuang karena tidak tegas di citra satelit: permukiman jarang bercampur pohon (NDBI −0,268 dan −0,176, tidak lolos), lahan campuran (0,010 dan −0,162), dan Situ Gintung (106.76275, −6.30453) yang tampak hijau di basemap dengan NDWI hanya 0,075, jadi tidak terdeteksi sebagai `Air`.
  - Data ini bisa dipakai ulang untuk Tugas Mandiri 2.
- [v] **Tangkapan layar Gambar 3**: NDBI (kiri) dan NDWI (kanan), area sama
  - Tersimpan di `gambar/modul-gee-03-ndbi-ndwi.png` (NDBI kiri, NDWI kanan, area dan zoom sama). Laut tampak merah di NDBI, artinya NDBI air juga positif, jadi NDBI harus dipasangkan dengan masker air.
- [v] **Tangkapan layar Gambar 4**: layer `Air` (biru) dan `Bangunan` (merah) bersamaan, pilih area pesisir atau pusat kota
  - Tersimpan di `gambar/modul-gee-04-bangunan-air.png` (pesisir Jakarta, `Air` dan `Bangunan` di atas `Image`).
- [ ] **Tulis Lesson Learnt Task II**
  - Poin: ambangan harus dikalibrasi per wilayah, NDBI dan NDWI dipakai berpasangan, kenapa median dan bukan mean.
  - Draf (belum dipoles, sunting dulu sebelum masuk laporan):

    Ambang −0,1 untuk NDBI dan 0,1 untuk NDWI di modul ternyata tidak perlu diganti, tapi itu baru terlihat sesudah dicek dua cara. Dibandingkn dengan ESA WorldCover, NDBI > −0,1 menangkap 78% piksel terbangun dengan presisi 85%. menaikkan ambang ke −0,05 memang membuat presisi naik ke 91%, tapi recall turun ke 63%, jadi lebih banyak permukiman yang hilang dari peta

    Cek Inspector di sekitar Ragunan memberi hasil yang sejalan. lima titik permukiman padat ada di NDBI 0,076 sampai 0,151 dan lima titik hutan, taman, dan lapangan golf ada di −0,398 sampai −0,107. Titik terakhir itu tepi taman berumput yang hanya 0,007 di bawah ambang, jadi rumput dan lahan terbuka adalah kelas yang paling mudah tertukar dengan bangunan.

    Yang tidak terduga justru di tahap memilih titik. Warna cyan pada komposit NIR-SWIR-Biru tidak selalu permukiman padat, dan beberapa titik yang dikira permukiman ternyata rumah jarang bercampur pohon dengan NDBI −0,27 dan −0,18. Piksel 30 m di area seperti itu sudah campuran, jadi titik kalibrasi harus dicek dulu di basemap Satellite sebelum nilainya dipakai

    NDBI tidak bisa dipakai sendiri karena laut juga punya NDBI positif, terlihat merah di layer NDBI, dan masker `air.eq(0)` yang membuangnya dari peta `Bangunan`. Situ Gintung punya NDWI hanya 0,075 dan tidak masuk layer `Air`, kemungkinan karena permukaannya tertutup vegtasi

    Komposit `median()` dari setahun citra Landsat 8 membuat seluruh ROI tampil tanpa lubang awan walau satu citra saja jarang bebas awan. median dipilih karena sisa awan yang lolos masker hanya muncul di sebagian kecil citra, jadi kalah dari nilai tengah, sementara mean masih ikut tertarik

## 3. Task III: Multitemporal, Komposit Minimum, Legenda, Grafik, bobot 25%

- [v] **Langkah 1: Latihan iterasi JavaScript (`for` di sisi klien) dan bedakan dari `map` di sisi server**
  - Dua mekanisme ini dipakai bergantian di langkah berikutnya.

  ```js
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
- [v] **Langkah 2: Siapkan 5 koleksi Landsat (4, 5, 7, 8, 9), dua varian cloud mask (TM dan OLI), dan fungsi komposit**
  - Penamaan band berbeda antar sensor (SWIR: `SR_B5` di TM/ETM+, `SR_B6` di OLI). Kalau keliru, sebagian tahun gagal dikomposit.
  - Dataset: [Landsat 4](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT04_C02_T1_L2), [Landsat 5](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2), [Landsat 7](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_L2), [Landsat 8](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2), [Landsat 9](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2).
  - **Prasyarat**: kode ini memakai `roi` dan `l8` dari Task II. `l8` tidak didefinisikan di blok ini, jadi kalau `task3.js` skrip baru, tambahkan di atasnya: `var l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2');` dan salin `roi` dari Task II.

  ```js
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
- [v] **Langkah 3: Petakan `yearList` (1990, 1995, 2000, 2005, 2010, 2015, 2020) menjadi koleksi lahan terbangun tahunan**
  - Satu fungsi lewat `map` menggantikan tujuh skrip salinan-tempel.

  ```js
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
- [v] **Tangkapan layar Gambar 5**: `Landsat_1990` (kiri) dan `Landsat_2020` (kanan)
  - Tersimpan di `gambar/modul-gee-05-lansat-1990-2020.png` (nama mengikuti modul, termasuk salah ketik "lansat").
- [v] **Tangkapan layar Gambar 6**: `Built-up_1990` (kiri) dan `Built-up_2020` (kanan)
  - Tersimpan di `gambar/modul-gee-06-built-1990-2020.png`.
- [v] **Langkah 4: Bangun peta urban sprawl dengan `min()` pada peta bernilai tahun, tambahkan legenda `ui.Panel` (pakai `String(year)`)**
  - `min()` mengambil tahun paling awal sebuah piksel terdeteksi terbangun, jadi satu peta merangkum seluruh sejarah ekspansi.
  - Blok ini sudah memuat legenda dan grafik luas (`areaChart`) untuk Gambar 7 dan 8.

  ```js
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
- [v] **Buat grafik luas (`ui.Chart`, satuan Ha)** dan `print(areaChart)`
  - Memberi angka untuk melengkapi peta.
  - Kodenya sudah ada di blok kode Langkah 4 di atas.
  - **Bug di kode modul (sudah diperbaiki di `task3`)**: `built.multiply(ee.Image.pixelArea().multiply(0.0001))` mengalikan luas dengan nilai piksel `built`, yaitu **tahun** (1990 dst.), jadi luasnya sekitar 2000 kali terlalu besar (versi modul: 143 juta Ha untuk 1990, padahal seluruh ROI hanya sekitar 600 ribu Ha). Diganti menjadi `built.gt(0).multiply(...)`. Sumbu X juga diberi `format: '####'` supaya tahun tidak tertulis "1,990".
  - Hasil setelah perbaikan (9 Oktober 2026):

    | tahun | luas terbangun (Ha) | jumlah citra di koleksi | sensor |
    | --- | --- | --- | --- |
    | 1990 | 72.060 | 21 | Landsat 4/5/7 (TM/ETM+) |
    | 1995 | 84.916 | 45 | Landsat 4/5/7 |
    | 2000 | 142.223 | 47 | Landsat 4/5/7 |
    | 2005 | 132.575 | 69 | Landsat 4/5/7 |
    | 2010 | 132.175 | 31 | Landsat 4/5/7 |
    | 2015 | 235.512 | 41 | Landsat 8/9 (OLI) |
    | 2020 | 180.747 | 45 | Landsat 8/9 |

  - Grafiknya **tidak selalu naik** seperti asumsi modul: turun sedikit di 2005 dan 2010, lalu turun sekitar 23% dari 2015 ke 2020. Ini bahan untuk analisis kritis di Lesson Learnt (nilai A rubrik). Kemungkinan penyebab yang perlu dibahas, belum diuji: lompatan sensor TM ke OLI di 2015, kerusakan SLC Landsat 7 sejak 2003 yang memengaruhi komposit 2005 dan 2010, beda musim atau kelembapan antartahun, dan ambang NDBI −0,1 yang sama untuk semua sensor.
- [v] **Tangkapan layar Gambar 7**: `Urban_expansion` dengan legenda, seluruh ROI terlihat
  - Tersimpan di `gambar/modul-gee-07-urban-sprawl.png` (seluruh ROI dan legenda terlihat).
  - Untuk analisis: pesisir timur laut (sekitar Muara Gembong) ikut berwarna 1990, kemungkinan tambak atau sawah yang terdeteksi sebagai bangunan pada citra TM. Ada juga garis tegak di tengah ROI tempat kepadatan warna berubah, kemungkinan batas jalur (path) Landsat.
- [v] **Tangkapan layar Gambar 8**: grafik "Urban area (Ha)" dengan judul dan sumbu terbaca
  - Tersimpan di `gambar/modul-gee-08-grafik.png`, diambil sesudah bug luas diperbaiki (lihat Langkah 4).
- [ ] **Tulis Lesson Learnt Task III**, termasuk analisis pola ekspansi
  - Nilai A butuh analisis kritis, bukan sekadar deskripsi. Diskusikan juga artefak seperti piksel yang "hilang" di tahun berikutnya.
  - Draf (belum dipoles, sunting dulu sebelum masuk laporan):

    Satu fungsi di dalam `yearList.map` cukup untuk membuat tujuh komposit dari lima satelit, dan pilihan sensornya ditentukan `year < 2014` di sisi klien. Bagian yang paling menyita waktu justru bukan iterasinya, tapi memastikan nama band TM dan OLI sudah disamakan ke B2 sampai B7 sebelm rumus NDBI dan MNDWI dipakai

    Trik nilai tahun di piksel `built` lalu `min()` lintas tahun membuat satu peta merangkum seluruh sejarah ekspansi. Di Gambar 7 pusat Jakarta berwarna 1990, lalu warnanya bergeser ke 2010 dan 2015 di Tangerang Selatan, Depok, dan Bekasi. pesisir timur laut di sekitar Muara Gembong ikut berwarna 1990, kemungkinan tambak atau sawah yang terbaca sebagai bangunan di citra TM, jadi bagian itu tidak bisa dibaca sebagai kota lama

    Trik yang sama menimbulkan bug di kode modul. Band luas dihitung dengan `built.multiply(...)`, padahal nilai piksel `built` adalah tahun, jadi luas tiap piksel terkali sekitar 2000. Versi modul memberi 143 juta Ha untuk 1990 sementara seluruh ROI hanya sekitar 600 ribu Ha. sesudah diganti `built.gt(0)` hasilnya 72.060 Ha. Angka yang tidak masuk akal seperti ini baru terlihat karena dibandingkan dengan luas ROI, bukan dari bentuk grafiknya, karena bentuk grafiknya sama persis

    Grafik sesudah perbaikan tidak selalu naik. Luas turun sedikit di 2005 dan 2010, lalu turun dari 235.512 Ha di 2015 ke 180.747 Ha di 2020. Kota tidak menyusut sebesar itu dalam lima tahun, jadi penurunannya lebih mungkin berasal dari data: pergantian sensor TM ke OLI di 2015, citra Landsat 7 sesudah kerusakan SLC tahun 2003 yang ikut masuk komposit 2005 dan 2010, beda musim antartahn, dan ambang NDBI −0,1 yang dipakai sama untuk semua sensor. Belum ada yang diuji satu satu, jadi ini dicatat sebagai dugaan

    Peta tahunan juga memperlihatkan garis tegak di tengah ROI tempat kepadatan warnanya berubah, kemungkinan batas dua jalur Landsat. komposit median tidak sepenuhnya menghapus beda antarjalur

## 4. Task IV: Kerawanan Banjir / Hazard (Batanghari, Jambi), bobot 25% (bersama Task V)

- [v] **Langkah 1: Buat komposit Landsat 8 2022 pada ROI Batanghari** (resep sama dengan Task II)
  - Memakai ulang resep yang sudah teruji.
  - **Prasyarat**: fungsi `cloudMask` dari Task II harus disalin ke skrip ini (modul menyebutnya "identik Task II"). Kode di bawah memakai `cloudMask` tetapi tidak mendefinisikannya.

  ```js
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
- [v] **Tangkapan layar Gambar 9**: komposit daerah kajian, jalur sungai terlihat
  - Tersimpan di `gambar/modul-gee-09-komposit-jambi.png`.
- [v] **Langkah 2: Deteksi air dengan NDWI, hitung jarak ke air dengan `fastDistanceTransform`, lalu harkatkan (Tabel 4)**
  - Hasilnya jarak kuadrat dalam piksel, jadi harus `.sqrt().multiply(30)` agar menjadi meter. Tanpa ini, ambang 50–200 m tidak bermakna.
  - Dokumentasi: [`fastDistanceTransform`](https://developers.google.com/earth-engine/apidocs/ee-image-fastdistancetransform).
  - Skrip `task4` menambahkan satu baris `Map.addLayer(ndwi, ...)` karena Gambar 10 meminta layer `NDWI`, sementara kode modul hanya menambahkan layer `Air`.
  - Danau tapal kuda dan rawa gelap di utara sungai tidak masuk layer `Air` (NDWI ≤ 0,1), jadi jarak dan harkatnya dihitung seolah daratan.

  ```js
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
- [v] **Tangkapan layar Gambar 10**: NDWI (kiri) dan `Air` (kanan)
  - Tersimpan di `gambar/modul-gee-10-ndwi-air.png`.
- [v] **Tangkapan layar Gambar 11**: `Jarak dari air` (kiri) dan `Harkat jarak dari air` (kanan)
  - Tersimpan di `gambar/modul-gee-11-jarak.png`.
- [v] **Langkah 3: Elevasi SRTM dan TPI (`focalMean`), masing-masing diharkatkan**
  - TPI memberi informasi cekungan atau punggungan yang tidak bisa digantikan elevasi. Dua titik setinggi 12 m bisa berbeda bahaya.
  - Dataset: [SRTM](https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003). Dokumentasi: [`focalMean`](https://developers.google.com/earth-engine/apidocs/ee-image-focalmean).

  ```js
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
- [v] **Tangkapan layar Gambar 12**: `Elevasi` dan `Harkat elevasi`
  - Tersimpan di `gambar/modul-gee-12-elevasi.png`.
- [v] **Tangkapan layar Gambar 13**: `TPI` dan `Harkat TPI`
  - Tersimpan di `gambar/modul-gee-13-tpi.png`.
- [v] **Langkah 4: NDVI + harkat vegetasi, jumlahkan keempat harkat, harkatkan ulang jadi kelas 1–5 (Tabel 5)**
  - Harkat NDVI kelas 5 harus `ndvi.lte(-0.25)` (koreksi Lampiran A), kalau tidak akan menimpa kelas 4. Penjumlahan hanya sah setelah semua variabel diseragamkan ke skala 1–5.
  - Sebaran kelas di ROI (9 Oktober 2026, skala 30 m):

    | layer | kelas 1 | kelas 2 | kelas 3 | kelas 4 | kelas 5 |
    | --- | --- | --- | --- | --- | --- |
    | harkat jarak air | 93,6% | 1,5% | 1,8% | 1,8% | 1,2% |
    | harkat elevasi | 45,2% | 16,8% | 20,7% | 16,1% | 1,2% |
    | harkat TPI | 49,1% | 8,2% | 6,7% | 6,2% | 29,8% |
    | harkat NDVI | 83,9% | 12,9% | 2,7% | 0,5% | 0,0% |
    | harkat kerawanan | 20,0% | 52,6% | 25,1% | 1,8% | 0,4% |

  - Harkat TPI terbelah ke kelas 1 dan 5 dan tampak seperti bintik acak di Gambar 13. SRTM bernilai meter bulat (di ROI −11 sampai 85 m), sementara ambang TPI modul berselisih 0,25 m, jadi kelas 2–4 hampir tidak terisi. Ini bahan untuk Problem C (skala TPI).
  - Kode dan Tabel 5 tidak cocok: kode memberi kelas 1 untuk jumlah ≤ 4, Tabel 5 memberi kelas 1 untuk < 4 dan kelas 2 untuk 4–8. Jumlah minimum empat harkat adalah 4, jadi kelas 1 versi tabel tidak mungkin terisi, dan 20% piksel "kelas 1" di kode menurut tabel termasuk kelas 2. Kode tidak diubah; sebutkan di laporan.

  ```js
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
- [v] **Tangkapan layar Gambar 14**: `NDVI` dan `Harkat NDVI`
  - Tersimpan di `gambar/modul-gee-14-ndvi.png`.
- [v] **Tangkapan layar Gambar 15**: `Kerawanan` (jumlah 4–20) dan `Harkat kerawanan`
  - Tersimpan di `gambar/modul-gee-15-kerawanan.png`.
- [ ] **Tulis Lesson Learnt Task IV**
  - Poin: variabel berbeda satuan baru bisa dijumlah setelah diharkat, TPI vs elevasi, sensitivitas pada ambangan kelas.
  - Draf (belum dipoles, sunting dulu sebelum masuk laporan):

    Empat variabel dengan satuan berbeda (meter jarak, meter elevasi, TPI, dan NDVI) baru bisa dijumlahkan sesudah semuanya diharkat ke skala 1 sampai 5, dan hasil penjumlahannya sangat bergantung pada ambang tiap variabel. Di ROI Batanghari harkat jarak air hampir seragam, 93,6% piksel ada di kelas 1, jadi variabel ini hanya membedakan pita tipis di tepi sungai

    TPI memberi hasil yang paling aneh. harkat TPI terbelah ke kelas 1 (49,1%) dan kelas 5 (29,8%), sementara kelas 2 sampai 4 masing masing hanya 6 sampai 8%, dan petanya tampak seperti bintik acak. SRTM menyimpan elevasi dalam meter bulat, jadi selisih elevasi dengan rata rata lingkungannya jarang jatuh di antara 0 dan −0,75 m. ambang 0,25 m di modul lebih halus dari data yang dipakai, dan kelas TPI lebih banyak mencerminkan pembulatan SRTM daripada bentuk lahan

    Elevasi justru variabel yang paling jelas memisahkan dataran banjir utara sungai dari daerah selatan yang lebih tinggi. Dataran di utara jatuh ke kelas 3 dan 4, selatan ke kelas 1, dan polanya terlihat konsisten dengan meander Batanghari di Gambar 12.

    Hasil akhirnya, 52,6% ROI masuk kelas 2 dan hanya 2,2% di kelas 4 dan 5, yang terkumpl di tepi sungai dan danau. Ada juga ketidakcocokn kecil antara kode dan Tabel 5: kode memberi kelas 1 untuk jumlah sampai 4, tabel memberi kelas 1 untuk di bawah 4, padahal jumlah empat harkat paling kecil adalah 4. menurut tabel 20% piksel kelas 1 itu seharusnya kelas 2

    Danau tapal kuda dan rawa gelap di utara sungai tidak terdeteksi oleh NDWI > 0,1, jadi jaraknya dihitung seolah daratan. Untuk area rawa seperti ini masker air dari NDWI saja kurang, dan MNDWI atau data air permukaan lain perlu dicoba

## 5. Task V: Eksposur, Kerentanan, dan Risiko Final, bobot 25% (bersama Task IV)

- [v] **Langkah 1: Harkat penduduk dari GHSL (urutkan waktu menurun, `first()`), Tabel 6**
  - Mengambil epok terbaru.
  - Dataset: [GHSL Population](https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_POP).
  - **Prasyarat**: Task V melanjutkan skrip Task IV (memakai `roi`, `bukanAir`, `harkatKerawanan`). Salin isi `task4.js` ke `task5.js`, lalu tambahkan kode Task V di bawahnya.
  - Skrip `task5` (9 Oktober 2026) = isi `task4` ditambah kode Task V, dibuat lewat "Save as" supaya `task4` tetap utuh. Semua layer Task V tampil tanpa error.

  ```js
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
- [v] **Langkah 2: Luas lahan terbangun (kelas 50) dan pertanian (kelas 40) dari WorldCover 10 m, `reduceResolution` ke 30 m, lalu harkatkan**
  - Data 10 m diringkas ke 30 m agar sejajar dengan grid variabel lain.
  - Dataset: [ESA WorldCover v200](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200). Dokumentasi: [`reduceResolution`](https://developers.google.com/earth-engine/apidocs/ee-image-reduceresolution).
  - Skrip `task5` menambahkan tiga `Map.addLayer` (`Harkat lahan terbangun`, `Luas pertanian`, `Harkat pertanian`) karena Gambar 17 dan 18 memintanya, sementara kode modul hanya menampilkan `Luas lahan terbangun`.
  - **Bug di kode modul (terverifikasi, kode `task5` belum diubah)**: `lahanTerbangun.multiply(area).reduceResolution(ee.Reducer.sum(), true)` tidak menjumlahkan 9 piksel 10 m. Nilai maksimum di ROI hanya 85,45 m², sekitar luas satu piksel WorldCover, jadi ambang > 100 m² (kelas 5) tidak pernah tercapai dan harkat lahan terbangun maupun pertanian praktis biner (kelas 1 atau 4). Uji perbaikan (9 Oktober 2026):

    | cara | luas maksimum per sel 30 m | catatan |
    | --- | --- | --- |
    | kode modul (`sum` berbobot) | 85,45 m² | setara satu piksel 10 m |
    | `reproject` ke proyeksi WorldCover dulu, lalu `sum` | 85,45 m² | tidak berubah |
    | `sum().unweighted()` | 2.136 m² | lebih besar dari luas sel, menghitung ganda |
    | fraksi `mean` × `pixelArea()` | 893,7 m² | cocok dengan sel 30 × 30 m, cara yang benar |

    Cara yang benar: `lahanTerbangun.unmask(0).reduceResolution({reducer: ee.Reducer.mean(), maxPixels: 1024}).reproject('EPSG:4326', null, 30).multiply(ee.Image.pixelArea())`. Dengan luas yang benar, ambang 40–100 m² (4–11% isi sel) membuat hampir semua sel kota masuk kelas 5, jadi ambangnya juga perlu ditinjau. **Keputusan: perbaiki di `task5` atau cukup dibahas di laporan?**

  ```js
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
- [v] **Tangkapan layar Gambar 16, 17, 18**: penduduk, lahan terbangun, lahan pertanian (masing-masing nilai + harkat berdampingan)
  - Tersimpan di `gambar/modul-gee-16-penduduk.png`, `gambar/modul-gee-17-terbangun.png`, dan `gambar/modul-gee-18-pertanian.png`.
- [v] **Langkah 3: Jumlahkan 3 harkat menjadi eksposur, lalu harkatkan ulang (Tabel 7)**

  ```js
  var eksposur = harkatPenduduk.add(harkatLahanTerbangun).add(harkatPertanian);
  Map.addLayer(eksposur, {min: 1, max: 15, palette: ['green', 'yellow', 'red']}, 'Eksposur', false);

  var harkatEksposur = eksposur.where(eksposur.gt(12), 5)
    .where(eksposur.gt(9).and(eksposur.lte(12)), 4)
    .where(eksposur.gt(6).and(eksposur.lte(9)), 3)
    .where(eksposur.gt(3).and(eksposur.lte(6)), 2)
    .where(eksposur.lte(3), 1);
  Map.addLayer(harkatEksposur, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat eksposur', false);
  ```
- [v] **Langkah 4: Kerentanan dari PDB dan IPM (band `b26` = 2015), jumlahkan, harkatkan (Tabel 8–9)**
  - **Arah harkat dibalik**: PDB atau IPM tinggi diberi harkat 1, karena kemampuan ekonomi dan manusia yang tinggi menurunkan kerentanan. Ini poin eksplisit di rubrik nilai A.
  - Dataset: [Gridded Global GDP per capita](https://gee-community-catalog.org/projects/gridded_gdp_hdi/) di GEE Community Catalog.
  - Halaman katalog itu sekarang mendokumentasikan versi 3.0 (1990–2022), tetapi aset versi 2 yang dipakai modul (`GDP_PPP_1990_2015_5arcmin_v2`, `HDI_1990_2015_v2`) **masih bisa dibaca**: diuji di Code Editor pada 9 Oktober 2026, masing-masing 26 band (1990–2015), jadi `b26` = 2015 tersedia. Kode modul bisa dipakai apa adanya.

  ```js
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
- [v] **Langkah 5: Peta risiko = harkat kerawanan + eksposur (+ kerentanan), harkatkan ulang (Tabel 10)**
  - Versi modul sengaja menonaktifkan kerentanan. Versi tiga komponen penuh dikerjakan di Tugas Mandiri nomor 4.
  - Ambang di blok ini (2/4/6/8) cocok untuk dua komponen (jumlah 2–10). Tabel 10 di modul memakai ambang untuk tiga komponen (< 3, 3–6, 7–9, 10–12, > 12). Saat mengaktifkan `.add(harkatKerentanan)` di Tugas Mandiri 4, sesuaikan ambangnya dan catat di laporan.
  - Sebaran kelas di ROI (9 Oktober 2026, skala 30 m, kode modul apa adanya):

    | layer | kelas 1 | kelas 2 | kelas 3 | kelas 4 | kelas 5 |
    | --- | --- | --- | --- | --- | --- |
    | harkat penduduk | 79,8% | 13,2% | 6,4% | 0,6% | 0,0% |
    | harkat lahan terbangun | 87,2% | 2,3% | 2,8% | 7,7% | 0% |
    | harkat pertanian | 95,8% | 0,7% | 0,8% | 2,7% | 0% |
    | harkat eksposur | 74,6% | 16,8% | 8,5% | 0,0% | 0% |
    | harkat PDB | 91,8% | 2,7% | 4,4% | 1,1% | 0% |
    | harkat IPM | 0% | 0% | 0% | 100% | 0% |
    | harkat kerentanan | 0% | 0% | 94,5% | 5,5% | 0% |
    | harkat risiko | 16,6% | 68,3% | 14,8% | 0,2% | 0% |

  - IPM bernilai satu kelas untuk seluruh ROI dan kerentanan 94,5% kelas 3, sesuai catatan modul bahwa data ±5 km hampir seragam di skala kota.

  ```js
  var risiko = harkatKerawanan.add(harkatEksposur);   // .add(harkatKerentanan);
  Map.addLayer(risiko, {min: 1, max: 10, palette: ['green', 'yellow', 'red']}, 'Risiko banjir', false);

  var harkatRisiko = risiko.where(risiko.gt(8), 5)
    .where(risiko.gt(6).and(risiko.lte(8)), 4)
    .where(risiko.gt(4).and(risiko.lte(6)), 3)
    .where(risiko.gt(2).and(risiko.lte(4)), 2)
    .where(risiko.lte(2), 1);
  Map.addLayer(harkatRisiko, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'Harkat risiko', false);
  ```
- [v] **Tangkapan layar Gambar 19**: `Eksposur` (3–15) dan `Harkat eksposur`
  - Tersimpan di `gambar/modul-gee-19-eksposur.png`.
- [v] **Tangkapan layar Gambar 20**: `Risiko banjir` dan `Harkat risiko`, legenda kelas terbaca
  - Tersimpan di `gambar/modul-gee-20-risiko.png`. Kode modul tidak membuat panel legenda kelas risiko, padahal instruksi Gambar 20 meminta legenda terbaca. Tambahkan legenda (bisa meniru `ui.Panel` dari Task III) kalau mau memenuhi instruksi itu.
- [ ] **Tulis pembahasan asumsi ambangan** dan keterbatasan resolusi
  - PDB/IPM beresolusi ±5 km, jauh lebih kasar daripada variabel fisik 30 m, sehingga kerentanan hampir seragam di skala kota kecil. Nilai A mensyaratkan asumsi ambangan dibahas.
- [ ] **Tulis Lesson Learnt Task V**
  - Draf (belum dipoles, sunting dulu sebelum masuk laporan):

    Arah harkat PDB dan IPM dibalik dari variabel fisik: nilai tinggi diberi harkat 1 karena kemampuan ekonomi dan kualitas manusia yang tinggi menurunkan kerentanan. Di ROI Batanghari arah itu hampir tidak berpengaruh, karena IPM jatuh di satu kelas untuk seluruh ROI dan kerentanan 94,5% di kelas 3. Data PDB dan IPM beresolusi sekitar 5 km, jadi satu sel sudah menutup sebagian besar kota

    Komponen eksposur ternyata terpengaruh bug di kode modul. Luas lahan terbangun dan pertanian dihitung dengan `reduceResolution(ee.Reducer.sum(), true)`, tapi nilai maksimumnya hanya 85,45 m², setara satu piksel WorldCover 10 m, bukan sekitar 900 m² untuk sel 30 m. akibatnya ambang > 100 m² untuk kelas 5 tidak pernah tercapai dan harkat kedua variabel praktis hanya kelas 1 atau 4. Cara yang memberi angka masuk akal adalah menghitung fraksi dengan `mean` lalu mengalikanya dengan luas sel, hasilnya maksimum 893,7 m²

    Dengan kode modul apa adanya, eksposur tidak pernah lebih dari kelas 3 dan risiko akhirnya 68,3% kelas 2, 14,8% kelas 3, dan hanya 0,2% kelas 4, tanpa kelas 5 sama sekali. Peta risiko di Gambar 20 karena itu lebih banyak menggambarkan pusat kota Jambi yang padat penduduk daripada dataran banjir di utara sungai, karena variabel fisik dan eksposur jatuh di area yang berbeda

    Model penjumlahn harkat memang mudah diaudit, tapi hasilnya sangat sensitif pada satuan dan ambang tiap variabel. Satu kesalahan satuan di eksposur cukup untuk menghapus seluruh kelas risiko tertinggi dari peta, dan kesalahan seperti ini baru terlihat sesudah sebaran kelasnya dihitung, bukan dari tampilan petanya

---

## 6. Tugas Praktikum Mandiri (III.9), wajib semua

- [v] **Tugas 1: Sensitivitas clustering**
  - Ubah jumlah cluster ke 5, 10, 20 dan ulang pelatihan beberapa kali. Hitung luas kelas kandidat terbangun dengan `reduceRegion` + `ee.Reducer.sum()` pada `pixelArea()`. Jelaskan efek jumlah cluster dan kestabilan nomor cluster.
  - Dokumentasi: [`reduceRegion`](https://developers.google.com/earth-engine/apidocs/ee-image-reduceregion).
  - Skrip `tugas1` (9 Oktober 2026). Gambar: `gambar/tugas-1-k5-vs-k20.png` (kiri k = 5, kanan k = 20, seed bawaan).
  - Cara memilih cluster kandidat terbangun: cluster yang lebih dari 50% pikselnya ditandai terbangun oleh ESA WorldCover. Aturan ini dipakai supaya 12 percobaan dinilai sama; pilihan visual di Task I (cluster 9 dan 11) tetap dicatat sebagai pembanding.

    | k | seed 10 (bawaan) | seed 1 | seed 2 |
    | --- | --- | --- | --- |
    | 5 | 45,2 Ha, cluster [4] | 346,9 Ha, [1] | 41,2 Ha, [3] |
    | 10 | 554,4 Ha, [4, 9] | 779,4 Ha, [1, 6, 9] | 696,0 Ha, [3, 4, 6] |
    | 15 | 722,6 Ha, [9, 10, 11] | 615,4 Ha, [1, 6, 14] | 639,5 Ha, [3, 4, 6, 12] |
    | 20 | 599,1 Ha, [9, 11, 19] | 485,3 Ha, [6, 14, 15] | 603,6 Ha, [3, 4, 6, 12] |

    IoU terhadap k = 15 seed 10: k = 5 hanya 0,06–0,34, k = 10 sampai 20 berkisar 0,64–0,92. Pilihan visual Task I memberi 497,8 Ha, IoU 0,689 terhadap aturan WorldCover pada model yang sama (aturan ikut memilih cluster 10 yang di Task I dibuang).
  - Draf jawaban:

    Jumlah cluster paling berpengaruh di nilai kecil. Dengan k = 5 luas kandidat terbangun berubah dari 41 Ha ke 347 Ha hanya karena seed diganti, karena dengan lima kelompok permukiman selalu tercampur dengan kelas lain, kadang ikut tanah terbuka, kadang hanya atap paling terang. mulai k = 10 hasilnya lebih stabil di 485 sampai 779 Ha, dan peta k = 20 sudah menangkap hampir seluruh kota Cepu

    Nomor cluster tidak stabl sama sekali. Untuk k = 15 kelompok terbangun bernomor 9, 10, 11 di seed bawaan, lalu 1, 6, 14 di seed 1, lalu 3, 4, 6, 12 di seed 2. Kode seperti `hasil.eq(2).or(hasil.eq(3))` di modul hanya benar untuk satu kali pelatihan, jadi nomor cluster harus dipilih ulang setiap model dilatih ulang
- [v] **Tugas 2: Kalibrasi ambangan NDBI**
  - Ambil NDBI di 5 lokasi jelas terbangun dan 5 jelas bukan lewat Inspector, tentukan ambangan baru, bandingkan peta dan laporkan perubahan luas (Ha).
  - Skrip `tugas2` (9 Oktober 2026). Gambar: `gambar/tugas-2-ambang.png` (merah = terbangun dengan ambang −0,1, cyan = piksel yang hilang saat ambang dinaikkan).
  - Data titik: 10 titik Inspector Task II (tabel di Task II, butir kalibrasi). NDBI terbangun 0,076 sampai 0,151, bukan terbangun −0,398 sampai −0,107. Ambang baru = titik tengah −0,016, dibulatkan **−0,02**.
  - Luas terbangun Jabodetabekpunjur: ambang −0,1 = **175.563 Ha**, ambang −0,02 = **112.742 Ha**, turun 62.821 Ha (−35,8%).
  - Draf jawaban:

    Ambang −0,02 dari sepuluh titik Inspector memisahkan kesepuluh titik itu dengan selisih paling lebar, tapi luas terbangun turun 35,8% dibanding ambang −0,1. piksel yang hilang (cyan di peta) hampir semua ada di tepi kawasan kota dan permukiman pinggiran, sementara inti Jakarta tetap. Titik kalibrasi sengaja dipilih yang paling jelas, jadi ambang dari titik ekstrem seperti ini cenderung terlalu ketat untuk permukiman campuran

    Perbandingan dengan WorldCover di Task II memberi gambaran yang sama: makin tinggi ambang makin tinggi presisi, tapi makin banyak permukiman yang hilang. Pilihan ambang bergantung tujuan petanya, dan −0,1 tetap lebih seimbang untuk menghitung luas kota
- [v] **Tugas 3: Urban sprawl kota lain**
  - Pindahkan ROI ke satu kota pilihan (Bandung atau Sleman), tambahkan 2024 ke `yearList`, sajikan peta dan grafik, jelaskan pola ekspansi.
  - Skrip `tugas3` (9 Oktober 2026), ROI Kota Bandung dan sekitarnya termasuk Cimahi (107,50–107,75 BT; 6,83–7,02 LS), `yearList` ditambah 2024, band luas memakai perbaikan `built.gt(0)`. Gambar: `gambar/tugas-3-bandung-peta.png` dan `gambar/tugas-3-bandung-grafik.png`.

    | tahun | 1990 | 1995 | 2000 | 2005 | 2010 | 2015 | 2020 | 2024 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | luas (Ha) | 11.772 | 13.917 | 18.278 | 19.522 | 20.153 | 29.505 | 24.672 | 26.105 |

  - Draf jawaban:

    Inti kota Bandung dan Cimahi sudah terbangun di 1990, lalu perluasan bergerak ke tenggara ke arah Bojongsoang dan Rancaekek, ke utara di kaki bukit, dan di 2024 ada bercak baru di selatan. Luasnya naik dari 11.772 Ha di 1990 ke 26.105 Ha di 2024

    Polanya sama dengan Jabodetabekpunjur: lonjakan besar tepat di 2015 lalu turun di 2020. Dua kota yang berbeda menunjukkan lompatan di tahun yang sama, yaitu tahun pertama komposit memakai sensor OLI, jadi sebagian lonjakan itu lebih mungkin berasal dari pergantian sensor daripada pembangunan baru
- [v] **Tugas 4: Risiko tiga komponen**
  - Aktifkan `.add(harkatKerentanan)`, bandingkan peta sebelum dan sesudah, hitung luas tiap kelas risiko 1–5 (`ee.Reducer.histogram()` atau `reduceRegion` bertingkat), diskusikan apakah kerentanan mengubah peringkat risiko.
  - Dokumentasi: [`ee.Reducer.histogram`](https://developers.google.com/earth-engine/apidocs/ee-reducer-histogram), [`reduceRegion`](https://developers.google.com/earth-engine/apidocs/ee-image-reduceregion).
  - Skrip `tugas4` = `task5` + risiko tiga komponen dengan ambang Tabel 10 (3–6 kelas 2, 7–9 kelas 3, 10–12 kelas 4, > 12 kelas 5; kelas 1 tidak mungkin karena jumlah minimum 3). Gambar: `gambar/tugas-4-risiko-2-vs-3-komponen.png` (kiri 2 komponen, kanan 3 komponen).

    | kelas | 2 komponen (Ha) | 3 komponen (Ha) |
    | --- | --- | --- |
    | 1 | 11.509 | 0 |
    | 2 | 47.360 | 38.549 |
    | 3 | 10.276 | 30.546 |
    | 4 | 153 | 203 |
    | 5 | 0 | 0 |

    Perpindahan kelas: 1→2 11.509 Ha, 2→2 27.040 Ha, 2→3 20.320 Ha, 3→3 10.226 Ha, 3→4 50 Ha, 4→4 153 Ha. Tidak ada piksel yang turun kelas.
  - Draf jawaban:

    Menambahkan kerentanan membuat 31.879 Ha naik satu kelas dan tidak ada yang turun. Kerentanan di ROI hampir seragam, 94,5% kelas 3, jadi penambahannya bekerja seperti menambah konstanta sekitar 3 ke semua piksel. urutan relatif antarwilayah hampir tidak berubah, yang berubah adalah label kelasnya karena ambang Tabel 10 dipakai pada rentang yang lebih lebar

    Di peta tiga komponen muncul blok persegi besar yang tidak ada di versi dua komponen. Blok itu batas sel PDB dan IPM yang beresolusi sekitar 5 km, jadi kerentanan menambahkn pola sel data, bukan informasi baru tentang wilayah. Untuk ROI seukuran kota, komponen kerentanan dari data ini belum memberi pembeda yang berarti

## 7. Soal HOTS (III.10), pilih minimal 2

Kelima problem dikerjakan (9 Oktober 2026). Skrip: `hotsAB` (A dan B), `hotsCD` (C dan D), `hotsE` (E). Laporan minimal memuat dua, tapi semuanya boleh disertakan.

- [v] **Problem A: Detektif Bit QA (C4)**: fungsi `maskAwanKustom` yang menolak piksel hanya jika minimal 2 dari 4 bit menyala, banding jumlah piksel valid, bahas trade-off
  - Gambar: `gambar/hots-a-tambahan-observasi.png` (tambahan observasi valid per piksel, mask kustom dikurangi mask modul).

    | ukuran (44 citra Landsat 8, 2022) | mask modul (tolak ≥ 1 bit) | mask kustom (tolak ≥ 2 bit) |
    | --- | --- | --- |
    | rata-rata observasi valid per piksel | 7,50 | 13,36 (+78%) |
    | median band biru komposit | 0,0449 | 0,0527 |
    | persentil 99 band biru komposit | 0,119 | 0,166 |

    Observasi yang diselamatkan mask kustom (tepat satu bit menyala), rata-rata per piksel: cloud saja 3,78, cirrus saja 1,07, shadow saja 0,78, dilated saja 0,23.
  - Draf jawaban:

    Mask kustom hampir menggandakan observasi valid, dari 7,50 ke 13,36 per piksel, dan tambahan paling banyak ada di selatan yang lebih sering berawan. Tapi 64% observasi yang diselamatkan adalah piksel yang bit cloud-nya menyala sendirian, jadi yang masuk lagi sebagian besar memang awan, hanya tanpa tanda dilated atau bayangan. Akibatnya terlihat di komposit: persentil 99 band biru naik dari 0,119 ke 0,166, tanda ada sisa awan terang yang lolos median

    Trade-off-nya jelas. Mask kustom berguna untuk daerah yang hampir selalu berawan dan kekurangan observasi, tapi untuk komposit setahun di Jabodetabekpunjur mask modul yang ketat sudah cukup dan hasilnya lebih bersih
- [v] **Problem B: Duel Indeks Air (C4)**: luas air NDWI vs MNDWI (ambang 0.1), peta selisih, jelaskan kenapa MNDWI unggul di latar terbangun ([Xu, 2006](https://doi.org/10.1080/01431160600589179))
  - Gambar: `gambar/hots-b-ndwi-vs-mndwi.png` (biru = air menurut keduanya, merah = hanya NDWI, kuning = hanya MNDWI).
  - Catatan teknis: di 26.036 Ha NDWI kosong (masked) tapi MNDWI terbaca air, karena band NIR tidak bernilai di piksel itu, kemungkinan laut gelap. Perbandingan di bawah hanya di piksel tempat keduanya bernilai.

    | ukuran | luas (Ha) |
    | --- | --- |
    | air menurut NDWI > 0,1 | 68.185 |
    | air menurut MNDWI > 0,1 | 84.074 |
    | selisih (MNDWI − NDWI) | 15.889 |
    | hanya MNDWI | 17.199 (sawah 7.111, badan air 8.762, lahan basah 850, lainnya 476) |
    | hanya NDWI | 1.311 (badan air 1.310, terbangun 0,6) |

  - Draf jawaban:

    MNDWI menangkap air 15.889 Ha lebih banyak dari NDWI di komposit yang sama. Area yang hanya terbaca MNDWI terkumpul di pesisir timur laut, yaitu tambak dan sawah tergenang (7.111 Ha di kelas pertanian WorldCover) dan badan air keruh. SWIR diserap air jauh lebih kuat dari NIR, jadi air keruh atau dangkal yang NIR-nya masih memantul tetap terbaca sebagai air oleh MNDWI

    Untuk latar terbangun, salah deteksi NDWI yang dibahas Xu (2006) di komposit ini ternyata kecil: hanya 0,6 Ha piksel terbangun yang terbaca air oleh NDWI saja. Pada ambang 0,1 dan komposit median setahun, keunggulan MNDWI di Jabodetabekpunjur lebih terlihat di air keruh dan sawah daripada di kota
- [v] **Problem C: Skala TPI (C5)**: radius `focalMean` 1, 3, 5, 9, tabel radius–luas kelas 5, putuskan radius terbaik untuk dataran banjir
  - Gambar: `gambar/hots-c-tpi-radius-1-vs-9.png` (biru = TPI kelas 5, cyan = proksi pernah tergenang GSW; kiri radius 1, kanan radius 9).
  - Proksi dataran banjir: JRC Global Surface Water, piksel yang pernah tergenang 1–49% waktu (1984–2021) di luar air 2022. Luas di ROI 2.165 Ha (sekitar 3% daratan).

    | radius `focalMean` | luas kelas 5 (Ha) | kelas 5 yang pernah tergenang | genangan yang tertangkap |
    | --- | --- | --- | --- |
    | 1 | 7.217 | 4,5% | 14,8% |
    | 3 (modul) | 20.664 | 4,1% | 39,2% |
    | 5 | 24.953 | 4,4% | 50,5% |
    | 9 | 27.819 | 4,9% | 63,0% |

  - Draf jawaban:

    Makin besar radius, makin luas kelas 5: dari 7.217 Ha di radius 1 ke 27.819 Ha di radius 9, karena pembanding rata rata lingkungan makin jauh dan makin banyak piksel yang terbaca lebih rendah dari sekitarnya. Radius 9 menangkap 63% area yang pernah tergenang, tapi hanya 4,9% kelas 5-nya benar benar pernah tergenang, hampir sama dengan proporsi genangan di seluruh ROI

    Peta radius 9 memperlihatkan sebabnya: kelas 5 membentuk jaringan lembah bercabang di daerah selatan yang lebih tinggi, bukan dataran banjir di utara. TPI dari SRTM meter bulat juga terkuantisasi (Task IV). Radius 9 paling baik di antara keempatnya, tapi untuk ROI sedatar ini TPI bukan variabel yang tepat, dan elevasi atau kemiringan lereng lebih berguna
- [v] **Problem D: Validasi banjir (C5)**: 10 titik pernah banjir + 10 tidak, akurasi di ambang harkat ≥ 4, usulkan perbaikan ambangan (butuh riset berita lokasi banjir)
  - Gambar: `gambar/hots-d-titik-proksi.png` (titik oranye/cyan di atas harkat kerawanan dan proksi genangan).
  - **Proksi, bukan data berita**: titik "pernah banjir" diambil acak (seed 7) dari area pernah tergenang JRC GSW, titik "tidak" dari area yang tidak pernah tergenang. Ganti dengan 10 + 10 titik dari berita kalau ada; kode `hotsCD` tinggal diganti bagian `titikD`.
  - 20 titik, ambang harkat kerawanan ≥ 4: pernah tergenang tertangkap 4 dari 10, tidak tergenang benar 10 dari 10, akurasi 70% (presisi 100%, recall 40%).
  - Sampel besar 300 + 300 titik (seed 11): elevasi median 8 m vs 18,5 m, jarak dari air median 398 m vs 1.766 m. Separuh piksel yang pernah tergenang berjarak > 398 m dari air 2022, jauh di atas ambang modul (kelas 5 hanya < 50 m).
  - Usulan: ambang jarak 250 / 500 / 750 / 1.000 m. Diuji di sampel 600 titik: akurasi 64,5% → 69,8%, recall 29,7% → 45,7%, presisi 97,8% → 88,4%. Di 20 titik akurasi tetap 70% (tertangkap 5 dari 10, satu salah tanda).
  - Draf jawaban:

    Peta kerawanan modul hampir tidak pernah salah menandai daerah kering, tapi hanya menangkap 4 dari 10 titik yang pernah tergenang. Variabel yang paling melemahkan adalah jarak dari air: ambang modul berhenti di 200 m, sementara separuh area yang pernah tergenang berjarak lebih dari 398 m dari air 2022, karena genangan musiman di dataran banjir menyebar jauh dari alur sungai

    Melebarkan ambang jarak ke 250, 500, 750, dan 1.000 m menaikkan recall dari 29,7% ke 45,7% di sampel 600 titik, dengan presisi turun dari 97,8% ke 88,4%. Titik "pernah banjir" di sini berasal dari GSW, bukan dari berita, jadi hasilnya mengukur kecocokan dengan riwayat genangan satelit, belum dengan kejadian banjir yang dilaporkan
- [v] **Problem E: Perancang model risiko (C6)**: variabel baru (lereng atau CHIRPS), harkat sendiri, tabel asumsi, uji sensitivitas (paling berat). Data pendukung: [`ee.Terrain.slope`](https://developers.google.com/earth-engine/apidocs/ee-terrain-slope), [CHIRPS Daily](https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY)
  - Gambar: `gambar/hots-e-risiko-kota-jambi.png` (harkat risiko usulan dengan legenda, batas Kota Jambi).
  - Wilayah: Kota Jambi dari FAO GAUL 2015 level 2 (10.384 Ha, daratan 9.657 Ha). Batas kecamatan tidak tersedia di katalog GEE maupun Community Catalog, jadi soal yang meminta satu kecamatan diganti satu kota; poligonnya bisa diganti di variabel `wilayah`.
  - Tabel asumsi:

    | komponen | variabel | ambang harkat 1 → 5 | dasar |
    | --- | --- | --- | --- |
    | kerawanan (bobot 0,35) | jarak dari air | > 1.000 / 750–1.000 / 500–750 / 250–500 / ≤ 250 m | Problem D: median jarak area pernah tergenang 398 m |
    | kerawanan (bobot 0,35) | elevasi SRTM | > 20 / 15–20 / 10–15 / 5–10 / ≤ 5 m | Tabel 4 modul; Problem D: median 8 m vs 18,5 m |
    | kerawanan (bobot 0,15) | kemiringan lereng (`ee.Terrain.slope`) | > 8 / 5–8 / 3–5 / 1–3 / ≤ 1 derajat | menggantikan TPI yang terkuantisasi (Task IV, Problem C) |
    | kerawanan (bobot 0,15) | NDVI | > 0,5 / 0,25–0,5 / 0–0,25 / −0,25–0 / ≤ −0,25 | Tabel 4 modul |
    | eksposur (rata-rata) | penduduk GHSL | ≤ 10 / 10–100 / 100–200 / 200–300 / > 300 | Tabel 6 modul |
    | eksposur (rata-rata) | fraksi terbangun WorldCover | ≤ 10% / 10–30% / 30–50% / 50–70% / > 70% | fraksi `mean`, memperbaiki bug Task V |
    | kerentanan | tidak dipakai | - | PDB/IPM ±5 km hampir seragam di skala kota (Tugas 4) |

    Risiko = 0,6 × kerawanan + 0,4 × eksposur, dibulatkan ke kelas 1–5.
  - Uji sensitivitas (luas dalam Ha; validasi kerawanan ≥ 4 terhadap proksi GSW, 499 Ha pernah tergenang = 5,2% daratan):

    | skema | kelas 1 | 2 | 3 | 4 | 5 | recall genangan | presisi | sama dengan A |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | A usulan | 703 | 4.773 | 3.932 | 249 | 0 | 60,7% | 24,1% | - |
    | B bobot kerawanan sama (0,25 × 4) | 340 | 4.419 | 4.697 | 201 | 0 | 50,3% | 31,3% | 78,7% |
    | C kerawanan 0,5 | 717 | 4.247 | 4.398 | 296 | 0 | 60,7% | 24,1% | 79,6% |

  - Draf jawaban:

    Model ini mengganti TPI dengan kemiringan lereng, melebarkan ambang jarak dari air sesuai hasil Problem D, dan menghitung eksposur lahan terbangun dari fraksi yang benar. Kerentanan tidak dipakai karena di skala kota datanya hampir seragam. Kelas 4 terkumpul di tepi selatan Batanghari di pusat kota, tempat permukiman padat berada dekat sungai, dan tidak ada kelas 5

    Uji sensitivitas menunjukkan sekitar 20% luas berganti kelas saat bobot diubah, jadi peta ini cukup stabil untuk membedakan kelas rendah dan sedang, tapi batas kelas 3 dan 4 sensitif pada bobot. Validasi terhadap genangan GSW memberi recall 60,7% dengan presisi 24,1%, sekitar 4,6 kali proporsi genangan di seluruh daratan. Angka ini mengukur kecocokan dengan riwayat genangan satelit, belum dengan kejadian banjir yang dilaporkan

---

## 7b. Konversi Skrip ke Python (tugas tambahan dosen)

- [v] **Salin skrip JavaScript final ke `js/`** (13 berkas, sama dengan repository `users/vermilion10/praktikum-gee`)
- [v] **Konversi ke Python di `python/`** dengan `earthengine-api` dan `folium`; panduan dan tabel padanan fitur di `python/README.md`
  - Peta Code Editor menjadi HTML folium di `python/output/*.html`, grafik menjadi PNG matplotlib, angka hasil `getInfo()` disimpan sebagai JSON.
  - Diuji 9 Oktober 2026: ke-13 skrip berjalan tanpa error dan angka utamanya sama dengan Code Editor (CLOUD_COVER_LAND 0,06; luas Task III 72.060 → 180.747 Ha; Tugas 1–4 dan HOTS A–E identik).
  - Satu beda kecil: NDBI titik V2 di Tugas 2 bernilai −0,243 di Python (sampel piksel 30 m), sementara pembacaan Inspector −0,336 (Inspector membaca di skala zoom peta). Kesimpulan tidak berubah, titik itu tetap di bawah ambang.
  - Tile peta di berkas HTML memakai token Earth Engine yang berlaku sementara; jalankan ulang skripnya kalau petanya kosong saat dibuka belakangan.
  - `FAO/GAUL/2015/level2` (dipakai `hotsE`) sudah ditandai usang oleh Earth Engine dan diganti `FAO/GAUL/2025/level2`; untuk sekarang masih berjalan.
- [ ] **Masukkan folder `js/` dan `python/` ke arsip pengumpulan** kalau dosen meminta kodenya ikut dikumpulkan

## 8. Laporan dan Pengumpulan

- [ ] **Kumpulkan semua tautan *Get Link*** skrip Task I–V (dan skrip tugas mandiri/HOTS), pastikan bisa dilihat penguji
  - Laporan tanpa tautan yang bisa dibuka tidak bisa diverifikasi.
- [ ] **Susun Laporan Praktikum (.pdf)** berisi:
  - Tangkapan layar Gambar 1–20 beserta panel Layers.
  - Potongan kode JavaScript dan penjelasan fungsinya.
  - Lesson Learnt tiap task (5 buah).
  - Jawaban Tugas Mandiri 1–4 dan minimal 2 Problem HOTS.
- [ ] **Sebutkan perbaikan bug modul di laporan**
  - Bagian Task III: band `area` di modul memakai `built.multiply(...)`, padahal nilai piksel `built` adalah tahun, jadi luasnya terkali sekitar 2000 (143 juta Ha untuk 1990, padahal seluruh ROI sekitar 600 ribu Ha). Tulis baris lama, baris baru (`built.gt(0).multiply(...)`), dan tabel luas sesudah perbaikan. Sebut juga `l8` yang tidak didefinisikan di kode Task III.
  - Alasannya: penguji yang membandingkan dengan angka modul akan melihat beda besar, jadi perbaikannya perlu dijelaskan, bukan diam diam diganti.
  - Bagian Task V (dibahas saja, kode tidak diubah sesuai keputusan 9 Oktober 2026): `reduceResolution(ee.Reducer.sum(), true)` di langkah 2 tidak menjumlahkan piksel 10 m (maksimum 85,45 m² per sel 30 m), jadi kelas 5 lahan terbangun dan pertanian tidak pernah tercapai. Sertakan tabel uji empat cara dari Task V Langkah 2, sebaran kelas risiko, dan dampaknya (tidak ada kelas risiko 5).
  - Sebut juga temuan kecil lain: Tabel 5 dan kode Task IV beda di batas kelas 1/2, TPI terkuantisasi oleh SRTM meter bulat, layer yang diminta gambar tapi tidak ada di kode (NDWI Task IV; harkat lahan terbangun, luas dan harkat pertanian Task V), dan legenda risiko yang tidak ada di kode.
- [ ] **Laporkan bug ke dosen atau asisten** (opsional, tapi membantu teman sekelas)
  - Draf pesan, sesuaikan sapaan dan kirim sendiri lewat Teams:

    > Selamat siang Pak/Bu, izin melaporkan temuan saat mengerjakan modul Intermediate GEE. Di Task III, langkah 3, band luas dihitung dengan `built.multiply(ee.Image.pixelArea().multiply(0.0001))`. Nilai piksel `built` berisi tahun (1990, 1995, dst.), jadi luas ikut terkali tahun dan grafik "Urban area (Ha)" menunjukkan sekitar 143 juta Ha untuk 1990, padahal ROI Jabodetabekpunjur hanya sekitar 600 ribu Ha. Dengan `built.gt(0).multiply(...)` hasilnya 72.060 Ha untuk 1990 dan 180.747 Ha untuk 2020. Selain itu, kode Task III memakai `l8` yang hanya didefinisikan di kode Task II, jadi akan error kalau dijalankan sebagai skrip terpisah. Terima kasih.

- [ ] **Cek tiap gambar**: tidak blur, tidak terpotong, layer terlihat, nama berkas sesuai pola
- [ ] **Beri nama arsip sesuai Tabel 12**: `[GEE2026_5A_D4_2024]_ModulGEE_001.zip` (ganti `5A`/`5B` dengan kelas, `2024` dengan angkatan, `001` dengan 3 digit terakhir NIM)
- [ ] **Kompres semua berkas jadi satu .zip**
- [ ] **Unggah ke [MS Teams](https://teams.microsoft.com)**, slot tugas "Pengumpulan Praktikum Intermediate GEE", sebelum batas waktu
  - Cek tenggat di Teams, modul tidak mencantumkan tanggalnya.

## 9. Cek Akhir Sebelum Kumpul (berdasarkan rubrik)

- [ ] Task I: filter metadata benar, cluster terbangun diverifikasi visual dengan argumen spektral
- [ ] Task II: cloud mask dipahami (bit QA), kedua indeks tepat, ambangan dikalibrasi dengan Inspector
- [ ] Task III: 7 tahun lintas sensor semua berhasil, peta + grafik benar, pola ekspansi dianalisis kritis
- [ ] Task IV–V: semua harkat benar (termasuk arah PDB/IPM), asumsi ambangan dibahas
- [ ] Pelaporan: screenshot lengkap, kode dijelaskan, lesson learnt mendalam, semua tugas dijawab

## Catatan

- Bug di modul sendiri yang ditemukan saat praktik: `l8` tidak didefinisikan di kode Task III, dan band `area` Task III terkali tahun (lihat Task III Langkah 4). Keduanya sudah ditangani di skrip `task3`.
- Skrip sumber e-book punya bug yang sudah diperbaiki di modul (Lampiran A): band `GREEN` di Task II, penamaan `image` di Task IV, `sqrt().multiply(30)` jarak air, `lte(-0.25)` harkat NDVI, `String(year)` di legenda. Pakai versi modul, jangan versi e-book.
- Hindari `getInfo()` di dalam perulangan dan selalu filter koleksi sebelum operasi berat, karena kuota GEE dipakai bersama.
