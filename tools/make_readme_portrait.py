#!/usr/bin/env python3
"""Reproduce the approved dark-theme README portrait as selectable text.

Optional artwork tool; requires Pillow (approved output used Pillow 12.2.0).
It is independent of MockMill's standard-library-only data generators.

    python tools/make_readme_portrait.py source.jpg --output portrait.txt
    python tools/make_readme_portrait.py source.jpg --check-readme README.md

Reference: https://pbs.twimg.com/media/HEMgpLjXMAAb8Em.jpg
Context: https://x.com/MeekMill/status/2036577255665647771
The original photograph is not distributed with the package. The fixed crop
and source hash prevent silently reproducing a different approved likeness.
Trailing spaces are intentional: every row has 76 cells so GitHub's centered
preformatted block keeps the portrait and shirt aligned.
"""

import argparse
import hashlib
import html
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


SOURCE_SHA256 = "e547d2d72180512bc32e14b3ec4708de8a079d75c78f1633c20023b456546173"
PORTRAIT_SHA256 = "cfe052b92a2dff910eee5b401cfc53a6b590738680a49f6467b5bec3c638bd99"
COLS, ROWS, CANVAS = 60, 27, 76
BRAILLE_BITS = ((0, 3), (1, 4), (2, 5), (6, 7))
LETTERS = {
    "M": ["##   ##", "### ###", "## # ##", "##   ##", "##   ##"],
    "O": [" ##### ", "##   ##", "##   ##", "##   ##", " ##### "],
    "C": [" ##### ", "##     ", "##     ", "##     ", " ##### "],
    "K": ["##   ##", "##  ## ", "#####  ", "##  ## ", "##   ##"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "#####"],
    "L": ["##   ", "##   ", "##   ", "##   ", "#####"],
}


def make_portrait(source: Path) -> str:
    if hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("Source image differs from the approved reference")
    with Image.open(source) as original:
        crop = original.convert("L").crop((405, 0, 825, 445))
    small = crop.resize((COLS * 2, ROWS * 4), Image.Resampling.LANCZOS)
    small = ImageOps.autocontrast(small, cutoff=1)
    small = small.filter(ImageFilter.UnsharpMask(radius=1.4, percent=120, threshold=3))

    # Exclude only the bright backdrop connected to the image corners.
    # Do not flood dark corners: that would erase the face itself.
    background = small.point(lambda value: 255 if value >= 218 else 0)
    for corner in ((0, 0), (COLS * 2 - 1, 0), (0, ROWS * 4 - 1),
                   (COLS * 2 - 1, ROWS * 4 - 1)):
        if background.getpixel(corner) == 255:
            ImageDraw.floodfill(background, corner, 128, thresh=0)
    outside = background.point(lambda value: 255 if value == 128 else 0)
    positive = ImageOps.invert(ImageEnhance.Contrast(small).enhance(1.12))
    positive = Image.composite(Image.new("L", small.size, 255), positive, outside)
    pixels = positive.convert("1", dither=Image.Dither.FLOYDSTEINBERG).convert("L")

    # Dots represent highlights on a dark surface; each glyph stores 2 x 4 dots.
    lines = []
    for y in range(ROWS):
        glyphs = []
        for x in range(COLS):
            value = sum(
                1 << BRAILLE_BITS[dy][dx]
                for dy in range(4) for dx in range(2)
                if pixels.getpixel((x * 2 + dx, y * 4 + dy)) < 128
            )
            glyphs.append(chr(0x2800 + value))
        lines.append(" " * 8 + "".join(glyphs) + " " * 8)

    logo = [
        " ".join(" " if char == " " else LETTERS[char][row] for char in "MOCK MILL")
        .replace("#", "█")
        for row in range(5)
    ]
    lines.extend([
        "                  __/ \\____________/ \\__                  ".center(CANVAS),
        "          ___..--'                      '--..___          ".center(CANVAS),
        "     _.-'                                      '-._      ".center(CANVAS),
    ])
    for line in logo + ["", "F A K E  D A T A   /   R E A L  F L O W"]:
        lines.append((" /|" + line.center(62) + "|\\ ").center(CANVAS))
    lines.append((" /|" + "_" * 62 + "|\\ ").center(CANVAS))
    result = "\n".join(lines) + "\n"
    if len(lines) != 38 or any(len(line) != CANVAS for line in lines):
        raise ValueError("Portrait geometry changed")
    if hashlib.sha256(result.encode("utf-8")).hexdigest() != PORTRAIT_SHA256:
        raise ValueError("Rendering differs from the approved output; check Pillow version")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-readme", type=Path)
    args = parser.parse_args()
    try:
        portrait = make_portrait(args.source)
    except ValueError as exc:
        parser.error(str(exc))
    if args.check_readme:
        readme = args.check_readme.read_text(encoding="utf-8")
        expected = "<pre>\n" + html.escape(portrait, quote=False) + "</pre>"
        if readme.count(expected) != 1:
            parser.error("README does not contain exactly one approved portrait")
        print("Approved portrait verified: 76 columns, 38 rows, exact SHA-256 match.")
    elif args.output:
        args.output.write_text(portrait, encoding="utf-8")
    else:
        sys.stdout.write(portrait)


if __name__ == "__main__":
    main()
