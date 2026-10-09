"""Task II: cloud masking, komposit median, NDBI/NDWI, thresholding (padanan js/task2.js)."""

import ee

from geeutil import Peta, init


def cloud_mask(image):
    qa = image.select('QA_PIXEL')      # band penanda kualitas piksel
    dilated = 1 << 1                   # bit 1: awan melebar
    cirrus = 1 << 2                    # bit 2: awan cirrus (tipis)
    cloud = 1 << 3                     # bit 3: awan
    shadow = 1 << 4                    # bit 4: bayangan awan
    mask = (qa.bitwiseAnd(dilated).eq(0)
            .And(qa.bitwiseAnd(cirrus).eq(0))
            .And(qa.bitwiseAnd(cloud).eq(0))
            .And(qa.bitwiseAnd(shadow).eq(0)))
    rename = image.select(
        ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
    scaled = rename.multiply(0.0000275).add(-0.2)
    return scaled.updateMask(mask)


def jalankan(peta):
    # ROI Jabodetabekpunjur
    roi = ee.Geometry({
        'geodesic': False,
        'type': 'Polygon',
        'coordinates': [[
            [106.53598136542733, -6.6221756519036195],
            [107.23910636542733, -6.6221756519036195],
            [107.23910636542733, -5.928728445061094],
            [106.53598136542733, -5.928728445061094],
            [106.53598136542733, -6.6221756519036195]
        ]]
    })

    l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    filtered = l8.filterBounds(roi).filterDate('2022-01-01', '2022-12-31')

    # Terapkan ke seluruh koleksi + komposit median
    median = filtered.map(cloud_mask).median().clip(roi)

    # Tampilkan komposit warna palsu: NIR-SWIR-Biru
    peta.add_layer(median, {'bands': ['B5', 'B6', 'B2'], 'min': [0.1, 0.05, 0], 'max': [0.4, 0.3, 0.15]}, 'Image')
    peta.center_object(roi, 9)

    # Kamus nama variabel -> band citra
    band_map = {
        'NIR': median.select('B5'),
        'SWIR': median.select('B6'),
        'GREEN': median.select('B3'),
    }

    # NDBI: positif = kecenderungan terbangun
    ndbi = median.expression('(SWIR - NIR) / (SWIR + NIR)', band_map)
    peta.add_layer(ndbi, {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'red']}, 'NDBI')

    # NDWI: positif = kecenderungan air
    ndwi = median.expression('(GREEN - NIR) / (GREEN + NIR)', band_map)
    peta.add_layer(ndwi, {'min': -1, 'max': 1, 'palette': ['red', 'white', 'blue']}, 'NDWI')

    # Thresholding
    air = ndwi.gt(0.1)                       # air = NDWI > 0.1
    peta.add_layer(air.selfMask(), {'palette': 'blue'}, 'Air')

    bangunan = ndbi.gt(-0.1).And(air.eq(0))  # NDBI > -0.1 dan bukan air
    peta.add_layer(bangunan.selfMask(), {'palette': 'red'}, 'Bangunan')
    return locals()


if __name__ == '__main__':
    init()
    peta = Peta('Task II')
    jalankan(peta)
    peta.save('task2.html')
