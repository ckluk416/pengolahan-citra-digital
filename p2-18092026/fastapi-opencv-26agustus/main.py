import os
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from skimage.exposure import match_histograms  # pastikan paket scikit-image sudah terinstal

import numpy as np
import cv2
import filters  # operasi dari notebook Colab Pertemuan 4
import matplotlib
matplotlib.use("Agg")  # backend non-GUI: plt.figure() di thread request akan crash dengan backend Tk default
import matplotlib.pyplot as plt

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads")

if not os.path.exists("static/histograms"):
    os.makedirs("static/histograms")


async def read_upload(file: UploadFile, flags=cv2.IMREAD_COLOR):
    # Decode UploadFile ke numpy array; mengembalikan None jika file bukan citra yang valid
    image_data = await file.read()
    if not image_data:
        return None
    np_array = np.frombuffer(image_data, np.uint8)
    return cv2.imdecode(np_array, flags)


def bad_image_response():
    return HTMLResponse("Tidak dapat membaca gambar yang diunggah", status_code=400)


def render_result(request: Request, original_path: str, modified_path: str):
    return templates.TemplateResponse(request, "result.html", {
        "original_image_path": original_path,
        "modified_image_path": modified_path
    })


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "home.html")

@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    img = await read_upload(file)
    if img is None:
        return bad_image_response()

    file_path = save_image(img, "uploaded")

    return render_result(request, file_path, file_path)

@app.post("/operation/", response_class=HTMLResponse)
async def perform_operation(
    request: Request,
    file: UploadFile = File(...),
    operation: str = Form(...),
    value: int = Form(...)
):
    img = await read_upload(file)
    if img is None:
        return bad_image_response()

    original_path = save_image(img, "original")

    # np.full(..., dtype=uint8) akan overflow kalau value > 255, jadi dibatasi ke 0..255
    value = int(np.clip(value, 0, 255))
    scalar = np.full(img.shape, value, dtype=np.uint8)

    if operation == "add":
        result_img = cv2.add(img, scalar)
    elif operation == "subtract":
        result_img = cv2.subtract(img, scalar)
    elif operation == "max":
        result_img = np.maximum(img, scalar)
    elif operation == "min":
        result_img = np.minimum(img, scalar)
    elif operation == "inverse":
        result_img = cv2.bitwise_not(img)
    else:
        return HTMLResponse(f"Operasi tidak dikenal: {operation}", status_code=400)

    modified_path = save_image(result_img, "modified")

    return render_result(request, original_path, modified_path)

@app.post("/logic_operation/", response_class=HTMLResponse)
async def perform_logic_operation(
    request: Request,
    file1: UploadFile = File(...),
    file2: UploadFile | None = File(None),
    operation: str = Form(...)
):
    img1 = await read_upload(file1)
    if img1 is None:
        return bad_image_response()

    original_path = save_image(img1, "original")

    if operation == "not":
        result_img = cv2.bitwise_not(img1)
    else:
        # Browser tetap mengirim field file2 kosong jika user tidak memilih file,
        # jadi cek isi filenya, bukan hanya `file2 is None`
        img2 = await read_upload(file2) if file2 is not None else None
        if img2 is None:
            return HTMLResponse("Operasi AND dan XOR memerlukan dua gambar.", status_code=400)

        # bitwise_and/xor mewajibkan ukuran kedua citra sama
        if img2.shape != img1.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        if operation == "and":
            result_img = cv2.bitwise_and(img1, img2)
        elif operation == "xor":
            result_img = cv2.bitwise_xor(img1, img2)
        else:
            return HTMLResponse(f"Operasi tidak dikenal: {operation}", status_code=400)

    modified_path = save_image(result_img, "modified")

    return render_result(request, original_path, modified_path)

@app.get("/grayscale/", response_class=HTMLResponse)
async def grayscale_form(request: Request):
    # Menampilkan form untuk upload gambar ke grayscale
    return templates.TemplateResponse(request, "grayscale.html")

@app.post("/grayscale/", response_class=HTMLResponse)
async def convert_grayscale(request: Request, file: UploadFile = File(...)):
    img = await read_upload(file)
    if img is None:
        return bad_image_response()

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    original_path = save_image(img, "original")
    modified_path = save_image(gray_img, "grayscale")

    return render_result(request, original_path, modified_path)

@app.get("/histogram/", response_class=HTMLResponse)
async def histogram_form(request: Request):
    # Menampilkan halaman untuk upload gambar untuk histogram
    return templates.TemplateResponse(request, "histogram.html")

@app.post("/histogram/", response_class=HTMLResponse)
async def generate_histogram(request: Request, file: UploadFile = File(...)):
    img = await read_upload(file)

    # Pastikan gambar berhasil diimpor
    if img is None:
        return bad_image_response()

    # Buat histogram grayscale dan berwarna
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayscale_histogram_path = save_histogram(gray_img, "grayscale")

    color_histogram_path = save_color_histogram(img)

    return templates.TemplateResponse(request, "histogram.html", {
        "grayscale_histogram_path": grayscale_histogram_path,
        "color_histogram_path": color_histogram_path
    })

