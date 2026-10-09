"""HOTS Problem A (Detektif Bit QA) dan Problem B (Duel Indeks Air) (padanan js/hotsAB.js)."""

import ee

from geeutil import Peta, init, simpan_json


def skala(image):
    return (image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                         ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
            .multiply(0.0000275).add(-0.2))


def jumlah_bit(image):
    """Jumlah bit curiga yang menyala (dilated, cirrus, cloud, shadow): 0 s.d. 4."""
    qa = image.select('QA_PIXEL')
    return (qa.bitwiseAnd(1 << 1).gt(0)
            .add(qa.bitwiseAnd(1 << 2).gt(0))
            .add(qa.bitwiseAnd(1 << 3).gt(0))
            .add(qa.bitwiseAnd(1 << 4).gt(0)))


def cloud_mask(image):
    """Mask modul: tolak kalau minimal satu bit menyala."""
    return skala(image).updateMask(jumlah_bit(image).eq(0))


def mask_awan_kustom(image):
    """Problem A: tolak hanya kalau minimal dua bit menyala."""
    return skala(image).updateMask(jumlah_bit(image).lt(2))


def jalankan(peta):
    # Wilayah dan koleksi sama dengan Task II: Jabodetabekpunjur, Landsat 8 tahun 2022
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
    filtered = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(roi).filterDate('2022-01-01', '2022-12-31')

    # ===== Problem A =====
    valid_modul = filtered.map(lambda img: jumlah_bit(img).eq(0).rename('v')).sum()
    valid_kustom = filtered.map(lambda img: jumlah_bit(img).lt(2).rename('v')).sum()

    def satu_bit(bit):
        """Dari observasi yang diselamatkan mask kustom (tepat satu bit), bit mana yang menyala."""
        return filtered.map(
            lambda img: jumlah_bit(img).eq(1).And(img.select('QA_PIXEL').bitwiseAnd(1 << bit).gt(0)).rename('v')
        ).sum()

    median_modul = filtered.map(cloud_mask).median().clip(roi)
    median_kustom = filtered.map(mask_awan_kustom).median().clip(roi)
    vis_komposit = {'bands': ['B5', 'B6', 'B2'], 'min': [0.1, 0.05, 0], 'max': [0.4, 0.3, 0.15]}
    peta.center_object(roi, 10)
    peta.add_layer(median_modul, vis_komposit, 'A: komposit mask modul', tampil=False)
    peta.add_layer(median_kustom, vis_komposit, 'A: komposit mask kustom', tampil=False)
    peta.add_layer(valid_kustom.subtract(valid_modul).clip(roi), {'min': 0, 'max': 20, 'palette': ['white', 'orange', 'red']},
                   'A: tambahan observasi valid', tampil=False)

    stat_a = (valid_modul.rename('modul')
              .addBands(valid_kustom.rename('kustom'))
              .addBands(satu_bit(1).rename('hanyaDilated'))
              .addBands(satu_bit(2).rename('hanyaCirrus'))
              .addBands(satu_bit(3).rename('hanyaCloud'))
              .addBands(satu_bit(4).rename('hanyaShadow'))
              .reduceRegion(reducer=ee.Reducer.mean(), geometry=roi, scale=90, maxPixels=1e10, tileScale=4))
    # Kecerahan biru komposit sebagai indikator sisa awan (awan terang di band biru)
    biru = (median_modul.select('B2').rename('modul').addBands(median_kustom.select('B2').rename('kustom'))
            .reduceRegion(reducer=ee.Reducer.percentile([50, 99]), geometry=roi, scale=90, maxPixels=1e10, tileScale=4))

    # ===== Problem B: NDWI vs MNDWI pada komposit yang sama (komposit mask modul) =====
    ndwi = median_modul.normalizedDifference(['B3', 'B5']).rename('ndwi')    # (GREEN - NIR) / (GREEN + NIR)
    mndwi = median_modul.normalizedDifference(['B3', 'B6']).rename('mndwi')  # (GREEN - SWIR1) / (GREEN + SWIR1)
    air_ndwi = ndwi.gt(0.1)
    air_mndwi = mndwi.gt(0.1)
    hanya_ndwi = air_ndwi.And(air_mndwi.Not())
    hanya_mndwi = air_mndwi.And(air_ndwi.Not())

    peta.add_layer(median_modul, vis_komposit, 'B: komposit')
    peta.add_layer(air_ndwi.And(air_mndwi).selfMask(), {'palette': 'blue'}, 'B: air menurut keduanya')
    peta.add_layer(hanya_ndwi.selfMask(), {'palette': 'red'}, 'B: air hanya menurut NDWI')
    peta.add_layer(hanya_mndwi.selfMask(), {'palette': 'yellow'}, 'B: air hanya menurut MNDWI')

    ha = ee.Image.pixelArea().divide(1e4)
    stat_b = (air_ndwi.multiply(ha).rename('ndwi')
              .addBands(air_mndwi.multiply(ha).rename('mndwi'))
              .addBands(hanya_ndwi.multiply(ha).rename('hanyaNdwi'))
              .addBands(hanya_mndwi.multiply(ha).rename('hanyaMndwi'))
              .reduceRegion(reducer=ee.Reducer.sum(), geometry=roi, scale=30, maxPixels=1e10, tileScale=4))

    # Tutupan lahan (WorldCover) di area yang diperdebatkan
    wc = ee.ImageCollection('ESA/WorldCover/v200').first().rename('wc')

    def luas_per_kelas(mask_img):
        return ee.List(ha.updateMask(mask_img).addBands(wc).reduceRegion(
            reducer=ee.Reducer.sum().group(groupField=1, groupName='kelas'),
            geometry=roi, scale=30, maxPixels=1e10, tileScale=4).get('groups'))

    r = ee.Dictionary({
        'jumlahCitra': filtered.size(), 'A': stat_a, 'biruB2': biru,
        'B': stat_b, 'wcHanyaNdwi': luas_per_kelas(hanya_ndwi), 'wcHanyaMndwi': luas_per_kelas(hanya_mndwi),
    }).getInfo()
    a = r['A']
    print(f"A: {r['jumlahCitra']} citra; observasi valid per piksel modul {a['modul']:.2f}, kustom {a['kustom']:.2f}")
    print(f"   diselamatkan: cloud {a['hanyaCloud']:.2f}, cirrus {a['hanyaCirrus']:.2f}, "
          f"shadow {a['hanyaShadow']:.2f}, dilated {a['hanyaDilated']:.2f}")
    print('   band biru komposit:', {k: round(x, 4) for k, x in r['biruB2'].items()})
    print('B:', {k: round(x) for k, x in r['B'].items()}, '(Ha)')
    simpan_json('hotsAB.json', r)
    return r


if __name__ == '__main__':
    init()
    peta = Peta('HOTS A dan B')
    jalankan(peta)
    peta.save('hotsAB.html')
