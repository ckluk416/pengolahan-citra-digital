# Praktikum Intermediate GEE (Versi Python)

Konversi skrip Earth Engine Code Editor (folder `../js`) ke Python memakai `earthengine-api`. Setiap berkas `.py` padanan satu berkas `.js` dengan nama yang sama.

| Python | JavaScript | Isi |
| --- | --- | --- |
| `task0_uji_koneksi.py` | `task0-uji-koneksi.js` | uji koneksi dan aset GDP/HDI |
| `task1.py` | `task1.js` | filter citra dan clustering k-means (Cepu) |
| `task2.py` | `task2.js` | cloud masking, komposit median, NDBI/NDWI (Jabodetabekpunjur) |
| `task3.py` | `task3.js` | urban sprawl 1990–2020, legenda, grafik luas |
| `task4.py` | `task4.js` | kerawanan banjir Batanghari |
| `task5.py` | `task5.js` | eksposur, kerentanan, risiko banjir |
| `tugas1.py` … `tugas4.py` | `tugas1.js` … `tugas4.js` | Tugas Praktikum Mandiri 1–4 |
| `hotsAB.py`, `hotsCD.py`, `hotsE.py` | `hotsAB.js`, `hotsCD.js`, `hotsE.js` | Soal HOTS A–E |

## Persiapan

Dependensi dikelola `uv` di proyek induk (`earthengine-api`, `folium`, `matplotlib`).

```bash
uv sync
uv run earthengine authenticate
```

Proyek Google Cloud bawaan adalah `gen-lang-client-0431253184`. Ganti lewat variabel lingkungan `EE_PROJECT` bila memakai proyek lain.

## Menjalankan

Jalankan dari folder `python`:

```bash
uv run python task1.py
```

Hasil tersimpan di `output/`:

- `*.html`: peta interaktif (pengganti panel peta Code Editor), buka di browser, layer bisa dinyalakan atau dimatikan dari kontrol di kanan atas.
- `*.png`: grafik (pengganti `ui.Chart`).
- `*.json`: angka hasil `getInfo()` untuk tabel laporan.

## Padanan fitur Code Editor

| Code Editor | Python |
| --- | --- |
| `Map.addLayer(obj, vis, nama, shown)` | `peta.add_layer(obj, vis, nama, tampil)` (`geeutil.Peta`, peta folium) |
| `Map.centerObject(obj, zoom)` | `peta.center_object(obj, zoom)` |
| legenda `ui.Panel` | `peta.add_legend(judul, label, warna)` |
| `ui.Chart.image.series` | `reduceRegion` per tahun lalu grafik matplotlib |
| `print(obj)`, `obj.evaluate(fn)` | `print(obj.getInfo())` |
| `function(x) { ... }` di `.map()` | fungsi Python atau `lambda` |
| `.and()`, `.or()`, `.not()` | `.And()`, `.Or()`, `.Not()` |
| `filterMetadata(p, 'less_than', v)` | `filter(ee.Filter.lt(p, v))` |
| properti `*_class_palette` pada citra | `remap` ke indeks kelas lalu `palette` di parameter visual |

Skrip lanjutan memanggil skrip sebelumnya seperti di versi JavaScript: `task5.py` memakai `task4.jalankan()`, `tugas4.py` memakai `task5`, `tugas2.py` memakai `task2`, `hotsCD.py` memakai `task4`, dan `tugas3.py` memakai fungsi `sprawl()` dari `task3.py`.
