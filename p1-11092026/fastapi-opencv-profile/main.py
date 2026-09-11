import json
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


def build_pixel_matrix(img, max_dim=20):
    """downsample the img to a small grid so teh pixels can be shown as a matrik"""
    h, w = img.shape[:2]
    scale = max_dim / max(h, w)
    new_w = max(1, round(w * scale))
    new_h = max(1, round(h * scale))
    small = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
    b, g, r = cv2.split(small)

    return [
        [{"r": int(r[y, x]), "g": int(g[y, x]), "b": int(b[y, x])} for x in range(new_w)]
        for y in range(new_h)
    ]


def build_histogram(channel):
    """count how many pixels fall into each intensity value (0-255) for one chammel"""
    hist = cv2.calcHist([channel], [0], None, [256], [0, 256])
    return hist.flatten().astype(int).tolist()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "home.html")

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
    pixel_matrix = build_pixel_matrix(img)
    histogram = {
        "R": build_histogram(r),
        "G": build_histogram(g),
        "B": build_histogram(b),
    }

    return templates.TemplateResponse(request, "display.html", {
        "image_path": f"/static/uploads/{filename}",
        "rgb_array": rgb_array,
        "pixel_matrix": pixel_matrix,
        "histogram_json": json.dumps(histogram)
    })
