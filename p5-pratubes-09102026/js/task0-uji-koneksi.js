// Uji koneksi (Task 0)
var koleksi = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')
  .filterDate('2022-01-01', '2022-03-01')
  .limit(1);
print('Jumlah citra:', koleksi.size());
print('Band citra uji:', koleksi.first().bandNames());

// Uji aset GDP/HDI versi 2 yang dipakai Task V
print('GDP v2:', ee.Image('projects/sat-io/open-datasets/GRIDDED_HDI_GDP/GDP_PPP_1990_2015_5arcmin_v2').bandNames().size());
print('HDI v2:', ee.Image('projects/sat-io/open-datasets/GRIDDED_HDI_GDP/HDI_1990_2015_v2').bandNames().size());
