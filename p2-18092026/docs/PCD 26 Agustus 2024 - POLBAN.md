---
title: "PCD 26 Agustus 2024 - POLBAN"
source: "https://mrizqi.notion.site/PCD-26-Agustus-2024-POLBAN-ddb7ef6670714a069ab533366eb57658"
exported: "2026-09-18T00:33:34.132Z"
generator: "NotionBackups.com"
---

# PCD 26 Agustus 2024 - POLBAN

DOSEN Praktikum : Rizqi (MR) & Trisna (TG)

## **Pendahuluan**

Dalam tutorial ini, kita akan membangun aplikasi web menggunakan FastAPI yang dapat melakukan berbagai operasi pengolahan citra. Aplikasi ini akan menggunakan OpenCV untuk memproses citra dan Bootstrap untuk membuat tampilan yang responsif. Fitur yang akan kita implementasikan meliputi:

1. Operasi dasar citra (tambah, kurang, max, min, inverse).
1. Operasi logika (NOT, AND, XOR).
1. Konversi citra ke grayscale.
1. Manipulasi histogram citra (histogram grayscale, histogram berwarna, histogram equalization, histogram specification).
1. Menghitung rata-rata intensitas piksel dan standar deviasi citra.

### **Langkah 1: Persiapan Proyek**

1. **Buat direktori proyek baru dan navigasikan ke dalamnya:**

  ```
  mkdir fastapi-opencv-26agustus
  cd fastapi-opencv-26agustus
  ```

1. **Buat struktur direktori berikut:**

  ```
  mkdir "static/uploads"
  mkdir "static/histograms"
  mkdir templates
  ```

1. **Buat virtual environment (opsional tapi disarankan):**

  ```
  python -m venv venv
  ```

1. **Aktifkan virtual environment:**
  - **Di Windows:**

    ```
    venv\\Scripts\\activate
    ```

  - **Di Linux/Mac:**

    ```
    source venv/bin/activate
    ```

1. **Instal FastAPI, Uvicorn, Jinja2, OpenCV, dan Matplotlib:**

  ```
  pip install fastapi uvicorn jinja2 opencv-python-headless python-multipart matplotlib scikit-image
  ```

### **Langkah 2: Membuat Struktur Proyek**

Struktur proyek akan terlihat seperti ini:

```
fastapi-opencv-profile/
├── main.py
├── static/
│   ├── uploads/
│   └── histograms/
└── templates/
    ├── base.html
    ├── equalize.html
    ├── grayscale.html
    ├── histogram.html
    ├── home.html
    ├── result.html
    ├── specify.html
    └── statistics.html
```

### **Langkah 3: Membuat Template HTML**

**1.** `base.html`**: Template Dasar**

Template ini akan menjadi dasar bagi semua halaman. Ini mencakup navigasi sidebar yang memudahkan akses ke semua fitur.

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}JTK PCD 2024 - NAMA - NIM{% endblock %}</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
  </head>
  <body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">JTK PCD 2024 - NAMA - NIM</a>
      </div>
    </nav>
    <div class="container-fluid">
      <div class="row">
        <!-- Sidebar -->
        <nav class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
          <div class="position-sticky">
            <ul class="nav flex-column">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="/">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/grayscale/">Grayscale</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/histogram/">Histogram</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/equalize/">Histogram Equalization</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/specify/">Histogram Specification</a>
              </li>
            </ul>
          </div>
        </nav>

        <!-- Main Content -->
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
          {% block content %}{% endblock %}
        </main>
      </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
