---
title: "PCD 16 SEPTEMBER 2024"
source: "https://mrizqi.notion.site/PCD-16-SEPTEMBER-2024-102fe88a4ea480d88009dbd333a7c56f"
exported: "2026-09-13T03:34:46.190Z"
generator: "NotionBackups.com"
---

# PCD 16 SEPTEMBER 2024

## **A. Pendahuluan**

Pada praktikum ini, Anda akan mengembangkan aplikasi berbasis Streamlit untuk mendeteksi dan menambahkan wajah baru ke dalam dataset. Selain itu, Anda akan melakukan pengolahan citra wajah dengan menambahkan derau (noise) jenis salt and pepper, menghilangkan noise tersebut, dan melakukan penajaman (sharpening) pada citra. Hasil akhir dari praktikum ini adalah dokumentasi proses beserta screenshot, serta kumpulan citra original dan hasil modifikasi.

## **B. Tujuan Praktikum**

1. Mengimplementasikan aplikasi deteksi wajah menggunakan Streamlit dan OpenCV.
1. Mengumpulkan dataset wajah baru melalui webcam.
1. Menerapkan teknik pengolahan citra: penambahan noise, penghilangan noise, dan penajaman citra.
1. Mengkonversi code streamlit ke API FastAPI anda.
1. Mendokumentasikan proses dan hasil pengolahan citra.

## **C. Alat dan Bahan**

1. **Perangkat Komputer** dengan Python terinstal.
1. **Webcam** terhubung ke komputer.
1. **Python Libraries**:
  - Streamlit
  - OpenCV
  - NumPy

## **D. Langkah-Langkah Praktikum**

### **1. Persiapan Lingkungan Kerja**

a. **Instalasi Python (Jika Belum Terinstal)**

- Pastikan Python versi 3.9 atau lebih baru sudah terinstal di komputer Anda.

b. **Membuat Virtual Environment (Opsional tetapi Disarankan)**

```
python -m venv praktikum_env
```

- **Aktifkan Virtual Environment:**
  - **Windows:**

    ```
    praktikum_env\\Scripts\\activate
    ```

  - **macOS/Linux:**

    ```
    source praktikum_env/bin/activate
    ```

c. **Instalasi Library yang Diperlukan**

- Buka terminal atau command prompt dan jalankan perintah berikut:

  ```
  pip install streamlit opencv-python-headless numpy
  ```

### **2. Menyiapkan Kode Aplikasi**

a. **Buat File Python**

- Buat file baru bernama `app.py` di direktori kerja Anda.
- Salin dan tempelkan kode berikut ke dalam `app.py`:

```
import streamlit as st
import cv2
import os
import numpy as np
import time

# Fungsi untuk mendeteksi wajah
def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(30, 30)
    )
    return faces

# Judul Aplikasi
st.title("Tambah Wajah Baru ke Dataset")

# Input nama orang baru
new_person = st.text_input("Masukkan nama orang baru:")

# Tombol untuk memulai proses penambahan wajah
capture = st.button("Tambahkan Wajah Baru")

if capture:
    if not new_person:
        st.warning("Silakan masukkan nama orang baru.")
    else:
        save_path = os.path.join('dataset', new_person)
        
        if not os.path.exists('dataset'):
            os.makedirs('dataset')
            st.info("Folder 'dataset' telah dibuat.")
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            st.success(f"Folder untuk {new_person} telah dibuat.")
            
            # Mulai menangkap gambar dari webcam
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Tidak dapat membuka webcam. Pastikan webcam terhubung dan tidak digunakan oleh aplikasi lain.")
            else:
                num_images = 0
                max_images = 20  # Ambil 20 gambar wajah

                frame_placeholder = st.empty()
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    while num_images < max_images:
                        ret, frame = cap.read()
                        if not ret:
                            st.error("Error: Tidak dapat membaca frame dari webcam.")
                            break

                        # Deteksi wajah dalam frame
                        faces = detect_faces(frame)

                        if len(faces) > 0:
                            for (x, y, w, h) in faces:
                                face = frame[y:y+h, x:x+w]
                                img_name = os.path.join(save_path, f"img_{num_images}.jpg")
                                cv2.imwrite(img_name, face)
                                num_images += 1

                                # Menggambar kotak di sekitar wajah yang terdeteksi
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                                # Tampilkan hasil deteksi
                                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                frame_placeholder.image(frame_rgb, channels="RGB", caption=f"Gambar {num_images}/{max_images}")

                                # Update progress bar
                                progress = num_images / max_images
                                progress_bar.progress(progress)
                                status_text.text(f"Menyimpan gambar {num_images} dari {max_images}...")

                                # Hentikan setelah menyimpan satu wajah per frame
                                break
                        else:
                            # Tampilkan frame tanpa deteksi
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            frame_placeholder.image(frame_rgb, channels="RGB", caption="Tidak ada wajah terdeteksi.")

                        time.sleep(0.1)  # Tambahkan delay untuk menghindari penggunaan CPU yang berlebihan

                    st.success(f"{num_images} gambar telah berhasil ditambahkan ke dataset {new_person}.")
                finally:
                    cap.release()
                    frame_placeholder.empty()
                    progress_bar.empty()
                    status_text.empty()
        else:
            st.warning("Nama sudah ada di dataset. Silakan pilih nama lain atau tambahkan lebih banyak gambar.")
```

