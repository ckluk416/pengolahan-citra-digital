"""HOTS Problem E: model risiko banjir versi sendiri (padanan js/hotsE.js).

Wilayah: Kota Jambi (FAO GAUL level 2). Batas kecamatan tidak tersedia di katalog GEE,
jadi dipakai batas kota; ganti `wilayah` dengan poligon kecamatan kalau tersedia.
"""

import ee

from geeutil import Peta, init, simpan_json


def cloud_mask(image):
    qa = image.select('QA_PIXEL')
    mask = (qa.bitwiseAnd(1 << 1).eq(0).And(qa.bitwiseAnd(1 << 2).eq(0))
            .And(qa.bitwiseAnd(1 << 3).eq(0)).And(qa.bitwiseAnd(1 << 4).eq(0)))
    return (image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                         ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
            .multiply(0.0000275).add(-0.2).updateMask(mask))


def jalankan(peta):
    titik_kota = ee.Geometry.Point([103.61, -1.61])
    kota = ee.FeatureCollection('FAO/GAUL/2015/level2').filterBounds(titik_kota).first()
    wilayah = ee.Feature(kota).geometry()
    peta.center_object(wilayah, 12)

    image = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(wilayah)
             .filterDate('2022-01-01', '2022-12-31').map(cloud_mask).median().clip(wilayah))
    peta.add_layer(image, {'bands': ['B5', 'B6', 'B2'], 'min': [0.1, 0.05, 0], 'max': [0.4, 0.3, 0.15]},
                   'Komposit 2022', tampil=False)

    ndwi = image.normalizedDifference(['B3', 'B5'])
    air = ndwi.gt(0.1)
    bukan_air = air.eq(0)
    ndvi = image.normalizedDifference(['B5', 'B4']).updateMask(bukan_air)

    def kelas5(img, a, naik):
        """a: 4 batas menaik; naik = True kalau nilai besar berarti harkat besar."""
        if naik:
            h = (img.where(img.lte(a[0]), 1).where(img.gt(a[0]).And(img.lte(a[1])), 2)
                 .where(img.gt(a[1]).And(img.lte(a[2])), 3).where(img.gt(a[2]).And(img.lte(a[3])), 4)
                 .where(img.gt(a[3]), 5))
        else:
            h = (img.where(img.gt(a[3]), 1).where(img.gt(a[2]).And(img.lte(a[3])), 2)
                 .where(img.gt(a[1]).And(img.lte(a[2])), 3).where(img.gt(a[0]).And(img.lte(a[1])), 4)
                 .where(img.lte(a[0]), 5))
        return h.updateMask(bukan_air).clip(wilayah)

    # ===== Kerawanan =====
    # 1. Jarak dari air: ambang dari hasil Problem D (separuh piksel pernah tergenang berjarak > 398 m)
    jarak_air = air.fastDistanceTransform().sqrt().multiply(30).reproject('EPSG:4326', None, 30)
    h_jarak = kelas5(jarak_air, [250, 500, 750, 1000], False)
    # 2. Elevasi: ambang modul (Tabel 4); di Problem D median piksel pernah tergenang 8 m, tidak tergenang 18,5 m
    srtm = ee.Image('USGS/SRTMGL1_003')
    h_elevasi = kelas5(srtm, [5, 10, 15, 20], False)
    # 3. Kemiringan lereng (derajat) menggantikan TPI: TPI dari SRTM meter bulat terkuantisasi (Task IV, Problem C).
    lereng = ee.Terrain.slope(srtm)
    h_lereng = kelas5(lereng, [1, 3, 5, 8], False)
    # 4. Vegetasi: ambang modul
    h_ndvi = kelas5(ndvi, [-0.25, 0, 0.25, 0.5], False)

    # ===== Eksposur =====
    penduduk = ee.ImageCollection('JRC/GHSL/P2023A/GHS_POP').sort('system:time_start', False).first()
    h_penduduk = kelas5(penduduk, [10, 100, 200, 300], True)
    # Fraksi lahan terbangun per sel 30 m (cara mean yang benar, lihat Task V)
    fraksi_bangun = (ee.ImageCollection('ESA/WorldCover/v200').first().eq(50).unmask(0)
                     .reduceResolution(reducer=ee.Reducer.mean(), maxPixels=1024)
                     .reproject('EPSG:4326', None, 30))
    h_bangun = kelas5(fraksi_bangun, [0.1, 0.3, 0.5, 0.7], True)

    # ===== Model dan uji sensitivitas =====
    def model(b):
        kerawanan = (h_jarak.multiply(b['jarak']).add(h_elevasi.multiply(b['elevasi']))
                     .add(h_lereng.multiply(b['lereng'])).add(h_ndvi.multiply(b['ndvi'])))
        eksposur = h_penduduk.add(h_bangun).divide(2)
        risiko = kerawanan.multiply(b['wKerawanan']).add(eksposur.multiply(1 - b['wKerawanan']))
        return kerawanan.round(), risiko.round().clamp(1, 5)

    skema = {
        'A_usulan': {'jarak': 0.35, 'elevasi': 0.35, 'lereng': 0.15, 'ndvi': 0.15, 'wKerawanan': 0.6},
        'B_bobotSama': {'jarak': 0.25, 'elevasi': 0.25, 'lereng': 0.25, 'ndvi': 0.25, 'wKerawanan': 0.6},
        'C_kerawananSetara': {'jarak': 0.35, 'elevasi': 0.35, 'lereng': 0.15, 'ndvi': 0.15, 'wKerawanan': 0.5},
    }

    gsw = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence').unmask(0)
    pernah_genang = gsw.gt(0).And(gsw.lt(50)).updateMask(bukan_air).clip(wilayah)
    ha = ee.Image.pixelArea().divide(1e4)
    _, acuan = model(skema['A_usulan'])

    hasil = {}
    for nama, bobot in skema.items():
        kerawanan, risiko = model(bobot)
        luas = ee.List(ha.addBands(risiko.rename('k')).reduceRegion(
            reducer=ee.Reducer.sum().group(groupField=1, groupName='kelas'),
            geometry=wilayah, scale=30, maxPixels=1e10, tileScale=4).get('groups'))
        cek = kerawanan.gte(4).rename('p').addBands(pernah_genang.rename('g')).addBands(risiko.eq(acuan).rename('sama'))
        s = (cek.select('p').And(cek.select('g')).multiply(ha).rename('tp')
             .addBands(cek.select('g').multiply(ha).rename('genang'))
             .addBands(cek.select('p').multiply(ha).rename('rawan45'))
             .addBands(cek.select('sama').multiply(ha).rename('samaDenganA'))
             .addBands(ha.updateMask(bukan_air).clip(wilayah).rename('daratan'))
             .reduceRegion(reducer=ee.Reducer.sum(), geometry=wilayah, scale=30, maxPixels=1e10, tileScale=4))
        hasil[nama] = ee.Dictionary({'luasKelas': luas, 'cek': s})
        if nama == 'A_usulan':
            peta.add_layer(kerawanan, {'min': 1, 'max': 5, 'palette': ['green', 'yellow', 'red']},
                           'E: kerawanan (usulan)', tampil=False)
            peta.add_layer(risiko, {'min': 1, 'max': 5, 'palette': ['green', 'yellow', 'red']}, 'E: risiko (usulan)')
    peta.add_layer(ee.FeatureCollection([ee.Feature(wilayah)]), {'color': '000000'}, 'Batas Kota Jambi')

    # Legenda kelas risiko
    peta.add_legend('Harkat risiko (usulan)', ['1', '2', '3', '4', '5'],
                    ['green', 'yellowgreen', 'yellow', 'orange', 'red'])

    r = ee.Dictionary({'namaWilayah': ee.Feature(kota).get('ADM2_NAME'), 'hasil': hasil}).getInfo()
    print('Wilayah:', r['namaWilayah'])
    for nama, h in r['hasil'].items():
        c = h['cek']
        kelas = ', '.join(f"{int(g['kelas'])}: {g['sum']:,.0f}" for g in h['luasKelas'])
        print(f"{nama}: kelas (Ha) {kelas}; recall {c['tp'] / c['genang']:.1%}, presisi {c['tp'] / c['rawan45']:.1%}, "
              f"sama dengan A {c['samaDenganA'] / c['daratan']:.1%}")
    simpan_json('hotsE.json', r)
    return r


if __name__ == '__main__':
    init()
    peta = Peta('HOTS E')
    jalankan(peta)
    peta.save('hotsE.html')
