// Tugas Mandiri 3: urban sprawl Kota Bandung dan sekitarnya (termasuk Cimahi), 1990-2024
// Kode berasal dari task3 (sudah memakai perbaikan band luas), ROI dan yearList diganti
var roi = ee.Geometry.Rectangle([107.50, -7.02, 107.75, -6.83], null, false);
Map.centerObject(roi, 11);
var l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2');

var l4 = ee.ImageCollection('LANDSAT/LT04/C02/T1_L2');
var l5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2');
var l7 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2');
var l9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2');

var yearList = [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024];   // 2024 ditambahkan

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
  // Perbaikan bug modul: built berisi tahun, jadi pakai built.gt(0)
  var area = built.gt(0).multiply(ee.Image.pixelArea().multiply(0.0001)).rename('area');

  return built.toUint16().rename('built')
    .addBands(area)
    .set('year', year, 'system:time_start', start);
}));

// Peta ekspansi: min lintas tahun = tahun TERAWAL piksel menjadi terbangun
var dict = {
  built_class_values: yearList,
  built_class_palette: ['800080', '0000FF', '00FFFF', '008000', 'FFFF00', 'FFA500', 'FF0000', 'FF1493']
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
    title: 'Urban area Bandung (Ha)',
    hAxis: {title: 'Year', format: '####'},
    vAxis: {title: 'Area (Ha)'}
  });
print(areaChart);

// Angka luas per tahun untuk tabel laporan
builtCol.map(function(img) {
  return ee.Feature(null, {year: img.get('year'), ha: img.select('area').reduceRegion({
    reducer: ee.Reducer.sum(), geometry: roi, scale: 30, maxPixels: 1e10, tileScale: 4}).get('area')});
}).aggregate_array('ha').evaluate(function(r, e) { print('TUGAS3 ' + (e ? 'ERR ' + e : JSON.stringify(r))); });
