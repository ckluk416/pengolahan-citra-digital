# P2 Report: FastAPI Image Processing App

Course: Pengolahan Citra Digital, semester 5
Student: Fathin Y (241524041)
Source material: `PCD 26 Agustus 2024 - POLBAN.md` (tutorial) and `Copy_of_PCD_9_September_2024_Pertemuan_4.ipynb` (Colab notebook)
Project folder: `fastapi-opencv-26agustus/`

## 1. Step 9: what I did and what I found

The tutorial ends with four short steps: understand the code, add it to your project folder, test every operation and fix what breaks, then document. This section covers steps 6 through 9.

### 1.1 Copying the tutorial code

I copied `main.py` and the eight templates from the tutorial as written. Running `uvicorn main:app --reload` started without errors, but every page returned HTTP 500. The traceback ended in `TypeError: unhashable type: 'dict'` inside Jinja2's template cache.

### 1.2 Root cause

The tutorial was written for FastAPI 0.11x in 2024. This repo pins FastAPI 0.141 and Starlette 1.6. Starlette 1.0 removed the old call form:

```python
# tutorial (no longer accepted)
templates.TemplateResponse("home.html", {"request": request, ...})

# current
templates.TemplateResponse(request, "home.html", {...})
```

With the old form, Starlette treats the dict as the template name and hands it to Jinja2, which tries to use it as a cache key and fails. Every route in the tutorial uses this call, so every route failed. I had already hit the same problem in the P1 project, so the fix was known.

### 1.3 Other defects found while testing

I wrote a test script that posts synthetic images to every endpoint, including bad inputs. It found six more problems:

| # | Problem | How it showed up | Fix |
|---|---|---|---|
| 1 | Template file named `histrogram.html` | `/histogram/` raised `TemplateNotFound` | Renamed to `histogram.html` |
| 2 | Matplotlib used the Tk GUI backend | `Tcl_AsyncDelete: async handler deleted by the wrong thread` after the first histogram request; the process could crash | `matplotlib.use("Agg")` before importing `pyplot` |
| 3 | No check that `cv2.imdecode` succeeded | Uploading a `.txt` file crashed in `cv2.cvtColor` with a 500 | Shared `read_upload()` helper; routes return 400 when it gives `None` |
| 4 | AND / XOR with two images of different size | `cv2.bitwise_and` assertion error | Resize the second image to the first |
| 5 | The `file2 is None` check for AND / XOR never fired | Browsers send an empty file part when the user picks nothing, so `file2` is an `UploadFile` with zero bytes | Decode first, then check for `None` |
| 6 | Slider value written into `np.full(..., dtype=uint8)` | Values above 255 wrap silently | Clip to 0..255 |

I also gave the histogram plots titles and axis labels, and rounded the statistics output to two decimals.

### 1.4 Test results

After the fixes, 23 request cases pass: five GET pages, every arithmetic and logic operation, grayscale, histogram, equalization, specification with same size, different size, and grayscale reference, and statistics. The two intentional bad inputs (a text file, and AND with no second image) return 400 with a message instead of 500.

## 2. How the notebook maps to this project

`src/message.txt` asks for the Colab notebook to be turned into FastAPI endpoints and integrated with the web app. The notebook is a linear script: upload one image with `google.colab.files.upload()`, then run five functions on it and show each result with `IPython.display`.

The web app already does the same three things as the notebook, just with different plumbing:

| Notebook | FastAPI project |
|---|---|
| `files.upload()` returns a dict of bytes | `UploadFile = File(...)` parameter on a POST route |
| `read_image()` does `np.frombuffer` + `cv2.imdecode` | `read_upload()` in `main.py`, same two calls |
| Five processing functions in separate cells | Same five functions in `filters.py` |
| `display_image()` encodes to PNG and shows it inline | `save_image()` writes a PNG to `static/uploads/` and `result.html` shows it with an `<img>` tag |
| Change a string literal and re-run the cell | `<select name="operation">` in `filter.html` |

So the notebook's cells 1 to 3 (upload and decode) already existed in the app. The work was moving cells 4 to 12 into `filters.py`, adding one route that picks a function by name, and adding a form page.

### 2.1 Changes to the notebook code

Three functions produced output that could not be saved as an image or produced wrong output, so I changed them. The rest is copied unchanged.

