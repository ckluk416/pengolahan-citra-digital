"""Task 0: uji koneksi Earth Engine (padanan js/task0-uji-koneksi.js)."""

import ee

from geeutil import init


def jalankan():
    koleksi = (ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')
               .filterDate('2022-01-01', '2022-03-01')
               .limit(1))
    print('Jumlah citra:', koleksi.size().getInfo())
    print('Band citra uji:', koleksi.first().bandNames().getInfo())

    # Uji aset GDP/HDI versi 2 yang dipakai Task V
    gdp = ee.Image('projects/sat-io/open-datasets/GRIDDED_HDI_GDP/GDP_PPP_1990_2015_5arcmin_v2')
    hdi = ee.Image('projects/sat-io/open-datasets/GRIDDED_HDI_GDP/HDI_1990_2015_v2')
    print('GDP v2:', gdp.bandNames().size().getInfo())
    print('HDI v2:', hdi.bandNames().size().getInfo())


if __name__ == '__main__':
    init()
    jalankan()