```

**2.** `home.html`**: Halaman Utama**

Template ini berisi form untuk mengunggah gambar dan memilih operasi yang akan dilakukan.

```
{% extends "base.html" %} {% block title %}Home{% endblock %} {% block content
%}
<div class="container mt-5">
  <h2 class="text-center">Unggah Citra Digital untuk Operasi yang Tersedia</h2>
  <form
    action="/upload/"
    enctype="multipart/form-data"
    method="post"
    class="mt-4"
  >
    <div class="mb-3">
      <input
        name="file"
        type="file"
        accept="image/*"
        class="form-control"
        required
      />
    </div>
    <div class="text-center">
      <input type="submit" value="Upload" class="btn btn-primary" />
    </div>
  </form>

  <h2 class="text-center mt-5">Operasi Aritmatika pada Citra</h2>
  <form
    action="/operation/"
    enctype="multipart/form-data"
    method="post"
    class="mt-4"
  >
    <div class="mb-3">
      <label for="file">Pilih Gambar:</label>
      <input
        name="file"
        type="file"
        accept="image/*"
        class="form-control"
        required
      />
    </div>
    <div class="mb-3">
      <label for="operation">Pilih Operasi:</label>
      <select name="operation" class="form-select" required>
        <option value="add">Tambah</option>
        <option value="subtract">Kurang</option>
        <option value="max">Max</option>
        <option value="min">Min</option>
        <option value="inverse">Inverse</option>
      </select>
    </div>
    <div class="mb-3">
      <label for="value">Nilai Operasi (Range):</label>
      <input
        type="range"
        class="form-range"
        min="0"
        max="100"
        step="1"
        name="value"
        id="value"
        value="50"
      />
      <output id="valueOutput" class="form-text">50</output>
    </div>
    <div class="text-center">
      <input type="submit" value="Lakukan Operasi" class="btn btn-primary" />
    </div>
  </form>

  <h2 class="text-center mt-5">Operasi Logika pada Citra</h2>
  <form
    action="/logic_operation/"
    enctype="multipart/form-data"
    method="post"
    class="mt-4"
  >
    <div class="mb-3">
      <label for="file1">Pilih Gambar 1:</label>
      <input
        name="file1"
        type="file"
        accept="image/*"
        class="form-control"
        required
      />
    </div>
    <div class="mb-3">
      <label for="file2">Pilih Gambar 2 (Untuk operasi AND dan XOR):</label>
      <input name="file2" type="file" accept="image/*" class="form-control" />
    </div>
    <div class="mb-3">
      <label for="operation">Pilih Operasi:</label>
      <select name="operation" class="form-select" required>
        <option value="not">NOT</option>
        <option value="and">AND</option>
        <option value="xor">XOR</option>
      </select>
    </div>
    <div class="text-center">
      <input
        type="submit"
        value="Lakukan Operasi Logika"
        class="btn btn-primary"
      />
    </div>
  </form>

  <h2 class="text-center mt-5">Statistik Citra</h2>
  <form
    action="/statistics/"
    enctype="multipart/form-data"
    method="post"
    class="mt-4"
  >
    <div class="mb-3">
      <label for="file">Pilih Gambar:</label>
      <input
        name="file"
        type="file"
        accept="image/*"
        class="form-control"
        required
      />
    </div>
    <div class="text-center">
      <input type="submit" value="Hitung Statistik" class="btn btn-primary" />
    </div>
  </form>

  <script>
    const slider = document.getElementById("value");
    const output = document.getElementById("valueOutput");
    slider.addEventListener("input", function () {
      output.textContent = slider.value;
    });
  </script>
</div>
{% endblock %}
```

**3.** `result.html`**: Menampilkan Gambar Asli dan Hasil**

Template ini digunakan untuk menampilkan gambar asli dan hasil setelah operasi dilakukan.

```
{% extends "base.html" %} {% block title %}Hasil Operasi Citra{% endblock %} {%
block content %}
<div class="container mt-5">
  <h2 class="text-center">Perbandingan Citra Asli dan Hasil Operasi</h2>
  <div class="row">
    <div class="col-md-6">
      <h4 class="text-center">Gambar Asli</h4>
      <div class="text-center">
        <img
          src="{{ original_image_path }}"
          alt="Original Image"
          class="img-fluid rounded shadow-lg mb-4"
        />
      </div>
    </div>
    <div class="col-md-6">
      <h4 class="text-center">Gambar Hasil</h4>
      <div class="text-center">
        <img
          src="{{ modified_image_path }}"
          alt="Modified Image"
          class="img-fluid rounded shadow-lg mb-4"
        />
      </div>
    </div>
  </div>
  <div class="text-center mt-4">
    <a href="/" class="btn btn-secondary">Kembali ke Home</a>
  </div>
