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
// Modul memakai cluster 2 dan 3. Pada run ini cluster 2 justru bervegetasi (NDBI -0.16, NDVI 0.36),
// sedangkan cluster 9 dan 11 punya NDBI positif, NDVI rendah, dan mengumpul di pusat kota Cepu.
var lahan_terbangun = hasil.eq(9).or(hasil.eq(11)).selfMask();

// 13. Tampilkan hasilnya
Map.addLayer(lahan_terbangun, {
  bands: ['cluster'],
  min: 1,
  palette: ['ff7070']
}, 'Bangunan');

// Tambahan (bukan dari modul): cluster mentah untuk memilih nomor cluster bangunan
Map.addLayer(hasil.randomVisualizer(), {}, 'Cluster mentah', false);

// Tambahan (bukan dari modul): arahkan peta ke poligon kajian untuk Gambar 1
Map.centerObject(geometry2, 14);
