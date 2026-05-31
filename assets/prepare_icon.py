#!/usr/bin/env python3
"""Convert assets/icon_source.png to icon.png and multi-size icon.ico."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install pillow")
    sys.exit(1)

ASSETS = Path(__file__).resolve().parent
SOURCE = ASSETS / "icon_source.png"
ICON_PNG = ASSETS / "icon.png"
ICON_ICO = ASSETS / "icon.ico"
ICO_SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (96, 96), (128, 128), (256, 256)]


def main() -> None:
    if not SOURCE.is_file():
        print(f"Not found: {SOURCE}")
        sys.exit(1)

    img = Image.open(SOURCE).convert("RGBA")
    img.save(ICON_PNG)
    print(f"Created {ICON_PNG}")

    frames: list[Image.Image] = []
    for w, h in ICO_SIZES:
        resized = img.resize((w, h), Image.Resampling.LANCZOS)
        rgb = Image.new("RGB", (w, h), (10, 12, 18))
        rgb.paste(resized, mask=resized.split()[3])
        frames.append(rgb)

    frames[0].save(
        ICON_ICO,
        format="ICO",
        sizes=[(s[0], s[1]) for s in ICO_SIZES],
        append_images=frames[1:],
    )
    print(f"Created {ICON_ICO} ({len(ICO_SIZES)} sizes)")


if __name__ == "__main__":
    main()