</div>
{% endblock %}
```

**4.** `histogram.html`**: Menampilkan Histogram**

Template ini digunakan untuk menampilkan histogram grayscale dan berwarna dari citra yang diunggah.

```
{% extends "base.html" %} {% block title %}Generate Image Histogram{% endblock
%} {% block content %}
<div class="container mt-5">
  <h2 class="text-center">Generate Histogram Citra</h2>
  <form
    action="/histogram/"
    enctype="multipart/form-data"
    method="post"
    class="mt-4"
  >
    <div class="mb-3">
      <input
        name="file"
        type="file"
        accept="image/*"
        class="form-control"
        required
      />
    </div>
    <div class="text-center">
      <input type="submit" value="Generate Histogram" class="btn btn-primary" />
    </div>
  </form>

  {% if grayscale_histogram_path and color_histogram_path %}
  <div class="row mt-5">
    <div class="col-md-6">
      <h4 class="text-center">Histogram Grayscale</h4>
      <img
        src="{{ grayscale_histogram_path }}"
        alt="Grayscale Histogram"
        class="img-fluid rounded shadow-lg mb-4"
      />
    </div>
    <div class="col-md-6">
      <h4 class="text-center">Histogram Berwarna</h4>
      <img
        src="{{ color_histogram_path }}"
        alt="Color Histogram"
        class="img-fluid rounded shadow-lg mb-4"
      />
    </div>
  </div>
  {% endif %}
</div>
{% endblock %}
```

**5.** `statistics.html`**: Menampilkan Rata-rata Intensitas dan Standar Deviasi**

Template ini digunakan untuk menampilkan hasil perhitungan rata-rata intensitas piksel dan standar deviasi.

```
{% extends "base.html" %} {% block title %}Statistik Citra{% endblock %} {%
block content %}
<div class="container mt-5">
  <h2 class="text-center">Statistik Citra</h2>
  <div class="text-center">
    <img
      src="{{ image_path }}"
      alt="Image for Statistics"
      class="img-fluid rounded shadow-lg mb-4"
    />
  </div>
  <h4 class="text-center">Rata-rata Intensitas Piksel: {{ mean_intensity }}</h4>
  <h4 class="text-center">Standar Deviasi (Kontras): {{ std_deviation }}</h4>
  <div class="text-center mt-4">
    <a href="/" class="btn btn-secondary">Kembali ke Home</a>
  </div>
</div>
{% endblock %}
```

**6.** `equalize.html`**: Halaman Histogram Equalization**

Buat file bernama `equalize.html` di dalam folder `templates` dengan isi seperti berikut:

```
{% extends "base.html" %} {% block title %}Histogram Equalization{% endblock %}
{% block content %}
<div class="container mt-5">
  <h2 class="text-center">Equalisasi Histogram Citra</h2>
  <form
    action="/equalize/"
    enctype="multipart/form-data"
    method="post"
    class="mt-4"
  >
    <div class="mb-3">
      <input
        name="file"
        type="file"
        accept="image/*"
        class="form-control"
        required
      />
    </div>
    <div class="text-center">
      <input
        type="submit"
        value="Equalisasi Histogram"
        class="btn btn-primary"
      />
    </div>
  </form>
</div>
{% endblock %}
```

**7.** `grayscale.html`**: Halaman Grayscale**

Buat file bernama `grayscale.html` di dalam folder `templates` dengan isi seperti berikut:

```
{% extends "base.html" %} {% block title %}Grayscale Image Conversion{% endblock
%} {% block content %}
<div class="container mt-5">
  <h2 class="text-center">Konversi Citra ke Grayscale</h2>
  <form
    action="/grayscale/"
    enctype="multipart/form-data"
    method="post"
    class="mt-4"
  >
    <div class="mb-3">
      <input
        name="file"
        type="file"
        accept="image/*"
        class="form-control"
        required
      />
    </div>
    <div class="text-center">
      <input
        type="submit"
        value="Konversi ke Grayscale"
        class="btn btn-primary"
      />
    </div>
  </form>
