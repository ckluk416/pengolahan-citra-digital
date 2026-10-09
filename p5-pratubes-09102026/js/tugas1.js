// Tugas Mandiri 1: sensitivitas clustering (jumlah cluster dan seed)
// Data dan wilayah kajian sama dengan Task I

var dataset = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2');
var geometry = ee.Geometry.Point([112.05730244401117, -6.897418238470722]);
dataset = dataset
  .filterBounds(geometry)
  .filterMetadata('CLOUD_COVER_LAND', 'less_than', 50)
  .sort('CLOUD_COVER_LAND');
var img = dataset.first();

var geometry2 = ee.Geometry.Polygon(
  [[[111.56510661311408, -7.125131151145682],
    [111.56510661311408, -7.178102498857165],
    [111.62192652888557, -7.178102498857165],
    [111.62192652888557, -7.125131151145682]]], null, false);

var band = ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'];
var img_pilih = img.select(band).clip(geometry2);
var data_training = img_pilih.sample({region: geometry2, scale: 30, numPixels: 500});

Map.addLayer(img, {bands: ['SR_B4', 'SR_B3', 'SR_B2'], min: 7061, max: 14103}, 'Data paling bersih');
Map.centerObject(geometry2, 14);

// Acuan pemilihan cluster: ESA WorldCover kelas 50 (terbangun).
// Cluster dianggap kandidat terbangun kalau lebih dari 50% pikselnya terbangun menurut WorldCover.
// Aturan ini menggantikan pilihan visual supaya semua percobaan dinilai dengan cara yang sama.
var terbangunWC = ee.ImageCollection('ESA/WorldCover/v200').first().eq(50).rename('wc50');
var luasPiksel = ee.Image.pixelArea().divide(1e4).rename('ha');

function uji(k, seed) {
  var model = ee.Clusterer.wekaKMeans({nClusters: k, seed: seed}).train(data_training);
  var hasil = img_pilih.cluster(model);
  var grup = ee.List(terbangunWC.addBands(luasPiksel).addBands(hasil).reduceRegion({
    reducer: ee.Reducer.mean().combine({reducer2: ee.Reducer.sum(), sharedInputs: false})
      .group({groupField: 2, groupName: 'cluster'}),
    geometry: geometry2, scale: 30, maxPixels: 1e9
  }).get('groups'));
  var dipilih = grup.map(function(g) {
    g = ee.Dictionary(g);
    return ee.Algorithms.If(ee.Number(g.get('mean')).gt(0.5), g.get('cluster'), null);
  }, true);
  var mask = hasil.remap(dipilih, ee.List.repeat(1, dipilih.size()), 0).rename('m');
  var luas = mask.multiply(luasPiksel).reduceRegion({
    reducer: ee.Reducer.sum(), geometry: geometry2, scale: 30, maxPixels: 1e9
  }).get('m');
  return {hasil: hasil, mask: mask, info: ee.Dictionary({k: k, seed: seed, dipilih: dipilih, luasHa: luas})};
}

// Pembanding: pilihan visual di task1 (k = 15, seed bawaan 10, cluster 9 dan 11)
var acuan = uji(15, 10);
var visual = acuan.hasil.eq(9).or(acuan.hasil.eq(11)).rename('m');
var luasVisual = visual.multiply(luasPiksel).reduceRegion({
  reducer: ee.Reducer.sum(), geometry: geometry2, scale: 30, maxPixels: 1e9
}).get('m');

function iou(a, b) {
  var s = a.and(b).rename('i').addBands(a.or(b).rename('u')).reduceRegion({
    reducer: ee.Reducer.sum(), geometry: geometry2, scale: 30, maxPixels: 1e9
  });
  return ee.Number(s.get('i')).divide(s.get('u'));
}

var daftarK = [5, 10, 15, 20];
var daftarSeed = [10, 1, 2];
var hasilUji = [];
var warna = {5: 'ffff00', 10: 'ff8c00', 15: 'ff0000', 20: 'ff00ff'};
daftarK.forEach(function(k) {
  daftarSeed.forEach(function(seed) {
    var r = uji(k, seed);
    hasilUji.push(r.info.set('iouAcuan', iou(r.mask, acuan.mask)));
    if (seed === 10) {
      Map.addLayer(r.mask.selfMask(), {palette: [warna[k]]}, 'Kandidat terbangun k=' + k, k === 15);
    }
  });
});

ee.Dictionary({uji: hasilUji, luasVisualHa: luasVisual, iouVisualVsAturan: iou(visual, acuan.mask)})
  .evaluate(function(r, e) { print('TUGAS1 ' + (e ? 'ERR ' + e : JSON.stringify(r))); });