### **3. Menjalankan Aplikasi Streamlit**

a. **Simpan File**

- Pastikan `app.py` telah disimpan setelah menempelkan kode di atas.

b. **Jalankan Aplikasi**

- Buka terminal atau command prompt di direktori tempat `app.py` berada.
- Jalankan perintah berikut:

  ```
  streamlit run app.py
  ```

- **Catatan:** Jika perintah `streamlit` tidak dikenali setelah instalasi, gunakan perintah alternatif berikut:

  ```
  python -m streamlit run app.py
  ```

c. **Interaksi dengan Aplikasi**

- Aplikasi akan terbuka di browser web Anda.
- Masukkan nama orang baru di kolom yang disediakan.
- Klik tombol "Tambahkan Wajah Baru" untuk memulai proses pengambilan gambar melalui webcam.
- Pastikan webcam terhubung dan tidak digunakan oleh aplikasi lain.
- Aplikasi akan secara otomatis mendeteksi wajah dan menyimpan 20 gambar wajah ke dalam folder dataset.

![](https://mrizqi.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F120c110a-2818-41a5-8c21-36c5c8d2a7c7%2Fbebefecb-699d-4000-884d-03b57a4155df%2Fimage.png?table=block&id=3526d297-68a6-4ad9-8ac1-77bd7fcac301&spaceId=120c110a-2818-41a5-8c21-36c5c8d2a7c7&width=1180&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

![](https://mrizqi.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F120c110a-2818-41a5-8c21-36c5c8d2a7c7%2Fb7e329b5-fd64-4675-a521-453e5562fd62%2Fimage.png?table=block&id=bf63b4ab-6a86-4108-9586-ae374d85cf4d&spaceId=120c110a-2818-41a5-8c21-36c5c8d2a7c7&width=1180&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

### **4. Pengolahan Citra Wajah**

Setelah berhasil mengumpulkan dataset wajah, langkah selanjutnya adalah melakukan pengolahan citra pada gambar yang telah dikumpulkan. Lakukan tiga tahap pengolahan: penambahan noise salt and pepper, penghilangan noise, dan penajaman citra.

### **a. Menambahkan Noise Salt and Pepper**

### **b. Menghilangkan Noise**

**c. Melakukan penjaman citra**

### **5. Dokumentasi dan Pengumpulan Hasil**

a. **Dokumentasi Proses**

- Buat dokumen PDF yang berisi:
  - **Deskripsi Aplikasi:** Penjelasan singkat tentang aplikasi yang dikembangkan.
  - **Langkah-langkah Penggunaan Aplikasi:** Cara menjalankan aplikasi dan menambahkan wajah ke dataset.
  - **Proses Pengolahan Citra:** Penjelasan tentang metode pengolahan citra yang diterapkan (penambahan noise, penghilangan noise, penajaman).
  - **Screenshot:** Tampilkan screenshot aplikasi saat menjalankan proses dan contoh hasil pengolahan citra.

b. **Kumpulan Citra**

- Pastikan folder `dataset` dan `processed_dataset` berisi:
  - **Citra Original:** Gambar wajah yang dikumpulkan melalui aplikasi.
  - **Citra Hasil Pengolahan:** Gambar yang telah ditambahkan noise, dihilangkan noisenya, dan ditajamkan.

c. **Pengemasan Hasil**

- Kumpulkan semua file berikut ke dalam satu file ZIP ( YY = Kelas , XXX = NIM ):
  - File PDF dokumentasi. (`[PCD2024_YY_xxx_D4_2022]_Modul4.pdf)`
  - Folder `dataset_XXX` dan `processed_dataset_XXX`.
- **Penamaan File ZIP:**
  - Contoh: `[PCD2024_YY_xxx_D4_2022]_Modul4.zip`

## **E. Penutup**

Pastikan semua langkah telah diikuti dengan benar dan hasil pengolahan citra telah terdokumentasi dengan baik. Periksa kembali semua file sebelum mengumpulkan untuk memastikan tidak ada yang terlewatkan. Selamat mengerjakan!