**Band-pass filter.** The notebook computes `image - low_pass` and then `low_pass + high_pass` on `uint8` arrays. Subtraction wraps around at zero (5 - 10 becomes 251), so the result is noise, and the final addition undoes the subtraction anyway. The replacement casts to `float32`, takes the difference of two Gaussian blurs (kernel 3 minus kernel 9), and normalizes back to `uint8`.

**Fourier spectrum.** `20 * np.log(np.abs(fshift))` gives `-inf` wherever the spectrum is exactly zero, and the result is a `float64` array. `cv2.imwrite` needs `uint8`. I added `+ 1` inside the log and a `to_uint8()` helper that replaces inf/nan and min-max normalizes to 0..255.

**Periodic noise reduction.** Same output type problem, same `to_uint8()` fix. I also made the mask radius a parameter and clamped the slice indices so a radius larger than the image does not produce a negative index.

I kept the notebook's algorithm for periodic noise as written, but it does not do what its name says. It zeroes a square at the center of the shifted spectrum. The center holds the low frequencies, which carry the overall brightness and the large shapes. Removing them leaves only edges and fine texture. That is a high-pass filter. Real periodic noise appears as bright dots away from the center, and removing it means notching those dots while keeping the center. My test image (a gradient, a bright square, and vertical stripes with period 8) confirmed this: after "noise reduction" the gradient and square were gone, and the stripes were still there. I noted this in a comment in `filters.py` rather than changing the behavior, since the assignment asks to convert the notebook code.

### 2.2 Test results for the filter route

Nine operations return 200 with images that have full 0..255 range and non-zero variance (so not blank). Zero padding with 25 px grows a 160x200 image to 210x250. An unknown operation name returns 400. The Fourier output shows the expected bright center plus a horizontal row of dots at the stripe frequency.

## 3. API reference

All routes accept `multipart/form-data` and return HTML. Uploaded and processed images are written to `static/uploads/` as PNG with a UUID filename and served back through the `/static` mount. Histogram plots go to `static/histograms/`.

Every POST route returns **400** with a plain text message if the uploaded file cannot be decoded as an image.

### GET routes (form pages)

| Path | Template | Purpose |
|---|---|---|
| `/` | `home.html` | Upload, arithmetic, logic, and statistics forms |
| `/grayscale/` | `grayscale.html` | Grayscale form |
| `/histogram/` | `histogram.html` | Histogram form |
| `/equalize/` | `equalize.html` | Equalization form |
| `/specify/` | `specify.html` | Specification form (two files) |
| `/filter/` | `filter.html` | Filtering and Fourier form |

### POST /upload/

| Field | Type | Notes |
|---|---|---|
| `file` | image | required |

Decodes and re-saves the image. Renders `result.html` with the same image on both sides. Used to confirm the upload path works.

### POST /operation/

| Field | Type | Notes |
|---|---|---|
| `file` | image | required |
| `operation` | `add`, `subtract`, `max`, `min`, `inverse` | required |
| `value` | int | 0..100 from the slider; clipped to 0..255 server side |

`add` and `subtract` use `cv2.add` / `cv2.subtract`, which saturate at 0 and 255. `max` and `min` clamp each pixel against `value`. `inverse` is `255 - pixel` and ignores `value`.

### POST /logic_operation/

| Field | Type | Notes |
|---|---|---|
| `file1` | image | required |
| `file2` | image | required for `and` and `xor`; ignored for `not` |
| `operation` | `not`, `and`, `xor` | required |

If `file2` is missing or empty for `and` / `xor`, returns 400 with "Operasi AND dan XOR memerlukan dua gambar." If the two images differ in size, `file2` is resized to match `file1`.

### POST /grayscale/

| Field | Type | Notes |
|---|---|---|
| `file` | image | required |

`cv2.cvtColor(img, COLOR_BGR2GRAY)`. Result is a single channel PNG.

### POST /histogram/

| Field | Type | Notes |
|---|---|---|
| `file` | image | required |

Produces two Matplotlib plots: a 256-bin histogram of the grayscale image, and one line per B, G, R channel from `cv2.calcHist`. Renders `histogram.html` with both plot paths so the form stays on screen above the results.

### POST /equalize/

