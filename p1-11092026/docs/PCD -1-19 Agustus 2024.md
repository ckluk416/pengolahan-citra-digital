---
title: "PCD -1-19 Agustus 2024"
source: "https://mrizqi.notion.site/PCD-1-19-Agustus-2024-fec11a35d27a43d98df370ec735034b0#a82b8dc4339b4f9cb2ee379bb3bdc0fc"
exported: "2026-09-11T01:28:35.788Z"
generator: "NotionBackups.com"
---

# PCD -1-19 Agustus 2024

Dalam praktikum ini, kita akan membangun aplikasi web sederhana menggunakan FastAPI. Aplikasi ini akan mengunggah citra digital dan menampilkan array RGB, . Kita akan menggunakan OpenCV untuk memproses citra dan Bootstrap untuk membuat tampilan yang responsif dan menarik.

### Langkah 1: Persiapan Proyek

1. **Buat direktori baru** untuk proyek Anda :

  ```
  mkdir fastapi-opencv-profile
  cd fastapi-opencv-profile
  ```

1. **Buat direktori** `static/uploads` untuk menyimpan citra:
1. **Buat direktori** `templates` untuk menyimpan file html:

  ```
  mkdir "static/uploads"
  mkdir templates
  ```

1. **Buat virtual environment** (opsional):

  ```
  python -m venv venv
  # Di Windows gunakan 
  venv\\Scripts\\activate
  #atau
  # selain windows
  source venv/bin/activate  
  ```

1. **Instal FastAPI, Uvicorn, Jinja2, dan OpenCV**:

  ```
  pip install fastapi uvicorn jinja2 opencv-python-headless python-multipart sqlalchemy databases sqlite-utils 
  ```

### Langkah 2: Membuat Struktur Proyek

**Buat struktur direktori berikut**:

  ```
  ├── main.py
  ├── static
  │   └── uploads
  └── templates
      ├── base.html
      ├── home.html
      └── display.html
  ```

### Langkah 3: Membuat Template HTML

Kita akan menggunakan Bootstrap untuk membuat tampilan yang responsif dan menarik. Mulai dengan template dasar (`base.html`) yang akan digunakan oleh halaman lainnya.

**1.** `base.html`**: Template Dasar**

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
    <div class="container mt-4">{% block content %}{% endblock %}</div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
```

**2.** `home.html`**: Halaman Upload Gambar**

```
{% extends "base.html" %} {% block title %}Home{% endblock %} {% block content
%}
<h2 class="text-center">Unggah Citra Digital untuk Mendapatkan Array RGB</h2>
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
{% endblock %}
```

**3.** `display.html`**: Halaman Profil Pengguna**

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Display Array RGB</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
  </head>
  <body class="bg-light">
    <div class="container mt-5">
      <h2 class="text-center">Gambar yang Diunggah</h2>
      <div class="text-center">
        <img
          src="{{ image_path }}"
          alt="Uploaded Image"
          class="img-fluid rounded shadow-lg mb-4"
        />
      </div>

      <h2 class="text-center">Array RGB</h2>
      <div class="row">
        <div class="col-md-4">
          <h3 class="text-center">Merah (R)</h3>
          <pre class="bg-white p-3 rounded shadow-sm">
{{ rgb_array['R'] | safe }}</pre
          >
        </div>
        <div class="col-md-4">
          <h3 class="text-center">Hijau (G)</h3>
          <pre class="bg-white p-3 rounded shadow-sm">
{{ rgb_array['G'] | safe }}</pre
          >
        </div>
        <div class="col-md-4">
          <h3 class="text-center">Biru (B)</h3>
          <pre class="bg-white p-3 rounded shadow-sm">
{{ rgb_array['B'] | safe }}</pre
          >
        </div>
      </div>

      <div class="text-center mt-4">
        <a href="/" class="btn btn-secondary">Unggah Gambar Lain</a>
      </div>
    </div>
  </body>
</html>
```

### Langkah 4: Membuat Backend di `main.py`

`main.py`**:**

```
import os
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np
import cv2

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    image_data = await file.read()
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join("static", "uploads", filename)

    with open(file_path, "wb") as f:
        f.write(image_data)

    np_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    b, g, r = cv2.split(img)

    rgb_array = {"R": r.tolist(), "G": g.tolist(), "B": b.tolist()}

    return templates.TemplateResponse("display.html", {
        "request": request,
        "image_path": f"/static/uploads/{filename}",
        "rgb_array": rgb_array
    })
```

### Langkah 5: Menjalankan Aplikasi

Jalankan aplikasi Anda menggunakan Uvicorn:

```
uvicorn main:app --reload
```

Buka halaman `http://127.0.0.1:8000/`

### Langkah 6: Ujicoba Citra Digital

Lakukan pengujian dengan file bacargb.zip

### Langkah 7: Pahami Code

Tuliskan hasil pemahaman anda

### Langkah 8: Modifikasi Code

Jika sudah paham modifikasi code, anda dapat membuat tampilan pixel seperti matriks,membuat chart, dll
