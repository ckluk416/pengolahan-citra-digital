"""Tugas Mandiri 3: urban sprawl Kota Bandung dan sekitarnya, 1990-2024 (padanan js/tugas3.js)."""

import ee

from geeutil import Peta, init
from task3 import sprawl


def jalankan(peta):
    # Kota Bandung dan sekitarnya (termasuk Cimahi); ROI dan yearList diganti dari Task III
    roi = ee.Geometry.Rectangle([107.50, -7.02, 107.75, -6.83], None, False)
    peta.center_object(roi, 11)
    year_list = [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]   # 2024 ditambahkan
    return sprawl(peta, roi, year_list, 'Urban area Bandung (Ha)', 'tugas3-grafik.png')


if __name__ == '__main__':
    init()
    peta = Peta('Tugas 3')
    jalankan(peta)
    peta.save('tugas3.html')
