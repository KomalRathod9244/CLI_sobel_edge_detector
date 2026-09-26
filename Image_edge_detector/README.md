# Image Edge Detector

Mini project: find edges in a photo from the command line with **NumPy** convolution and **Pillow**.

## Layout

```text
Image_edge_detector/
  app.py                      # CLI entry point
  requirements.txt
  README.md
  src/
    edge_detector/
      __init__.py             # public processing API
      processing.py           # grayscale, Sobel, threshold
      cli.py                  # argparse interface
```

## How it works

1. Convert the image to grayscale (Rec. 601 luminance).
2. Convolve with Sobel kernels `Gx` and `Gy`.
3. Combine into a gradient magnitude and scale it to 0–255.
4. A threshold keeps only stronger edge pixels.

Sobel already includes a little smoothing, so there is no extra blur step.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python app.py photo.jpg
python app.py photo.jpg -o edges.png -t 50 --invert
python app.py --help
```

| Flag | Meaning |
| --- | --- |
| `input` | Source image (PNG, JPEG, BMP, WebP, …) |
| `-o`, `--output` | Output path (default: `<name>_edges.png` next to the input) |
| `-t`, `--threshold` | Keep magnitude ≥ N (0–255, default 40) |
| `--invert` | Black edges on white instead of white on black |
