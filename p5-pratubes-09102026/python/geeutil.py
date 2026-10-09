"""Pengganti fitur Code Editor untuk versi Python.

- ``init()`` menggantikan login otomatis Code Editor.
- ``Peta`` menggantikan ``Map``: layer ditampilkan di peta folium lalu disimpan sebagai HTML.
- ``simpan_json`` menyimpan hasil ``getInfo()`` supaya angka bisa dicek ulang.
"""

import json
import os
from pathlib import Path

import ee
import folium

PROJECT = os.environ.get('EE_PROJECT', 'gen-lang-client-0431253184')
OUTPUT = Path(__file__).resolve().parent / 'output'


def init():
    """Inisialisasi Earth Engine. Jalankan `earthengine authenticate` sekali sebelumnya."""
    ee.Initialize(project=PROJECT)
    OUTPUT.mkdir(exist_ok=True)


def _vis_ke_parameter(vis):
    """Ubah visParam gaya JavaScript (list atau string) ke bentuk yang diterima getMapId."""
    hasil = {}
    for kunci, nilai in (vis or {}).items():
        if isinstance(nilai, (list, tuple)):
            hasil[kunci] = ','.join(str(v) for v in nilai)
        else:
            hasil[kunci] = nilai
    return hasil


class Peta:
    """Padanan sederhana objek ``Map`` di Code Editor."""

    def __init__(self, judul='Peta'):
        self.judul = judul
        self.peta = folium.Map(location=[-6.2, 106.8], zoom_start=9, control_scale=True, tiles=None)
        folium.TileLayer('OpenStreetMap', name='Map').add_to(self.peta)

    def center_object(self, objek, zoom=10):
        if isinstance(objek, (ee.Feature, ee.FeatureCollection)):
            objek = objek.geometry()
        lon, lat = objek.centroid(1).coordinates().getInfo()
        self.peta.location = [lat, lon]
        self.peta.options['zoom'] = zoom

    def add_layer(self, objek, vis=None, nama='Layer', tampil=True, opacity=1.0):
        vis = dict(vis or {})
        if isinstance(objek, (ee.Geometry, ee.Feature, ee.FeatureCollection)):
            fc = objek if isinstance(objek, ee.FeatureCollection) else ee.FeatureCollection([ee.Feature(objek)])
            warna = vis.get('color', '000000')
            gambar = fc.style(color=warna, pointSize=4, fillColor='00000000', width=2)
            map_id = gambar.getMapId({})
        else:
            map_id = ee.Image(objek).getMapId(_vis_ke_parameter(vis))
        folium.raster_layers.TileLayer(
            tiles=map_id['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name=nama,
            overlay=True,
            control=True,
            show=tampil,
            opacity=opacity,
        ).add_to(self.peta)

    def add_legend(self, judul, label, warna):
        """Legenda kiri-bawah, padanan ui.Panel legenda di Code Editor."""
        baris = ''.join(
            f'<div><span style="display:inline-block;width:16px;height:16px;'
            f'background:{w if w.startswith("#") or not _hex(w) else "#" + w};'
            f'border:1px solid #333;margin-right:6px;vertical-align:middle"></span>{l}</div>'
            for l, w in zip(label, warna)
        )
        html = (
            '<div style="position:fixed;bottom:24px;left:12px;z-index:9999;background:white;'
            'padding:8px 10px;border:1px solid #999;font:13px sans-serif">'
            f'<b>{judul}</b>{baris}</div>'
        )
        self.peta.get_root().html.add_child(folium.Element(html))

    def save(self, nama_file):
        folium.LayerControl(collapsed=False).add_to(self.peta)
        path = OUTPUT / nama_file
        self.peta.save(str(path))
        print('Peta disimpan:', path)
        return path


def _hex(teks):
    return len(teks) in (3, 6) and all(c in '0123456789abcdefABCDEF' for c in teks)


def simpan_json(nama_file, data):
    path = OUTPUT / nama_file
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Data disimpan:', path)
    return path