</div>
{% endblock %}
```

**8.** `specify.html`**: Halaman Histogram Specification**

Buat file bernama `specify.html` di dalam folder `templates` dengan isi seperti berikut:

```
{% extends "base.html" %} {% block title %}Histogram Specification{% endblock %}
{% block content %}
<div class="container mt-5">
  <h2 class="text-center">Spesifikasi Histogram Citra</h2>
  <form
    action="/specify/"
    enctype="multipart/form-data"
    method="post"
    class="mt-4"
  >
    <div class="mb-3">
      <label for="file">Pilih Gambar yang Akan Diubah:</label>
      <input
        name="file"
        type="file"
        accept="image/*"
        class="form-control"
        required
      />
    </div>
    <div class="mb-3">
      <label for="ref_file">Pilih Gambar Referensi:</label>
      <input
        name="ref_file"
        type="file"
        accept="image/*"
        class="form-control"
        required
      />
    </div>
    <div class="text-center">
      <input
        type="submit"
        value="Spesifikasi Histogram"
        class="btn btn-primary"
      />
    </div>
  </form>
</div>
{% endblock %}
```

### **Langkah 4: Membuat Backend di** `main.py`

`main.py`**:**

```
import os
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from skimage.exposure import match_histograms  # pastikan paket scikit-image sudah terinstal

import numpy as np
import cv2
import matplotlib.pyplot as plt

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads")

if not os.path.exists("static/histograms"):
    os.makedirs("static/histograms")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    file_path = save_image(img, "uploaded")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": file_path,
        "modified_image_path": file_path
    })

@app.post("/operation/", response_class=HTMLResponse)
async def perform_operation(
    request: Request,
    file: UploadFile = File(...),
    operation: str = Form(...),
    value: int = Form(...)
):
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    original_path = save_image(img, "original")

    if operation == "add":
        result_img = cv2.add(img, np.full(img.shape, value, dtype=np.uint8))
    elif operation == "subtract":
        result_img = cv2.subtract(img, np.full(img.shape, value, dtype=np.uint8))
    elif operation == "max":
        result_img = np.maximum(img, np.full(img.shape, value, dtype=np.uint8))
    elif operation == "min":
        result_img = np.minimum(img, np.full(img.shape, value, dtype=np.uint8))
    elif operation == "inverse":
        result_img = cv2.bitwise_not(img)

    modified_path = save_image(result_img, "modified")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path
    })

@app.post("/logic_operation/", response_class=HTMLResponse)
async def perform_logic_operation(
    request: Request,
    file1: UploadFile = File(...),
    file2: UploadFile = File(None),
    operation: str = Form(...)
):
    image_data1 = await file1.read()
    np_array1 = np.frombuffer(image_data1, np.uint8)
    img1 = cv2.imdecode(np_array1, cv2.IMREAD_COLOR)

    original_path = save_image(img1, "original")

    if operation == "not":
        result_img = cv2.bitwise_not(img1)
    else:
        if file2 is None:
            return HTMLResponse("Operasi AND dan XOR memerlukan dua gambar.", status_code=400)
        image_data2 = await file2.read()
        np_array2 = np.frombuffer(image_data2, np.uint8)
        img2 = cv2.imdecode(np_array2, cv2.IMREAD_COLOR)

        if operation == "and":
            result_img = cv2.bitwise_and(img1, img2)
        elif operation == "xor":
            result_img = cv2.bitwise_xor(img1, img2)

    modified_path = save_image(result_img, "modified")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path
    })
@app.get("/grayscale/", response_class=HTMLResponse)
async def grayscale_form(request: Request):
    # Menampilkan form untuk upload gambar ke grayscale
    return templates.TemplateResponse("grayscale.html", {"request": request})

