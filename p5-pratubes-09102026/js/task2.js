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
