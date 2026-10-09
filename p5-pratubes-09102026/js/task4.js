// Prasyarat dari Task II: fungsi cloudMask (kode Task IV memakainya tanpa mendefinisikannya)
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

// Badan air
var ndwi = image.expression('(GREEN - NIR) / (GREEN + NIR)', bandMap);
var air = ndwi.gt(0.1);
var bukanAir = air.eq(0);
// Tambahan (bukan dari modul): layer NDWI untuk Gambar 10
Map.addLayer(ndwi, {min: -1, max: 1, palette: ['red', 'white', 'blue']}, 'NDWI', false);
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