@app.post("/grayscale/", response_class=HTMLResponse)
async def convert_grayscale(request: Request, file: UploadFile = File(...)):
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    original_path = save_image(img, "original")
    modified_path = save_image(gray_img, "grayscale")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path
    })

@app.get("/histogram/", response_class=HTMLResponse)
async def histogram_form(request: Request):
    # Menampilkan halaman untuk upload gambar untuk histogram
    return templates.TemplateResponse("histogram.html", {"request": request})

@app.post("/histogram/", response_class=HTMLResponse)
async def generate_histogram(request: Request, file: UploadFile = File(...)):
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Pastikan gambar berhasil diimpor
    if img is None:
        return HTMLResponse("Tidak dapat membaca gambar yang diunggah", status_code=400)

    # Buat histogram grayscale dan berwarna
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayscale_histogram_path = save_histogram(gray_img, "grayscale")

    color_histogram_path = save_color_histogram(img)

    return templates.TemplateResponse("histogram.html", {
        "request": request,
        "grayscale_histogram_path": grayscale_histogram_path,
        "color_histogram_path": color_histogram_path
    })

@app.get("/equalize/", response_class=HTMLResponse)
async def equalize_form(request: Request):
    # Menampilkan halaman untuk upload gambar untuk equalisasi histogram
    return templates.TemplateResponse("equalize.html", {"request": request})

@app.post("/equalize/", response_class=HTMLResponse)
async def equalize_histogram(request: Request, file: UploadFile = File(...)):
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)

    equalized_img = cv2.equalizeHist(img)

    original_path = save_image(img, "original")
    modified_path = save_image(equalized_img, "equalized")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path
    })

@app.get("/specify/", response_class=HTMLResponse)
async def specify_form(request: Request):
    # Menampilkan halaman untuk upload gambar dan referensi untuk spesifikasi histogram
    return templates.TemplateResponse("specify.html", {"request": request})

@app.post("/specify/", response_class=HTMLResponse)
async def specify_histogram(request: Request, file: UploadFile = File(...), ref_file: UploadFile = File(...)):
    # Baca gambar yang diunggah dan gambar referensi
    image_data = await file.read()
    ref_image_data = await ref_file.read()

    np_array = np.frombuffer(image_data, np.uint8)
    ref_np_array = np.frombuffer(ref_image_data, np.uint8)
		
		#jika ingin grayscale
    #img = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
    #ref_img = cv2.imdecode(ref_np_array, cv2.IMREAD_GRAYSCALE)

    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # Membaca gambar dalam format BGR
    ref_img = cv2.imdecode(ref_np_array, cv2.IMREAD_COLOR)  # Membaca gambar referensi dalam format BGR

    if img is None or ref_img is None:
        return HTMLResponse("Gambar utama atau gambar referensi tidak dapat dibaca.", status_code=400)

    # Spesifikasi histogram menggunakan match_histograms dari skimage #grayscale
    #specified_img = match_histograms(img, ref_img, multichannel=False)
		    # Spesifikasi histogram menggunakan match_histograms dari skimage untuk gambar berwarna
    specified_img = match_histograms(img, ref_img, channel_axis=-1)
    # Konversi kembali ke format uint8 jika diperlukan
    specified_img = np.clip(specified_img, 0, 255).astype('uint8')

    original_path = save_image(img, "original")
    modified_path = save_image(specified_img, "specified")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path
    })

@app.post("/statistics/", response_class=HTMLResponse)
async def calculate_statistics(request: Request, file: UploadFile = File(...)):
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)

    mean_intensity = np.mean(img)
    std_deviation = np.std(img)

    image_path = save_image(img, "statistics")

    return templates.TemplateResponse("statistics.html", {
        "request": request,
        "mean_intensity": mean_intensity,
        "std_deviation": std_deviation,
        "image_path": image_path
    })