@app.get("/equalize/", response_class=HTMLResponse)
async def equalize_form(request: Request):
    # Menampilkan halaman untuk upload gambar untuk equalisasi histogram
    return templates.TemplateResponse(request, "equalize.html")

@app.post("/equalize/", response_class=HTMLResponse)
async def equalize_histogram(request: Request, file: UploadFile = File(...)):
    img = await read_upload(file, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return bad_image_response()

    equalized_img = cv2.equalizeHist(img)

    original_path = save_image(img, "original")
    modified_path = save_image(equalized_img, "equalized")

    return render_result(request, original_path, modified_path)

@app.get("/specify/", response_class=HTMLResponse)
async def specify_form(request: Request):
    # Menampilkan halaman untuk upload gambar dan referensi untuk spesifikasi histogram
    return templates.TemplateResponse(request, "specify.html")

@app.post("/specify/", response_class=HTMLResponse)
async def specify_histogram(request: Request, file: UploadFile = File(...), ref_file: UploadFile = File(...)):
    # Baca gambar yang diunggah dan gambar referensi dalam format BGR
    # (jika ingin grayscale, ganti flag ke cv2.IMREAD_GRAYSCALE dan hapus channel_axis di bawah)
    img = await read_upload(file, cv2.IMREAD_COLOR)
    ref_img = await read_upload(ref_file, cv2.IMREAD_COLOR)

    if img is None or ref_img is None:
        return HTMLResponse("Gambar utama atau gambar referensi tidak dapat dibaca.", status_code=400)

    # Spesifikasi histogram menggunakan match_histograms dari skimage untuk gambar berwarna
    # (ukuran citra tidak perlu sama, hanya jumlah channel yang harus sama)
    specified_img = match_histograms(img, ref_img, channel_axis=-1)
    # Konversi kembali ke format uint8
    specified_img = np.clip(specified_img, 0, 255).astype('uint8')

    original_path = save_image(img, "original")
    modified_path = save_image(specified_img, "specified")

    return render_result(request, original_path, modified_path)

@app.post("/statistics/", response_class=HTMLResponse)
async def calculate_statistics(request: Request, file: UploadFile = File(...)):
    img = await read_upload(file, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return bad_image_response()

    mean_intensity = float(np.mean(img))
    std_deviation = float(np.std(img))

    image_path = save_image(img, "statistics")

    return templates.TemplateResponse(request, "statistics.html", {
        "mean_intensity": round(mean_intensity, 2),
        "std_deviation": round(std_deviation, 2),
        "image_path": image_path
    })

@app.get("/filter/", response_class=HTMLResponse)
async def filter_form(request: Request):
    # Menampilkan form untuk filtering spasial & transformasi Fourier
    return templates.TemplateResponse(request, "filter.html")

@app.post("/filter/", response_class=HTMLResponse)
async def apply_filter_operation(
    request: Request,
    file: UploadFile = File(...),
    operation: str = Form(...),
    padding_size: int = Form(20),
    radius: int = Form(30)
):
    img = await read_upload(file)
    if img is None:
        return bad_image_response()

    original_path = save_image(img, "original")

    # Nilai operasi di form: "<kelompok>_<varian>", mis. conv_sharpen, filter_band
    if operation.startswith("conv_"):
        result_img = filters.apply_convolution(img, operation.removeprefix("conv_"))
    elif operation == "zero_padding":
        result_img = filters.apply_zero_padding(img, max(1, padding_size))
    elif operation.startswith("filter_"):
        result_img = filters.apply_filter(img, operation.removeprefix("filter_"))
    elif operation == "fourier":
        result_img = filters.apply_fourier_transform(img)
    elif operation == "periodic_noise":
        result_img = filters.reduce_periodic_noise(img, max(1, radius))
    else:
        return HTMLResponse(f"Operasi tidak dikenal: {operation}", status_code=400)

    modified_path = save_image(result_img, operation)

    return render_result(request, original_path, modified_path)

def save_image(image, prefix):
    filename = f"{prefix}_{uuid4()}.png"
    path = os.path.join("static/uploads", filename)
    cv2.imwrite(path, image)
    return f"/static/uploads/{filename}"

def save_histogram(image, prefix):
    histogram_path = f"static/histograms/{prefix}_{uuid4()}.png"
    plt.figure()
    plt.hist(image.ravel(), 256, [0, 256])
    plt.title("Histogram Grayscale")
    plt.xlabel("Intensitas")
    plt.ylabel("Jumlah Piksel")
    plt.savefig(histogram_path)
    plt.close()
    return f"/{histogram_path}"

def save_color_histogram(image):
    color_histogram_path = f"static/histograms/color_{uuid4()}.png"
    plt.figure()
    for i, color in enumerate(['b', 'g', 'r']):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
    plt.title("Histogram Berwarna (B, G, R)")
    plt.xlabel("Intensitas")
    plt.ylabel("Jumlah Piksel")
    plt.xlim([0, 256])
    plt.savefig(color_histogram_path)
    plt.close()
    return f"/{color_histogram_path}"