| Field | Type | Notes |
|---|---|---|
| `file` | image | required, read as grayscale |

`cv2.equalizeHist`. Both the original and the result are grayscale.

### POST /specify/

| Field | Type | Notes |
|---|---|---|
| `file` | image | required, the image to change |
| `ref_file` | image | required, the histogram to match |

`skimage.exposure.match_histograms(img, ref_img, channel_axis=-1)`. Images may differ in size. Both are read as 3-channel BGR, so a grayscale reference is expanded to three equal channels by `imdecode`. Returns 400 with "Gambar utama atau gambar referensi tidak dapat dibaca." if either fails to decode.

### POST /statistics/

| Field | Type | Notes |
|---|---|---|
| `file` | image | required, read as grayscale |

Renders `statistics.html` with `mean_intensity` (`np.mean`, brightness) and `std_deviation` (`np.std`, contrast), both rounded to two decimals.

### POST /filter/

| Field | Type | Notes |
|---|---|---|
| `file` | image | required |
| `operation` | see table below | required |
| `padding_size` | int | default 20; used by `zero_padding` only |
| `radius` | int | default 30; used by `periodic_noise` only |

| `operation` | Function in `filters.py` | What it does |
|---|---|---|
| `conv_average` | `apply_convolution(img, "average")` | 3x3 box blur, `cv2.filter2D` |
| `conv_sharpen` | `apply_convolution(img, "sharpen")` | 3x3 sharpen kernel (center 5, cross -1) |
| `conv_edge` | `apply_convolution(img, "edge")` | 3x3 Laplacian-style kernel (center 8, ring -1) |
| `zero_padding` | `apply_zero_padding(img, padding_size)` | `cv2.copyMakeBorder` with black border; output is larger than input |
| `filter_low` | `apply_filter(img, "low")` | 5x5 Gaussian blur |
| `filter_high` | `apply_filter(img, "high")` | Same kernel as `conv_sharpen` |
| `filter_band` | `apply_filter(img, "band")` | Gaussian(3) minus Gaussian(9) in float, normalized |
| `fourier` | `apply_fourier_transform(img)` | Grayscale, `fft2`, `fftshift`, `20*log(|F|+1)`, normalized; single channel output |
| `periodic_noise` | `reduce_periodic_noise(img, radius)` | Zero a `2r x 2r` square at the spectrum center, inverse FFT, normalized; single channel output |

Unknown `operation` values return 400.

## 4. Running

```
cd p2-18092026/fastapi-opencv-26agustus
uv run uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/. Dependencies are in the repo root `pyproject.toml`: fastapi, uvicorn, jinja2, python-multipart, opencv-python-headless, numpy, matplotlib, scikit-image.

## 5. File layout

```
fastapi-opencv-26agustus/
├── main.py          routes, upload decoding, save helpers
├── filters.py       the five notebook functions plus to_uint8()
├── static/
│   ├── uploads/     input and output PNGs (ignored by git)
│   └── histograms/  Matplotlib plots (ignored by git)
└── templates/
    ├── base.html        navbar, sidebar, Bootstrap
    ├── home.html        upload, arithmetic, logic, statistics forms
    ├── result.html      side by side original and result
    ├── grayscale.html
    ├── histogram.html   form plus the two plots when present
    ├── equalize.html
    ├── specify.html
    ├── statistics.html
    └── filter.html      notebook operations
```

## 6. Conclusion

The tutorial code is a correct description of the algorithms but does not run on current FastAPI without changing every `TemplateResponse` call. Once that was fixed, the remaining bugs were all input handling: bad files, mismatched sizes, and the way browsers submit empty file inputs. None of the OpenCV calls themselves needed changing.

Moving the notebook into the app was mostly a matter of removing Colab-specific I/O. The processing functions transferred with two kinds of edits: casting to float where the notebook did arithmetic on `uint8`, and normalizing float results to `uint8` before saving. The notebook could hide both problems because `display_image` re-encodes whatever it gets and the human eye tolerates a wrapped or clipped image on screen. A file on disk is less forgiving.

The one algorithmic finding is that the notebook's periodic noise function is a high-pass filter. It is worth keeping as an example of what removing low frequencies does, but a real noise removal step would need to locate the noise peaks in the spectrum first.
