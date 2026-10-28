#!/usr/bin/env python3
"""Render a supplied portrait as a colored character mosaic HTML artifact."""
from __future__ import annotations

import argparse
import html
from pathlib import Path

from PIL import Image, ImageOps

CHARS = "@%#*+=-:. "


def render(source: Path, output: Path, width: int = 108) -> None:
    image = Image.open(source).convert("RGB")
    image = ImageOps.exif_transpose(image)
    ratio = image.height / image.width
    height = max(1, int(width * ratio * 0.48))
    image = image.resize((width, height))
    cells: list[str] = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
            char = CHARS[min(len(CHARS) - 1, int(luminance * len(CHARS)))]
            row.append(f'<span style="color:rgb({r},{g},{b})">{html.escape(char)}</span>')
        cells.append("".join(row))
    output.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(cells)
    output.write_text(f'''<!doctype html>
<meta charset="utf-8">
<title>MockMill — Meek Mill fan-made color ASCII parody</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; background:#080b12; color:#dce8ee; font:14px/1.45 system-ui,sans-serif; }}
  main {{ max-width:1240px; margin:0 auto; padding:32px 20px 56px; }}
  h1 {{ margin:0 0 6px; font-size:28px; }}
  p {{ color:#9eb0bb; }}
  .notice {{ border-left:4px solid #55d6be; padding:10px 14px; background:#101c28; }}
  .art {{ overflow:auto; margin-top:24px; padding:20px; background:#05070b; border:1px solid #263746; border-radius:12px; }}
  pre {{ margin:0; font:8px/1 monospace; letter-spacing:0; }}
  a {{ color:#72d8c4; }}
</style>
<main>
  <h1>MOCK MILL — full-color ASCII portrait</h1>
  <p>A character-mosaic transformation for a clearly fictional, fan-made parody presentation.</p>
  <p class="notice"><strong>Not affiliated with, endorsed by or official artwork of Meek Mill.</strong><br>
  Source portrait: <a href="https://www.hotnewhiphop.com/profile/meekmill/mixtapes/popular/month/0">HotNewHipHop profile image</a>.
  The original photograph is not bundled in this repository.</p>
  <section class="art"><pre aria-label="Full-color ASCII portrait">{body}</pre></section>
</main>
''', encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=108)
    args = parser.parse_args()
    render(args.source, args.output, args.width)
