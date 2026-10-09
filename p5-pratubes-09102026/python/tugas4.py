"""Tugas Mandiri 4: risiko tiga komponen (padanan js/tugas4.js = task5.js + kode Tugas 4)."""

import ee

from geeutil import Peta, init, simpan_json
import task5

HIJAU_MERAH = task5.HIJAU_MERAH


def jalankan(peta):
    v = task5.jalankan(peta)
    roi = v['roi']

    # Kerentanan diaktifkan: jumlah harkat 3 s.d. 15, diharkat ulang mengikuti Tabel 10
    risiko3 = v['harkat_kerawanan'].add(v['harkat_eksposur']).add(v['harkat_kerentanan'])
    peta.add_layer(risiko3, {'min': 3, 'max': 15, 'palette': HIJAU_MERAH}, 'Risiko 3 komponen', tampil=False)

    harkat_risiko3 = (risiko3.where(risiko3.gt(12), 5)
                      .where(risiko3.gt(9).And(risiko3.lte(12)), 4)
                      .where(risiko3.gt(6).And(risiko3.lte(9)), 3)
                      .where(risiko3.gte(3).And(risiko3.lte(6)), 2)
                      .where(risiko3.lt(3), 1))
    peta.add_layer(harkat_risiko3, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat risiko 3 komponen',
                   tampil=False)

    # Luas tiap kelas (Ha) untuk versi 2 komponen (modul) dan 3 komponen
    ha_piksel = ee.Image.pixelArea().divide(1e4)

    def luas_kelas(img):
        return ee.List(ha_piksel.addBands(img.rename('k')).reduceRegion(
            reducer=ee.Reducer.sum().group(groupField=1, groupName='kelas'),
            geometry=roi, scale=30, maxPixels=1e10, tileScale=4).get('groups'))

    # Perpindahan kelas: kode = kelas 2 komponen * 10 + kelas 3 komponen
    pindah = v['harkat_risiko'].multiply(10).add(harkat_risiko3)
    r = ee.Dictionary({
        'duaKomponen': luas_kelas(v['harkat_risiko']),
        'tigaKomponen': luas_kelas(harkat_risiko3),
        'perpindahan': luas_kelas(pindah),
    }).getInfo()
    for kunci, grup in r.items():
        print(kunci, ', '.join(f"{int(g['kelas'])}: {g['sum']:,.0f} Ha" for g in grup))
    simpan_json('tugas4.json', r)
    return r


if __name__ == '__main__':
    init()
    peta = Peta('Tugas 4')
    jalankan(peta)
    peta.save('tugas4.html')
