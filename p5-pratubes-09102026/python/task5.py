"""Task V: eksposur, kerentanan, dan risiko banjir (padanan js/task5.js).

Melanjutkan Task IV, sama seperti task5.js = isi task4.js + kode Task V.
Kode reduceResolution(sum) dibiarkan seperti modul; bug-nya dibahas di laporan.
"""

import ee

from geeutil import Peta, init
import task4

HIJAU_MERAH = task4.HIJAU_MERAH


def jalankan(peta):
    v = task4.jalankan(peta)
    roi, bukan_air = v['roi'], v['bukan_air']
    harkat_kerawanan = v['harkat_kerawanan']

    # ===== Task V: eksposur, kerentanan, dan risiko (melanjutkan Task IV) =====
    penduduk = (ee.ImageCollection('JRC/GHSL/P2023A/GHS_POP')
                .sort('system:time_start', False)
                .first().updateMask(bukan_air).clip(roi))
    peta.add_layer(penduduk, {'min': 0, 'max': 250, 'palette': ['black', 'red', 'white']}, 'Penduduk', tampil=False)

    harkat_penduduk = (penduduk.where(penduduk.gt(300), 5)
                       .where(penduduk.gt(200).And(penduduk.lte(300)), 4)
                       .where(penduduk.gt(100).And(penduduk.lte(200)), 3)
                       .where(penduduk.gt(10).And(penduduk.lte(100)), 2)
                       .where(penduduk.lte(10), 1))
    peta.add_layer(harkat_penduduk, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat penduduk', tampil=False)

    wc = ee.ImageCollection('ESA/WorldCover/v200').first().clip(roi).updateMask(bukan_air)

    lahan_terbangun = wc.eq(50)   # kelas 50 = built-up
    pertanian = wc.eq(40)         # kelas 40 = cropland

    area = ee.Image.pixelArea()

    # Luas terbangun per piksel 30 m (m persegi)
    lahan_terbangun_area = (lahan_terbangun.multiply(area)
                            .reduceResolution(ee.Reducer.sum(), True)
                            .reproject('EPSG:4326', None, 30))
    peta.add_layer(lahan_terbangun_area, {'min': 0, 'max': 100, 'palette': ['black', 'red', 'white']},
                   'Luas lahan terbangun', tampil=False)

    harkat_lahan_terbangun = (lahan_terbangun_area.where(lahan_terbangun_area.gt(100), 5)
                              .where(lahan_terbangun_area.gt(80).And(lahan_terbangun_area.lte(100)), 4)
                              .where(lahan_terbangun_area.gt(60).And(lahan_terbangun_area.lte(80)), 3)
                              .where(lahan_terbangun_area.gt(40).And(lahan_terbangun_area.lte(60)), 2)
                              .where(lahan_terbangun_area.lte(40), 1))
    # Tambahan (bukan dari modul): layer untuk Gambar 17
    peta.add_layer(harkat_lahan_terbangun, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat lahan terbangun',
                   tampil=False)

    # Luas pertanian per piksel 30 m + harkat
    pertanian_area = (pertanian.multiply(area)
                      .reduceResolution(ee.Reducer.sum(), True)
                      .reproject('EPSG:4326', None, 30))
    # Tambahan (bukan dari modul): layer untuk Gambar 18
    peta.add_layer(pertanian_area, {'min': 0, 'max': 100, 'palette': ['black', 'green', 'white']}, 'Luas pertanian',
                   tampil=False)

    harkat_pertanian = (pertanian_area.where(pertanian_area.gt(100), 5)
                        .where(pertanian_area.gt(80).And(pertanian_area.lte(100)), 4)
                        .where(pertanian_area.gt(60).And(pertanian_area.lte(80)), 3)
                        .where(pertanian_area.gt(40).And(pertanian_area.lte(60)), 2)
                        .where(pertanian_area.lte(40), 1))
    peta.add_layer(harkat_pertanian, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat pertanian', tampil=False)

    eksposur = harkat_penduduk.add(harkat_lahan_terbangun).add(harkat_pertanian)
    peta.add_layer(eksposur, {'min': 1, 'max': 15, 'palette': HIJAU_MERAH}, 'Eksposur', tampil=False)

    harkat_eksposur = (eksposur.where(eksposur.gt(12), 5)
                       .where(eksposur.gt(9).And(eksposur.lte(12)), 4)
                       .where(eksposur.gt(6).And(eksposur.lte(9)), 3)
                       .where(eksposur.gt(3).And(eksposur.lte(6)), 2)
                       .where(eksposur.lte(3), 1))
    peta.add_layer(harkat_eksposur, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat eksposur', tampil=False)

    # PDB per piksel (USD)
    pdb = (ee.Image('projects/sat-io/open-datasets/GRIDDED_HDI_GDP/GDP_PPP_1990_2015_5arcmin_v2')
           .select('b26').clip(roi).updateMask(bukan_air))
    peta.add_layer(pdb, {'min': 0, 'max': 1e8, 'palette': ['black', 'green', 'white']}, 'PDB', tampil=False)

    harkat_pdb = (pdb.where(pdb.gt(40 * 1e6), 1)
                  .where(pdb.gt(30 * 1e6).And(pdb.lte(40 * 1e6)), 2)
                  .where(pdb.gt(20 * 1e6).And(pdb.lte(30 * 1e6)), 3)
                  .where(pdb.gt(10 * 1e6).And(pdb.lte(20 * 1e6)), 4)
                  .where(pdb.lte(10 * 1e6), 5))
    peta.add_layer(harkat_pdb, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat PDB', tampil=False)

    # IPM (0--1)
    ipm = (ee.Image('projects/sat-io/open-datasets/GRIDDED_HDI_GDP/HDI_1990_2015_v2')
           .select('b26').clip(roi).updateMask(bukan_air))
    peta.add_layer(ipm, {'min': 0.5, 'max': 1, 'palette': ['black', 'blue', 'white']}, 'IPM', tampil=False)

    harkat_ipm = (ipm.where(ipm.gt(0.85), 1)
                  .where(ipm.gt(0.8).And(ipm.lte(0.85)), 2)
                  .where(ipm.gt(0.75).And(ipm.lte(0.8)), 3)
                  .where(ipm.gt(0.7).And(ipm.lte(0.75)), 4)
                  .where(ipm.lte(0.7), 5))
    peta.add_layer(harkat_ipm, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat IPM', tampil=False)

    kerentanan = harkat_pdb.add(harkat_ipm)
    peta.add_layer(kerentanan, {'min': 1, 'max': 10, 'palette': HIJAU_MERAH}, 'Kerentanan', tampil=False)

    harkat_kerentanan = (kerentanan.where(kerentanan.gt(8), 5)
                         .where(kerentanan.gt(6).And(kerentanan.lte(8)), 4)
                         .where(kerentanan.gt(4).And(kerentanan.lte(6)), 3)
                         .where(kerentanan.gt(2).And(kerentanan.lte(4)), 2)
                         .where(kerentanan.lte(2), 1))
    peta.add_layer(harkat_kerentanan, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat kerentanan', tampil=False)

    risiko = harkat_kerawanan.add(harkat_eksposur)   # .add(harkat_kerentanan)
    peta.add_layer(risiko, {'min': 1, 'max': 10, 'palette': HIJAU_MERAH}, 'Risiko banjir', tampil=False)

    harkat_risiko = (risiko.where(risiko.gt(8), 5)
                     .where(risiko.gt(6).And(risiko.lte(8)), 4)
                     .where(risiko.gt(4).And(risiko.lte(6)), 3)
                     .where(risiko.gt(2).And(risiko.lte(4)), 2)
                     .where(risiko.lte(2), 1))
    peta.add_layer(harkat_risiko, {'min': 1, 'max': 5, 'palette': HIJAU_MERAH}, 'Harkat risiko')

    v.update({k: val for k, val in locals().items() if k not in ('v', 'peta')})
    return v


if __name__ == '__main__':
    init()
    peta = Peta('Task V')
    jalankan(peta)
    peta.save('task5.html')
