"""HOTS Problem C (Skala TPI) dan Problem D (Banjir vs Bukan Banjir) (padanan js/hotsCD.js).

Melanjutkan kode task4 (ROI Batanghari).
"""

import ee

from geeutil import Peta, init, simpan_json
import task4


def harkat_tpi(t):
    return (t.where(t.gt(0), 1)
            .where(t.gt(-0.25).And(t.lte(0)), 2)
            .where(t.gt(-0.5).And(t.lte(-0.25)), 3)
            .where(t.gt(-0.75).And(t.lte(-0.5)), 4)
            .where(t.lte(-0.75), 5))


def jalankan(peta):
    v = task4.jalankan(peta)
    roi, bukan_air, srtm = v['roi'], v['bukan_air'], v['srtm']

    # ===== Proksi "pernah tergenang": JRC Global Surface Water 1984-2021 =====
    # occurrence 1-49% = pernah tergenang tapi bukan air permanen. Dipakai karena data titik banjir dari berita tidak tersedia.
    gsw = ee.Image('JRC/GSW1_4/GlobalSurfaceWater')
    occ = gsw.select('occurrence').unmask(0)
    pernah_genang = occ.gt(0).And(occ.lt(50)).updateMask(bukan_air).clip(roi).rename('genang')
    peta.add_layer(pernah_genang.selfMask(), {'palette': ['00ffff']}, 'Proksi pernah tergenang (GSW)', tampil=False)
    ha = ee.Image.pixelArea().divide(1e4)

    # ===== Problem C: skala TPI =====
    hasil_c = []
    for r in [1, 3, 5, 9]:
        t = srtm.subtract(srtm.focalMean(r)).reproject('EPSG:4326', None, 30).updateMask(bukan_air).clip(roi)
        k5 = harkat_tpi(t).eq(5)
        peta.add_layer(k5.selfMask(), {'palette': ['blue']}, f'TPI kelas 5, radius {r}', tampil=False)
        s = (k5.multiply(ha).rename('k5')
             .addBands(k5.And(pernah_genang).multiply(ha).rename('k5Genang'))
             .addBands(pernah_genang.multiply(ha).rename('genang'))
             .addBands(t.lt(0).multiply(ha).rename('negatif'))
             .reduceRegion(reducer=ee.Reducer.sum(), geometry=roi, scale=30, maxPixels=1e10, tileScale=4))
        hasil_c.append(ee.Dictionary(s).set('radius', r))

    # ===== Problem D: validasi kerawanan dengan proksi =====
    kelas = pernah_genang.unmask(0).updateMask(bukan_air).clip(roi).rename('kelas')
    variabel = (v['harkat_kerawanan'].rename('hKerawanan')
                .addBands(v['harkat_jarak_air'].rename('hJarak')).addBands(v['harkat_elevasi'].rename('hElevasi'))
                .addBands(v['harkat_tpi'].rename('hTPI')).addBands(v['harkat_ndvi'].rename('hNDVI'))
                .addBands(v['jarak_air'].rename('jarak')).addBands(srtm.rename('elevasi'))
                .addBands(v['tpi'].rename('tpi')).addBands(v['ndvi'].rename('ndvi')))
    titik_d = kelas.addBands(variabel).stratifiedSample(
        numPoints=10, classBand='kelas', region=roi, scale=30, seed=7, geometries=True, dropNulls=True)
    peta.add_layer(titik_d.filter(ee.Filter.eq('kelas', 1)), {'color': 'cyan'}, 'D: titik pernah tergenang', tampil=False)
    peta.add_layer(titik_d.filter(ee.Filter.eq('kelas', 0)), {'color': 'orange'}, 'D: titik tidak tergenang', tampil=False)
    # Sampel besar untuk melihat variabel mana yang paling memisahkan kedua kelompok
    sampel_besar = kelas.addBands(variabel).stratifiedSample(
        numPoints=300, classBand='kelas', region=roi, scale=30, seed=11, dropNulls=True)
    kolom = ['hKerawanan', 'hJarak', 'hElevasi', 'hTPI', 'hNDVI', 'jarak', 'elevasi', 'tpi', 'ndvi']

    def rata_rata(k):
        return sampel_besar.filter(ee.Filter.eq('kelas', k)).reduceColumns(
            reducer=ee.Reducer.mean().repeat(len(kolom)), selectors=kolom).get('mean')

    def persentil(k, nama_kolom):
        return sampel_besar.filter(ee.Filter.eq('kelas', k)).reduceColumns(
            ee.Reducer.percentile([10, 25, 50, 75, 90]), [nama_kolom])

    r = ee.Dictionary({
        'C': hasil_c,
        'D10': titik_d.map(lambda f: f.set('lonlat', f.geometry().coordinates()))
        .reduceColumns(ee.Reducer.toList(5), ['kelas', 'hKerawanan', 'jarak', 'elevasi', 'lonlat']).get('list'),
        'rata1': rata_rata(1), 'rata0': rata_rata(0),
        'elev1': persentil(1, 'elevasi'), 'elev0': persentil(0, 'elevasi'),
        'jarak1': persentil(1, 'jarak'), 'jarak0': persentil(0, 'jarak'),
    }).getInfo()

    for c in r['C']:
        print(f"C radius {c['radius']}: kelas 5 {c['k5']:,.0f} Ha, pernah tergenang {c['k5Genang']:,.0f} Ha")
    benar = sum(1 for p in r['D10'] if (p[1] >= 4) == (p[0] == 1))
    print(f"D: akurasi 20 titik pada harkat >= 4: {benar}/20")
    print('D: rata-rata pernah tergenang', [round(x, 2) for x in r['rata1']])
    print('D: rata-rata tidak tergenang ', [round(x, 2) for x in r['rata0']])
    simpan_json('hotsCD.json', r)
    return r


if __name__ == '__main__':
    init()
    peta = Peta('HOTS C dan D')
    jalankan(peta)
    peta.save('hotsCD.html')
