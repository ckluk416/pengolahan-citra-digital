// HOTS Problem E: model risiko banjir versi sendiri
// Wilayah: Kota Jambi (FAO GAUL level 2). Batas kecamatan tidak tersedia di katalog GEE,
// jadi dipakai batas kota; ganti `wilayah` dengan poligon kecamatan kalau tersedia.

var titikKota = ee.Geometry.Point([103.61, -1.61]);
var kota = ee.FeatureCollection('FAO/GAUL/2015/level2').filterBounds(titikKota).first();
var wilayah = ee.Feature(kota).geometry();
Map.centerObject(wilayah, 11);

function cloudMask(image) {
  var qa = image.select('QA_PIXEL');
  var mask = qa.bitwiseAnd(1 << 1).eq(0).and(qa.bitwiseAnd(1 << 2).eq(0))
    .and(qa.bitwiseAnd(1 << 3).eq(0)).and(qa.bitwiseAnd(1 << 4).eq(0));
  return image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                      ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
    .multiply(0.0000275).add(-0.2).updateMask(mask);
}
var image = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(wilayah)
  .filterDate('2022-01-01', '2022-12-31').map(cloudMask).median().clip(wilayah);
Map.addLayer(image, {bands: ['B5', 'B6', 'B2'], min: [0.1, 0.05, 0], max: [0.4, 0.3, 0.15]}, 'Komposit 2022', false);

var ndwi = image.normalizedDifference(['B3', 'B5']);
var air = ndwi.gt(0.1);
var bukanAir = air.eq(0);
var ndvi = image.normalizedDifference(['B5', 'B4']).updateMask(bukanAir);

function kelas5(img, ambang, naik) {
  // ambang: 4 batas menaik; naik = true kalau nilai besar berarti harkat besar
  var a = ambang;
  var h = naik
    ? img.where(img.lte(a[0]), 1).where(img.gt(a[0]).and(img.lte(a[1])), 2).where(img.gt(a[1]).and(img.lte(a[2])), 3)
         .where(img.gt(a[2]).and(img.lte(a[3])), 4).where(img.gt(a[3]), 5)
    : img.where(img.gt(a[3]), 1).where(img.gt(a[2]).and(img.lte(a[3])), 2).where(img.gt(a[1]).and(img.lte(a[2])), 3)
         .where(img.gt(a[0]).and(img.lte(a[1])), 4).where(img.lte(a[0]), 5);
  return h.updateMask(bukanAir).clip(wilayah);
}

// ===== Kerawanan =====
// 1. Jarak dari air: ambang dari hasil Problem D (separuh piksel pernah tergenang berjarak > 398 m)
var jarakAir = air.fastDistanceTransform().sqrt().multiply(30).reproject('EPSG:4326', null, 30);
var hJarak = kelas5(jarakAir, [250, 500, 750, 1000], false);
// 2. Elevasi: ambang modul (Tabel 4); di Problem D median piksel pernah tergenang 8 m, tidak tergenang 18,5 m
var srtm = ee.Image('USGS/SRTMGL1_003');
var hElevasi = kelas5(srtm, [5, 10, 15, 20], false);
// 3. Kemiringan lereng (derajat) menggantikan TPI: TPI dari SRTM meter bulat terkuantisasi (Task IV, Problem C).
//    Lahan datar < 1 derajat paling mudah menampung genangan.
var lereng = ee.Terrain.slope(srtm);
var hLereng = kelas5(lereng, [1, 3, 5, 8], false);
// 4. Vegetasi: ambang modul
var hNDVI = kelas5(ndvi, [-0.25, 0, 0.25, 0.5], false);

// ===== Eksposur =====
// Penduduk GHSL: ambang modul (Tabel 6)
var penduduk = ee.ImageCollection('JRC/GHSL/P2023A/GHS_POP').sort('system:time_start', false).first();
var hPenduduk = kelas5(penduduk, [10, 100, 200, 300], true);
// Fraksi lahan terbangun per sel 30 m (cara mean yang benar, lihat Task V)
var fraksiBangun = ee.ImageCollection('ESA/WorldCover/v200').first().eq(50).unmask(0)
  .reduceResolution({reducer: ee.Reducer.mean(), maxPixels: 1024}).reproject('EPSG:4326', null, 30);
