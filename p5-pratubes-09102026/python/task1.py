"""Task I: filter citra, metadata, dan clustering k-means (padanan js/task1.js)."""

import ee

from geeutil import Peta, init


def jalankan(peta):
    # 1. Panggil data Landsat 9
    dataset = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')

    # 2. Geometry untuk filter berdasarkan lokasi
    geometry = ee.Geometry.Point([112.05730244401117, -6.897418238470722])

    # 3. Filter lokasi + filter metadata + urutkan tutupan awan
    #    (filterMetadata('CLOUD_COVER_LAND', 'less_than', 50) ditulis dengan ee.Filter.lt)
    dataset = (dataset
               .filterBounds(geometry)
               .filter(ee.Filter.lt('CLOUD_COVER_LAND', 50))
               .sort('CLOUD_COVER_LAND'))

    # 4. Intip metadata apa saja yang tersimpan pada citra
    print('Daftar metadata:', dataset.first().propertyNames().getInfo())

    # 5. Metadata spesifik: tutupan awan di daratan
    print('CLOUD_COVER_LAND:', dataset.first().get('CLOUD_COVER_LAND').getInfo())

    # 6. Ambil satu citra (awan paling tipis karena sudah di-sort)
    img = dataset.first()

    # 7. Visual parameter true color (merah-hijau-biru)
    image_vis_param = {'bands': ['SR_B4', 'SR_B3', 'SR_B2'], 'min': 7061, 'max': 14103, 'gamma': 1}
    peta.add_layer(img, image_vis_param, 'Data paling bersih')

    # 8. Poligon batas wilayah kajian clustering
    geometry2 = ee.Geometry.Polygon(
        [[[111.56510661311408, -7.125131151145682],
          [111.56510661311408, -7.178102498857165],
          [111.62192652888557, -7.178102498857165],
          [111.62192652888557, -7.125131151145682]]], None, False)

    # 9. Pilih band reflektansi dan potong ke wilayah kajian
    band = ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7']
    img_pilih = img.select(band).clip(geometry2)

    # 10. Ambil 500 piksel contoh sebagai bahan latih clusterer
    data_training = img_pilih.sample(region=geometry2, scale=30, numPixels=500)

    # 11. Latih model k-means 15 kelompok, lalu terapkan ke seluruh citra
    cluster_model = ee.Clusterer.wekaKMeans(15).train(data_training)
    hasil = img_pilih.cluster(cluster_model)

    # 12. Pilih kelompok yang tampak sebagai bangunan, sembunyikan yang lain
    # Modul memakai cluster 2 dan 3. Pada run ini cluster 2 justru bervegetasi (NDBI -0.16, NDVI 0.36),
    # sedangkan cluster 9 dan 11 punya NDBI positif, NDVI rendah, dan mengumpul di pusat kota Cepu.
    lahan_terbangun = hasil.eq(9).Or(hasil.eq(11)).selfMask()

    # 13. Tampilkan hasilnya
    peta.add_layer(lahan_terbangun, {'bands': ['cluster'], 'min': 1, 'palette': ['ff7070']}, 'Bangunan')

    # Tambahan (bukan dari modul): cluster mentah untuk memilih nomor cluster bangunan
    peta.add_layer(hasil.randomVisualizer(), {}, 'Cluster mentah', tampil=False)

    # Tambahan (bukan dari modul): arahkan peta ke poligon kajian untuk Gambar 1
    peta.center_object(geometry2, 14)
    return locals()


if __name__ == '__main__':
    init()
    peta = Peta('Task I')
    jalankan(peta)
    peta.save('task1.html')
