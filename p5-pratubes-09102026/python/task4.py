"""Task IV: kerawanan banjir di Batanghari, Jambi (padanan js/task4.js)."""

import ee

from geeutil import Peta, init
from task2 import cloud_mask  # Prasyarat dari Task II: fungsi cloudMask

HIJAU_MERAH = ['green', 'yellow', 'red']


def jalankan(peta):
    roi = ee.Geometry({
        'geodesic': False,
        'type': 'Polygon',
        'coordinates': [[
            [103.47443690212873, -1.7079691352593016],
            [103.7202559939256, -1.7079691352593016],
            [103.7202559939256, -1.469108505971908],
            [103.47443690212873, -1.469108505971908],
            [103.47443690212873, -1.7079691352593016]
        ]]
    })

    filtered = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                .filterBounds(roi)
                .filterDate('2022-01-01', '2022-12-31'))

    image = filtered.map(cloud_mask).median().clip(roi)

    peta.add_layer(image, {'bands': ['B5', 'B6', 'B2'], 'min': [0.1, 0.05, 0], 'max': [0.4, 0.3, 0.15]}, 'Image')
    peta.center_object(roi, 11)

    band_map = {
        'NIR': image.select('B5'), 'SWIR': image.select('B6'), 'GREEN': image.select('B3'),
        'RED': image.select('B4'), 'BLUE': image.select('B2'),
    }

    # Badan air
    ndwi = image.expression('(GREEN - NIR) / (GREEN + NIR)', band_map)
    air = ndwi.gt(0.1)
    bukan_air = air.eq(0)
    # Tambahan (bukan dari modul): layer NDWI untuk Gambar 10
    peta.add_layer(ndwi, {'min': -1, 'max': 1, 'palette': ['red', 'white', 'blue']}, 'NDWI', tampil=False)
    peta.add_layer(air, {'palette': ['black', 'blue'], 'min': 0, 'max': 1}, 'Air', tampil=False)

    # Jarak dari air (meter)
    jarak_air = (air.fastDistanceTransform()
                 .sqrt().multiply(30)      # jarak kuadrat-piksel -> meter
                 .updateMask(bukan_air)
                 .clip(roi)
                 .reproject('EPSG:4326', None, 30))
    peta.add_layer(jarak_air, {'min': 0, 'max': 1000, 'palette': ['red', 'yellow', 'green']}, 'Jarak dari air',
                   tampil=False)

    # Harkat jarak (Tabel 4)
    harkat_jarak_air = (jarak_air.where(jarak_air.gt(200), 1)
                        .where(jarak_air.gt(150).And(jarak_air.lte(200)), 2)
                        .where(jarak_air.gt(100).And(jarak_air.lte(150)), 3)
                        .where(jarak_air.gt(50).And(jarak_air.lte(100)), 4)
                        .where(jarak_air.lte(50), 5))
    peta.add_layer(harkat_jarak_air, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat jarak dari air',
                   tampil=False)

    # Elevasi
    srtm = ee.Image('USGS/SRTMGL1_003').clip(roi).updateMask(bukan_air)
    peta.add_layer(srtm, {'min': 0, 'max': 200, 'palette': HIJAU_MERAH}, 'Elevasi', tampil=False)

    harkat_elevasi = (srtm.where(srtm.gt(20), 1)
                      .where(srtm.gt(15).And(srtm.lte(20)), 2)
                      .where(srtm.gt(10).And(srtm.lte(15)), 3)
                      .where(srtm.gt(5).And(srtm.lte(10)), 4)
                      .where(srtm.lte(5), 5))
    peta.add_layer(harkat_elevasi, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat elevasi', tampil=False)

    # TPI = elevasi dikurangi rata-rata elevasi lingkungannya
    tpi = (srtm.subtract(srtm.focalMean(3))
           .reproject('EPSG:4326', None, 30)
           .updateMask(bukan_air)
           .clip(roi))
    peta.add_layer(tpi, {'min': -10, 'max': 10, 'palette': ['blue', 'yellow', 'red']}, 'TPI', tampil=False)

    harkat_tpi = (tpi.where(tpi.gt(0), 1)
                  .where(tpi.gt(-0.25).And(tpi.lte(0)), 2)
                  .where(tpi.gt(-0.5).And(tpi.lte(-0.25)), 3)
                  .where(tpi.gt(-0.75).And(tpi.lte(-0.5)), 4)
                  .where(tpi.lte(-0.75), 5))
    peta.add_layer(harkat_tpi, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat TPI', tampil=False)

    # Vegetasi
    ndvi = image.expression('(NIR - RED) / (NIR + RED)', band_map).updateMask(bukan_air)
    peta.add_layer(ndvi, {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI', tampil=False)

    harkat_ndvi = (ndvi.where(ndvi.gt(0.5), 1)
                   .where(ndvi.gt(0.25).And(ndvi.lte(0.5)), 2)
                   .where(ndvi.gt(0).And(ndvi.lte(0.25)), 3)
                   .where(ndvi.gt(-0.25).And(ndvi.lte(0)), 4)
                   .where(ndvi.lte(-0.25), 5))
    peta.add_layer(harkat_ndvi, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat NDVI', tampil=False)

    # Jumlah harkat keempat variabel (4 s.d. 20) lalu harkat kembali (Tabel 5)
    kerawanan = harkat_jarak_air.add(harkat_elevasi).add(harkat_tpi).add(harkat_ndvi)
    peta.add_layer(kerawanan, {'min': 1, 'max': 20, 'palette': HIJAU_MERAH}, 'Kerawanan', tampil=False)

    harkat_kerawanan = (kerawanan.where(kerawanan.gt(16), 5)
                        .where(kerawanan.gt(12).And(kerawanan.lte(16)), 4)
                        .where(kerawanan.gt(8).And(kerawanan.lte(12)), 3)
                        .where(kerawanan.gt(4).And(kerawanan.lte(8)), 2)
                        .where(kerawanan.lte(4), 1))
    peta.add_layer(harkat_kerawanan, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat kerawanan',
                   tampil=False)
    return locals()


if __name__ == '__main__':
    init()
    peta = Peta('Task IV')
    jalankan(peta)
    peta.save('task4.html')
