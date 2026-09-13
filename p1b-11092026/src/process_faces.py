import os
import cv2
import numpy as np


def add_salt_and_pepper_noise(image, amount=0.02, salt_ratio=0.5):
    noisy = image.copy()
    h, w = image.shape[:2]
    num_pixels = int(amount * h * w)

    num_salt = int(num_pixels * salt_ratio)
    ys = np.random.randint(0, h, num_salt)
    xs = np.random.randint(0, w, num_salt)
    noisy[ys, xs] = 255

    num_pepper = num_pixels - num_salt
    ys = np.random.randint(0, h, num_pepper)
    xs = np.random.randint(0, w, num_pepper)
    noisy[ys, xs] = 0

    return noisy


def remove_noise(image, ksize=3):
    return cv2.medianBlur(image, ksize)


def sharpen_image(image):
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    return cv2.filter2D(image, -1, kernel)


def process_dataset(dataset_dir="dataset", output_dir="processed_dataset"):
    if not os.path.exists(dataset_dir):
        print(f"Folder '{dataset_dir}' tidak ditemukan.")
        return

    valid_ext = (".jpg", ".jpeg", ".png")

    for person_name in os.listdir(dataset_dir):
        person_path = os.path.join(dataset_dir, person_name)
        if not os.path.isdir(person_path):
            continue

        out_person_path = os.path.join(output_dir, person_name)
        os.makedirs(out_person_path, exist_ok=True)

        for filename in os.listdir(person_path):
            if not filename.lower().endswith(valid_ext):
                continue

            img_path = os.path.join(person_path, filename)
            image = cv2.imread(img_path)
            if image is None:
                print(f"Gagal membaca {img_path}, dilewati.")
                continue

            name, ext = os.path.splitext(filename)

            noisy = add_salt_and_pepper_noise(image)
            denoised = remove_noise(noisy)
            sharpened = sharpen_image(denoised)

            cv2.imwrite(os.path.join(out_person_path, f"{name}_noisy{ext}"), noisy)
            cv2.imwrite(os.path.join(out_person_path, f"{name}_denoised{ext}"), denoised)
            cv2.imwrite(os.path.join(out_person_path, f"{name}_sharpened{ext}"), sharpened)

            print(f"Selesai memproses {img_path}")

    print(f"Semua citra telah diproses dan disimpan di '{output_dir}'.")


if __name__ == "__main__":
    process_dataset()
