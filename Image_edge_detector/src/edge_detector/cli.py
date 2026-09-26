"""Command-line Sobel edge detector."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from edge_detector.processing import apply_threshold, detect_edges, edges_to_pil

DEFAULT_THRESHOLD = 40


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect edges in an image with Sobel (NumPy + Pillow).",
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to the source image (PNG, JPEG, BMP, WebP).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Where to write the edge map (default: <input>_edges.png).",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        metavar="N",
        help=f"Keep pixels with magnitude >= N (0-255, default {DEFAULT_THRESHOLD}).",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Black edges on a white background instead of white on black.",
    )
    return parser.parse_args(argv)


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_edges.png")


def run(args: argparse.Namespace) -> int:
    input_path: Path = args.input
    if not input_path.is_file():
        print(f"error: input not found: {input_path}", file=sys.stderr)
        return 1

    threshold = args.threshold
    if not 0 <= threshold <= 255:
        print("error: --threshold must be between 0 and 255", file=sys.stderr)
        return 1

    try:
        with Image.open(input_path) as image:
            image.load()
            magnitude = detect_edges(image)
    except (OSError, UnidentifiedImageError) as exc:
        print(f"error: could not open image: {exc}", file=sys.stderr)
        return 1

    edges = apply_threshold(magnitude, threshold, invert=args.invert)
    output_path = args.output or default_output_path(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        edges_to_pil(edges).save(output_path)
    except OSError as exc:
        print(f"error: could not save: {exc}", file=sys.stderr)
        return 1

    height, width = magnitude.shape
    print(
        f"Sobel edges written to {output_path} "
        f"({width}x{height}, threshold={threshold}"
        f"{', inverted' if args.invert else ''})"
    )
    return 0


def main(argv: list[str] | None = None) -> None:
    raise SystemExit(run(parse_args(argv)))
