"""Tugas Mandiri 2: kalibrasi ambangan NDBI (padanan js/tugas2.js = task2.js + kode Tugas 2)."""

import ee

from geeutil import Peta, init, simpan_json
import task2


def jalankan(peta):
    v = task2.jalankan(peta)
    ndbi, air, bangunan, roi = v['ndbi'], v['air'], v['bangunan'], v['roi']

    # Sepuluh titik Inspector dari Task II, sudah dicek di basemap Satellite
    data_titik = [
        ('T1', 'terbangun', [106.86540, -6.28235]), ('T2', 'terbangun', [106.85682, -6.33354]),
        ('T3', 'terbangun', [106.84223, -6.31733]), ('T4', 'terbangun', [106.91573, -6.29348]),
        ('T5', 'terbangun', [106.86234, -6.28717]), ('V1', 'bukan', [106.82163, -6.31136]),
        ('V2', 'bukan', [106.81994, -6.30935]), ('V3', 'bukan', [106.91089, -6.32501]),
        ('V4', 'bukan', [106.88929, -6.28427]), ('V5', 'bukan', [106.90818, -6.32812]),
    ]
    titik = ee.FeatureCollection([ee.Feature(ee.Geometry.Point(xy), {'id': i, 'kelas': k}) for i, k, xy in data_titik])
    nilai_titik = ndbi.rename('ndbi').sampleRegions(collection=titik, scale=30)
    print('NDBI di titik kalibrasi:')
    for f in nilai_titik.getInfo()['features']:
        p = f['properties']
        print(f"  {p['id']} ({p['kelas']}): {p['ndbi']:.3f}")

    # Ambang baru = titik tengah antara NDBI terendah titik terbangun (0.076)
    # dan NDBI tertinggi titik bukan terbangun (-0.107), dibulatkan: -0.02
    ambang_baru = -0.02
    bangunan_baru = ndbi.gt(ambang_baru).And(air.eq(0))
    peta.add_layer(bangunan_baru.selfMask(), {'palette': 'orange'}, 'Bangunan (ambang -0.02)', tampil=False)

    # Piksel yang hilang saat ambang dinaikkan dari -0.1 ke -0.02
    hilang = bangunan.And(bangunan_baru.Not())
    peta.add_layer(hilang.selfMask(), {'palette': 'cyan'}, 'Hilang saat ambang dinaikkan', tampil=False)

    ha = ee.Image.pixelArea().divide(1e4)
    luas = (bangunan.multiply(ha).rename('lama')
            .addBands(bangunan_baru.multiply(ha).rename('baru'))
            .reduceRegion(reducer=ee.Reducer.sum(), geometry=roi, scale=30, maxPixels=1e10, tileScale=4)
            .getInfo())
    print(f"Luas terbangun ambang -0.1: {luas['lama']:,.0f} Ha; ambang -0.02: {luas['baru']:,.0f} Ha")
    simpan_json('tugas2.json', luas)
    return luas


if __name__ == '__main__':
    init()
    peta = Peta('Tugas 2')
    jalankan(peta)
    peta.save('tugas2.html')
