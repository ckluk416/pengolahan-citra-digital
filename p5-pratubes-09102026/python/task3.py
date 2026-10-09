"""Task III: perulangan, koleksi 1990-2020, komposit minimum, legenda, dan grafik (padanan js/task3.js).

ui.Chart.image.series diganti grafik matplotlib yang disimpan sebagai PNG.
Band luas memakai perbaikan built.gt(0), sama seperti skrip task3 di Code Editor.
"""

import ee
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

from geeutil import OUTPUT, Peta, init  # noqa: E402

PALETTE = ['800080', '0000FF', '00FFFF', '008000', 'FFFF00', 'FFA500', 'FF0000', 'FF1493']


def filter_col(col, roi, date):
    return col.filterDate(date[0], date[1]).filterBounds(roi)


# Cloud mask Landsat 4/5/7 (TM): urutan band beda, tanpa cirrus
def cloud_mask_tm(image):
    qa = image.select('QA_PIXEL')
    mask = (qa.bitwiseAnd(1 << 1).eq(0)
            .And(qa.bitwiseAnd(1 << 3).eq(0))
            .And(qa.bitwiseAnd(1 << 4).eq(0)))
    return (image.select(['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'],
                         ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
            .updateMask(mask))


# Cloud mask Landsat 8/9 (OLI): sekelas Task II
def cloud_mask_oli(image):
    qa = image.select('QA_PIXEL')
    mask = (qa.bitwiseAnd(1 << 1).eq(0)
            .And(qa.bitwiseAnd(1 << 2).eq(0))
            .And(qa.bitwiseAnd(1 << 3).eq(0))
            .And(qa.bitwiseAnd(1 << 4).eq(0)))
    return (image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                         ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
            .updateMask(mask))


def sprawl(peta, roi, year_list, judul_grafik, nama_grafik):
    l4 = ee.ImageCollection('LANDSAT/LT04/C02/T1_L2')
    l5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
    l7 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
    l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    l9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')

    def landsat457(roi, date):
        col = filter_col(l4, roi, date).merge(filter_col(l5, roi, date)).merge(filter_col(l7, roi, date))
        return col.map(cloud_mask_tm).median().clip(roi)

    def landsat89(roi, date):
        col = filter_col(l8, roi, date).merge(filter_col(l9, roi, date))
        return col.map(cloud_mask_oli).median().clip(roi)

    def per_tahun(year):
        start = ee.Date.fromYMD(year, 1, 1)
        end = ee.Date.fromYMD(year, 12, 31)
        date = [start, end]

        landsat = landsat457 if year < 2014 else landsat89

        # Komposit + penskalaan reflektansi
        image = landsat(roi, date).multiply(0.0000275).add(-0.2)
        peta.add_layer(image, {'bands': ['B5', 'B6', 'B2'], 'min': [0.1, 0.05, 0], 'max': [0.4, 0.3, 0.15]},
                       f'Landsat_{year}', tampil=False)

        # Indeks spektral tahunan
        band_map_tahun = {
            'NIR': image.select('B5'), 'SWIR': image.select('B6'), 'RED': image.select('B4'),
            'GREEN': image.select('B3'), 'BLUE': image.select('B2'),
        }
        ndbi_tahun = image.expression('(SWIR - NIR) / (SWIR + NIR)', band_map_tahun).rename('NDBI')
        mndwi = image.expression('(GREEN - SWIR) / (GREEN + SWIR)', band_map_tahun).rename('MNDWI')

        # Lahan terbangun: NILAI PIKSEL = TAHUN deteksi
        built = ee.Image(0).where(ndbi_tahun.gt(-0.1).And(mndwi.lte(0)), year).selfMask().clip(roi)
        peta.add_layer(built, {'palette': 'red'}, f'Built-up_{year}', tampil=False)

        # Band luas (hektar) untuk grafik
        # Koreksi: modul menulis built.multiply(...), padahal nilai piksel built adalah TAHUN (1990 dst.),
        # jadi luasnya ikut terkali tahun. built.gt(0) mengubahnya menjadi 1 untuk piksel terbangun.
        area = built.gt(0).multiply(ee.Image.pixelArea().multiply(0.0001)).rename('area')

        return (built.toUint16().rename('built').addBands(area)
                .set({'year': year, 'system:time_start': start.millis()}))

    built_col = ee.ImageCollection([per_tahun(y) for y in year_list])

    # Peta ekspansi: min lintas tahun = tahun TERAWAL piksel menjadi terbangun.
    # Code Editor membaca properti built_class_palette otomatis; di Python warnanya dipasang lewat remap.
    palette = PALETTE[:len(year_list)]
    urban_expansion = built_col.select('built').min()
    urban_idx = urban_expansion.remap(year_list, list(range(len(year_list))))
    peta.add_layer(urban_idx, {'min': 0, 'max': len(year_list) - 1, 'palette': palette}, 'Urban_expansion')

    # Legenda kiri-bawah
    peta.add_legend('Urban expansion', [str(y) for y in year_list], palette)

    # Grafik luas lahan terbangun (Ha) per tahun (padanan ui.Chart.image.series)
    luas = ee.List([
        img.select('area').reduceRegion(reducer=ee.Reducer.sum(), geometry=roi, scale=30,
                                        maxPixels=1e10, tileScale=4).get('area')
        for img in [built_col.filter(ee.Filter.eq('year', y)).first() for y in year_list]
    ]).getInfo()
    for y, h in zip(year_list, luas):
        print(f'{y}: {h:,.0f} Ha')

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(year_list, luas, alpha=0.3)
    ax.plot(year_list, luas, marker='o')
    ax.set_title(judul_grafik)
    ax.set_xlabel('Year')
    ax.set_ylabel('Area (Ha)')
    ax.set_xticks(year_list)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT / nama_grafik, dpi=150)
    plt.close(fig)
    print('Grafik disimpan:', OUTPUT / nama_grafik)
    return {'built_col': built_col, 'luas': luas}


def jalankan(peta):
    # Prasyarat dari Task II (blok kode Task III memakai roi dan l8 tanpa mendefinisikannya)
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

    # Latihan iterasi: for di Python (sisi klien)
    for i in range(30):
        print(i)

    # map pada list: ubah setiap unsur tanpa menyalin-tempel
    names = ['Ahmad', 'Agung', 'Andi']
    names_new = [name + ' Keren' for name in names]
    print(names_new)   # ['Ahmad Keren', 'Agung Keren', 'Andi Keren']

    lists = [{'name': 'A', 'year': 2010}, {'name': 'B', 'year': 2011}]
    print([obj['name'] for obj in lists])   # ['A', 'B']

    year_list = [1990, 1995, 2000, 2005, 2010, 2015, 2020]
    peta.center_object(roi, 10)
    hasil = sprawl(peta, roi, year_list, 'Urban area (Ha)', 'task3-grafik.png')
    return {'roi': roi, **hasil}


if __name__ == '__main__':
    init()
    peta = Peta('Task III')
    jalankan(peta)
    peta.save('task3.html')
