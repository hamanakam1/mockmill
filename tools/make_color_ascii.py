#!/usr/bin/env python3
"""Render a supplied portrait as a colored character mosaic HTML artifact."""
from __future__ import annotations

import argparse
import html
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

CHARS = "@%#*+=-:. "


def render(source: Path, output: Path, width: int = 108, label: str = "") -> None:
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
    if output.suffix.lower() == ".png":
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 9)
        canvas = Image.new("RGB", (width * 6 + 24, height * 10 + 24), "#05070b")
        draw = ImageDraw.Draw(canvas)
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
                char = CHARS[min(len(CHARS) - 1, int(luminance * len(CHARS)))]
                draw.text((12 + x * 6, 8 + y * 10), char, font=font, fill=(r, g, b))
        if label:
            label_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 18)
            label_lines = label.split(" / ")
            y = int(canvas.height * 0.68)
            for line in label_lines:
                box = draw.textbbox((0, 0), line, font=label_font)
                x = (canvas.width - (box[2] - box[0])) // 2
                draw.text((x + 2, y + 2), line, font=label_font, fill="#05070b", stroke_width=2, stroke_fill="#05070b")
                draw.text((x, y), line, font=label_font, fill="#f4d37d", stroke_width=1, stroke_fill="#fff4cf")
                y += 22
        output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output, "PNG")
        return
    if output.suffix.lower() == ".svg":
        lines = []
        for y, line in enumerate(cells):
            # SVG text preserves the colored character mosaic while GitHub can preview it inline.
            lines.append(f'<text x="24" y="{32 + y * 10}" xml:space="preserve">{line}</text>')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="{height * 10 + 64}" viewBox="0 0 1500 {height * 10 + 64}" role="img" aria-labelledby="title desc">
<title id="title">MockMill full-color ASCII parody portrait</title>
<desc id="desc">A high-detail colored character mosaic based on a public Meek Mill promotional portrait. Fan-made parody, not affiliated or endorsed.</desc>
<rect width="1500" height="100%" fill="#05070b"/><g font-family="monospace" font-size="10">{''.join(lines)}</g></svg>''', encoding="utf-8")
        return
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
    parser.add_argument("--label", default="")
    args = parser.parse_args()
    render(args.source, args.output, args.width, args.label)
