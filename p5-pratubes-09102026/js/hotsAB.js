// HOTS Problem A (Detektif Bit QA) dan Problem B (Duel Indeks Air)
// Wilayah dan koleksi sama dengan Task II: Jabodetabekpunjur, Landsat 8 tahun 2022

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
var filtered = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
  .filterBounds(roi).filterDate('2022-01-01', '2022-12-31');

function skala(image) {
  return image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                      ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
    .multiply(0.0000275).add(-0.2);
}

// Jumlah bit curiga yang menyala (dilated, cirrus, cloud, shadow): 0 s.d. 4
function jumlahBit(image) {
  var qa = image.select('QA_PIXEL');
  return qa.bitwiseAnd(1 << 1).gt(0)
    .add(qa.bitwiseAnd(1 << 2).gt(0))
    .add(qa.bitwiseAnd(1 << 3).gt(0))
    .add(qa.bitwiseAnd(1 << 4).gt(0));
}

// Mask modul: tolak kalau minimal satu bit menyala
function cloudMask(image) {
  return skala(image).updateMask(jumlahBit(image).eq(0));
}

// ===== Problem A: tolak hanya kalau minimal dua bit menyala =====
function maskAwanKustom(image) {
  return skala(image).updateMask(jumlahBit(image).lt(2));
}

var validModul = filtered.map(function(img) { return jumlahBit(img).eq(0).rename('v'); }).sum();
var validKustom = filtered.map(function(img) { return jumlahBit(img).lt(2).rename('v'); }).sum();

// Dari observasi yang diselamatkan mask kustom (tepat satu bit), bit mana yang menyala
function satuBit(bit) {
  return filtered.map(function(img) {
    var qa = img.select('QA_PIXEL');
    return jumlahBit(img).eq(1).and(qa.bitwiseAnd(1 << bit).gt(0)).rename('v');
  }).sum();
}

var medianModul = filtered.map(cloudMask).median().clip(roi);
var medianKustom = filtered.map(maskAwanKustom).median().clip(roi);
var visKomposit = {bands: ['B5', 'B6', 'B2'], min: [0.1, 0.05, 0], max: [0.4, 0.3, 0.15]};
Map.centerObject(roi, 10);
Map.addLayer(medianModul, visKomposit, 'A: komposit mask modul', false);
Map.addLayer(medianKustom, visKomposit, 'A: komposit mask kustom', false);
Map.addLayer(validKustom.subtract(validModul).clip(roi), {min: 0, max: 20, palette: ['white', 'orange', 'red']},
  'A: tambahan observasi valid', false);

var statA = validModul.rename('modul')
  .addBands(validKustom.rename('kustom'))
  .addBands(satuBit(1).rename('hanyaDilated'))
  .addBands(satuBit(2).rename('hanyaCirrus'))
  .addBands(satuBit(3).rename('hanyaCloud'))
  .addBands(satuBit(4).rename('hanyaShadow'))
  .reduceRegion({reducer: ee.Reducer.mean(), geometry: roi, scale: 90, maxPixels: 1e10, tileScale: 4});
// Kecerahan biru komposit sebagai indikator sisa awan (awan terang di band biru)
var biru = medianModul.select('B2').rename('modul').addBands(medianKustom.select('B2').rename('kustom'))
  .reduceRegion({reducer: ee.Reducer.percentile([50, 99]), geometry: roi, scale: 90, maxPixels: 1e10, tileScale: 4});

// ===== Problem B: NDWI vs MNDWI pada komposit yang sama (komposit mask modul) =====
var ndwi = medianModul.normalizedDifference(['B3', 'B5']).rename('ndwi');     // (GREEN - NIR) / (GREEN + NIR)
var mndwi = medianModul.normalizedDifference(['B3', 'B6']).rename('mndwi');   // (GREEN - SWIR1) / (GREEN + SWIR1)
var airNdwi = ndwi.gt(0.1);
var airMndwi = mndwi.gt(0.1);
var hanyaNdwi = airNdwi.and(airMndwi.not());
var hanyaMndwi = airMndwi.and(airNdwi.not());

Map.addLayer(medianModul, visKomposit, 'B: komposit');
Map.addLayer(airNdwi.and(airMndwi).selfMask(), {palette: 'blue'}, 'B: air menurut keduanya');
Map.addLayer(hanyaNdwi.selfMask(), {palette: 'red'}, 'B: air hanya menurut NDWI');
Map.addLayer(hanyaMndwi.selfMask(), {palette: 'yellow'}, 'B: air hanya menurut MNDWI');

var ha = ee.Image.pixelArea().divide(1e4);
var statB = airNdwi.multiply(ha).rename('ndwi')
  .addBands(airMndwi.multiply(ha).rename('mndwi'))
  .addBands(hanyaNdwi.multiply(ha).rename('hanyaNdwi'))
  .addBands(hanyaMndwi.multiply(ha).rename('hanyaMndwi'))
  .reduceRegion({reducer: ee.Reducer.sum(), geometry: roi, scale: 30, maxPixels: 1e10, tileScale: 4});

// Tutupan lahan (WorldCover) di area yang diperdebatkan
var wc = ee.ImageCollection('ESA/WorldCover/v200').first().rename('wc');
function luasPerKelas(maskImg) {
  return ee.List(ha.updateMask(maskImg).addBands(wc).reduceRegion({
    reducer: ee.Reducer.sum().group({groupField: 1, groupName: 'kelas'}),
    geometry: roi, scale: 30, maxPixels: 1e10, tileScale: 4
  }).get('groups'));
}

ee.Dictionary({
  jumlahCitra: filtered.size(), A: statA, biruB2: biru,
  B: statB, wcHanyaNdwi: luasPerKelas(hanyaNdwi), wcHanyaMndwi: luasPerKelas(hanyaMndwi)
}).evaluate(function(r, e) { print('HOTSAB ' + (e ? 'ERR ' + e : JSON.stringify(r))); });