var hBangun = kelas5(fraksiBangun, [0.1, 0.3, 0.5, 0.7], true);

// ===== Model dan uji sensitivitas =====
function model(b) {
  var kerawanan = hJarak.multiply(b.jarak).add(hElevasi.multiply(b.elevasi))
    .add(hLereng.multiply(b.lereng)).add(hNDVI.multiply(b.ndvi));
  var eksposur = hPenduduk.add(hBangun).divide(2);
  var risiko = kerawanan.multiply(b.wKerawanan).add(eksposur.multiply(1 - b.wKerawanan));
  return {kerawanan: kerawanan.round(), risiko: risiko.round().clamp(1, 5)};
}
var skema = {
  A_usulan: {jarak: 0.35, elevasi: 0.35, lereng: 0.15, ndvi: 0.15, wKerawanan: 0.6},
  B_bobotSama: {jarak: 0.25, elevasi: 0.25, lereng: 0.25, ndvi: 0.25, wKerawanan: 0.6},
  C_kerawananSetara: {jarak: 0.35, elevasi: 0.35, lereng: 0.15, ndvi: 0.15, wKerawanan: 0.5}
};

var gsw = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence').unmask(0);
var pernahGenang = gsw.gt(0).and(gsw.lt(50)).updateMask(bukanAir).clip(wilayah);
var ha = ee.Image.pixelArea().divide(1e4);
var acuan = model(skema.A_usulan).risiko;

var hasil = {};
Object.keys(skema).forEach(function(nama) {
  var m = model(skema[nama]);
  var luas = ee.List(ha.addBands(m.risiko.rename('k')).reduceRegion({
    reducer: ee.Reducer.sum().group({groupField: 1, groupName: 'kelas'}),
    geometry: wilayah, scale: 30, maxPixels: 1e10, tileScale: 4}).get('groups'));
  var cek = m.kerawanan.gte(4).rename('p').addBands(pernahGenang.rename('g'))
    .addBands(m.risiko.eq(acuan).rename('sama'));
  var s = cek.select('p').and(cek.select('g')).multiply(ha).rename('tp')
    .addBands(cek.select('g').multiply(ha).rename('genang'))
    .addBands(cek.select('p').multiply(ha).rename('rawan45'))
    .addBands(cek.select('sama').multiply(ha).rename('samaDenganA'))
    .addBands(ha.updateMask(bukanAir).clip(wilayah).rename('daratan'))
    .reduceRegion({reducer: ee.Reducer.sum(), geometry: wilayah, scale: 30, maxPixels: 1e10, tileScale: 4});
  hasil[nama] = ee.Dictionary({luasKelas: luas, cek: s});
  if (nama === 'A_usulan') {
    Map.addLayer(m.kerawanan, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'E: kerawanan (usulan)', false);
    Map.addLayer(m.risiko, {min: 1, max: 5, palette: ['green', 'yellow', 'red']}, 'E: risiko (usulan)');
  }
});
Map.addLayer(ee.Image().paint(ee.FeatureCollection([ee.Feature(wilayah)]), 0, 2), {palette: ['black']}, 'Batas Kota Jambi');

// Legenda kelas risiko
var legenda = ui.Panel([ui.Label('Harkat risiko (usulan)')], ui.Panel.Layout.flow('vertical'), {position: 'bottom-left'});
['green', 'yellowgreen', 'yellow', 'orange', 'red'].forEach(function(w, i) {
  legenda.add(ui.Panel([ui.Label('', {width: '18px', height: '18px', backgroundColor: w}), ui.Label(String(i + 1))],
    ui.Panel.Layout.flow('horizontal')));
});
Map.add(legenda);

ee.Dictionary({namaWilayah: ee.Feature(kota).get('ADM2_NAME'), hasil: hasil})
  .evaluate(function(r, e) { print('HOTSE ' + (e ? 'ERR ' + e : JSON.stringify(r))); });
