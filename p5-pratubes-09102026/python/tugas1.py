"""Tugas Mandiri 1: sensitivitas clustering, jumlah cluster dan seed (padanan js/tugas1.js)."""

import ee

from geeutil import Peta, init, simpan_json


def jalankan(peta):
    # Data dan wilayah kajian sama dengan Task I
    dataset = (ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')
               .filterBounds(ee.Geometry.Point([112.05730244401117, -6.897418238470722]))
               .filter(ee.Filter.lt('CLOUD_COVER_LAND', 50))
               .sort('CLOUD_COVER_LAND'))
    img = dataset.first()

    geometry2 = ee.Geometry.Polygon(
        [[[111.56510661311408, -7.125131151145682],
          [111.56510661311408, -7.178102498857165],
          [111.62192652888557, -7.178102498857165],
          [111.62192652888557, -7.125131151145682]]], None, False)

    band = ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7']
    img_pilih = img.select(band).clip(geometry2)
    data_training = img_pilih.sample(region=geometry2, scale=30, numPixels=500)

    peta.add_layer(img, {'bands': ['SR_B4', 'SR_B3', 'SR_B2'], 'min': 7061, 'max': 14103}, 'Data paling bersih')
    peta.center_object(geometry2, 14)

    # Acuan pemilihan cluster: ESA WorldCover kelas 50 (terbangun).
    # Cluster dianggap kandidat terbangun kalau lebih dari 50% pikselnya terbangun menurut WorldCover.
    terbangun_wc = ee.ImageCollection('ESA/WorldCover/v200').first().eq(50).rename('wc50')
    luas_piksel = ee.Image.pixelArea().divide(1e4).rename('ha')

    def uji(k, seed):
        model = ee.Clusterer.wekaKMeans(nClusters=k, seed=seed).train(data_training)
        hasil = img_pilih.cluster(model)
        grup = ee.List(terbangun_wc.addBands(luas_piksel).addBands(hasil).reduceRegion(
            reducer=ee.Reducer.mean().combine(reducer2=ee.Reducer.sum(), sharedInputs=False)
            .group(groupField=2, groupName='cluster'),
            geometry=geometry2, scale=30, maxPixels=1e9).get('groups'))
        dipilih = grup.map(
            lambda g: ee.Algorithms.If(ee.Number(ee.Dictionary(g).get('mean')).gt(0.5),
                                       ee.Dictionary(g).get('cluster'), None),
            True)
        mask = hasil.remap(dipilih, ee.List.repeat(1, dipilih.size()), 0).rename('m')
        luas = mask.multiply(luas_piksel).reduceRegion(
            reducer=ee.Reducer.sum(), geometry=geometry2, scale=30, maxPixels=1e9).get('m')
        return hasil, mask, ee.Dictionary({'k': k, 'seed': seed, 'dipilih': dipilih, 'luasHa': luas})

    # Pembanding: pilihan visual di task1 (k = 15, seed bawaan 10, cluster 9 dan 11)
    acuan_hasil, acuan_mask, _ = uji(15, 10)
    visual = acuan_hasil.eq(9).Or(acuan_hasil.eq(11)).rename('m')
    luas_visual = visual.multiply(luas_piksel).reduceRegion(
        reducer=ee.Reducer.sum(), geometry=geometry2, scale=30, maxPixels=1e9).get('m')

    def iou(a, b):
        s = a.And(b).rename('i').addBands(a.Or(b).rename('u')).reduceRegion(
            reducer=ee.Reducer.sum(), geometry=geometry2, scale=30, maxPixels=1e9)
        return ee.Number(s.get('i')).divide(s.get('u'))

    warna = {5: 'ffff00', 10: 'ff8c00', 15: 'ff0000', 20: 'ff00ff'}
    hasil_uji = []
    for k in [5, 10, 15, 20]:
        for seed in [10, 1, 2]:
            _, mask, info = uji(k, seed)
            hasil_uji.append(info.set('iouAcuan', iou(mask, acuan_mask)))
            if seed == 10:
                peta.add_layer(mask.selfMask(), {'palette': [warna[k]]}, f'Kandidat terbangun k={k}', tampil=(k == 15))

    r = ee.Dictionary({'uji': hasil_uji, 'luasVisualHa': luas_visual,
                       'iouVisualVsAturan': iou(visual, acuan_mask)}).getInfo()
    print(f"visual {r['luasVisualHa']:.1f} Ha, IoU visual vs aturan {r['iouVisualVsAturan']:.3f}")
    for u in r['uji']:
        print(f"k={u['k']} seed={u['seed']} dipilih={u['dipilih']} luas={u['luasHa']:.1f} Ha IoU={u['iouAcuan']:.3f}")
    simpan_json('tugas1.json', r)
    return r


if __name__ == '__main__':
    init()
    peta = Peta('Tugas 1')
    jalankan(peta)
    peta.save('tugas1.html')