def save_image(image, prefix):
    filename = f"{prefix}_{uuid4()}.png"
    path = os.path.join("static/uploads", filename)
    cv2.imwrite(path, image)
    return f"/static/uploads/{filename}"

def save_histogram(image, prefix):
    histogram_path = f"static/histograms/{prefix}_{uuid4()}.png"
    plt.figure()
    plt.hist(image.ravel(), 256, [0, 256])
    plt.savefig(histogram_path)
    plt.close()
    return f"/{histogram_path}"

def save_color_histogram(image):
    color_histogram_path = f"static/histograms/color_{uuid4()}.png"
    plt.figure()
    for i, color in enumerate(['b', 'g', 'r']):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
    plt.savefig(color_histogram_path)
    plt.close()
    return f"/{color_histogram_path}"
```

### **Penjelasan Kode**

1. **Operasi Aritmatika dan Logika**:
  - Endpoint `/operation/` menangani berbagai operasi aritmatika (tambah, kurang, max, min, inverse) sesuai dengan input dari pengguna.
  - Endpoint `/logic_operation/` menangani operasi logika (NOT, AND, XOR). Operasi NOT memerlukan satu gambar, sementara operasi AND dan XOR memerlukan dua gambar.
1. **Konversi Grayscale**:
  - Endpoint `/grayscale/` mengonversi gambar ke grayscale menggunakan `cv2.cvtColor()`.
1. **Manipulasi Histogram**:
  - Endpoint `/histogram/` membuat histogram grayscale dan berwarna.
  - Endpoint `/equalize/` melakukan histogram equalization pada citra grayscale.
  - Endpoint `/specify/` melakukan histogram specification untuk mencocokkan histogram dari dua citra berbeda.
1. **Statistik Citra**:
  - Endpoint `/statistics/` menghitung rata-rata intensitas piksel dan standar deviasi (kontras) dari gambar.
1. **Fungsi Penyimpanan**:
  - Fungsi `save_image()` digunakan untuk menyimpan gambar di direktori `static/uploads`.
  - Fungsi `save_histogram()` dan `save_color_histogram()` digunakan untuk menyimpan histogram di direktori `static/histograms`.

### **Langkah 5: Menjalankan Aplikasi**

Jalankan aplikasi menggunakan Uvicorn:

```
uvicorn main:app --reload
```

### **Langkah 6: Pahami Code**

### **Langkah 7: Tambahkan Code diatas ke folder Proyek PCD Anda**

### **Langkah 8: Ujicoba Operasi pada citra, cek apakah ada kesalahan , perbaiki jika ada.**

### **Langkah 9: Dokumentasi dan Laporkan.**

\*Untuk melihat dampak histogram equalization anda dapat menggunakan citra berikut :

[WikipediaHistogram equalization](https://en.wikipedia.org/wiki/Histogram_equalization#/media/File:Unequalized_Hawkes_Bay_NZ.jpg)

\*Untuk Code Histogram Spesification / Matching dapat melihat halaman berikut [Histogram matching with OpenCV, scikit-image, and Python - GeeksforGeeks](https://www.geeksforgeeks.org/histogram-matching-with-opencv-scikit-image-and-python/) atau [https://informatika.stei.itb.ac.id/~rinaldi.munir/Citra/2022-2023/Makalah/Makalah-IF4073-Citra-Sem1-2022 (9).pdf](https://informatika.stei.itb.ac.id/~rinaldi.munir/Citra/2022-2023/Makalah/Makalah-IF4073-Citra-Sem1-2022%20(9%29.pdf)

Untuk Citra Uji Histogram Spesification / Matching bisa menggunakan:

[https://en.wikipedia.org/wiki/File:STS120LaunchHiRes-edit1.jpg](https://en.wikipedia.org/wiki/File:STS120LaunchHiRes-edit1.jpg)

[https://commons.wikimedia.org/wiki/File:STS-116\_Launch\_(KSC-06PD-2750)\_cropped.jpg](https://commons.wikimedia.org/wiki/File:STS-116_Launch_%28KSC-06PD-2750%29_cropped.jpg)
