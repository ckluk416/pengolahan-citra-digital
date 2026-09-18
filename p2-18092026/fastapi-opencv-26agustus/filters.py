"""
Operasi filtering dari notebook Colab PCD Pertemuan 4 (9 September 2024),
dipindahkan menjadi fungsi murni agar bisa dipanggil dari endpoint FastAPI.

Semua fungsi menerima citra BGR uint8 (hasil cv2.imdecode) dan mengembalikan
citra uint8 yang siap disimpan dengan cv2.imwrite.
"""
import cv2
import numpy as np


def to_uint8(image):
    # Normalisasi array float (mis. hasil FFT) ke rentang 0..255 agar bisa disimpan sebagai PNG
    image = np.nan_to_num(image, nan=0.0, posinf=0.0, neginf=0.0)
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def apply_convolution(image, kernel_type="average"):
    if kernel_type == "average":
        kernel = np.ones((3, 3), np.float32) / 9
    elif kernel_type == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    elif kernel_type == "edge":
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    else:
        raise ValueError(f"kernel_type tidak dikenal: {kernel_type}")

    return cv2.filter2D(image, -1, kernel)


def apply_zero_padding(image, padding_size=10):
    return cv2.copyMakeBorder(
        image, padding_size, padding_size, padding_size, padding_size,
        cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )


def apply_filter(image, filter_type="low"):
    if filter_type == "low":
        return cv2.GaussianBlur(image, (5, 5), 0)
    if filter_type == "high":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)
    if filter_type == "band":
        # Versi notebook: low + (image - low) pada uint8 -> overflow/wrap-around, hasilnya
        # bukan band-pass. Band-pass yang benar = selisih dua Gaussian (difference of Gaussians),
        # dihitung dalam float lalu dinormalisasi kembali ke uint8.
        img_f = image.astype(np.float32)
        low_small = cv2.GaussianBlur(img_f, (3, 3), 0)
        low_large = cv2.GaussianBlur(img_f, (9, 9), 0)
        return to_uint8(low_small - low_large)
    raise ValueError(f"filter_type tidak dikenal: {filter_type}")


def apply_fourier_transform(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    # +1 agar log(0) tidak menghasilkan -inf
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    return to_uint8(magnitude_spectrum)


def reduce_periodic_noise(image, radius=30):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)

    # Mask persegi di tengah spektrum (sesuai notebook). Catatan: ini menghilangkan
    # frekuensi RENDAH, sehingga secara efektif berfungsi sebagai high-pass filter.
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols), np.uint8)
    mask[max(crow - radius, 0):crow + radius, max(ccol - radius, 0):ccol + radius] = 0

    fshift = fshift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    return to_uint8(np.abs(img_back))
