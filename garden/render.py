import base64
import io
from pathlib import Path

from PIL import Image


_ASSETS = Path(__file__).parent.parent / "assets"

_FLOWER_SIZE = (80, 80)     # flower thumbnail
_STEM_SIZE   = (55, 95)     # stem thumbnail (narrower, taller than flower)


def _load_background(width: int, height: int) -> Image.Image:
    grass = Image.open(_ASSETS / "grass.png").convert("RGBA")
    grass = grass.resize((width, height), Image.LANCZOS)
    # Composite onto a sky-blue base in case of transparent pixels at the top
    bg = Image.new("RGBA", (width, height), (173, 216, 180))
    bg.paste(grass, mask=grass)
    return bg.convert("RGB")


def _load_stem() -> Image.Image:
    stem = Image.open(_ASSETS / "flower_stem.png").convert("RGBA")
    stem.thumbnail(_STEM_SIZE, Image.LANCZOS)
    return stem


def _decode_flower(image_b64: str) -> Image.Image:
    img = Image.open(io.BytesIO(base64.b64decode(image_b64))).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    img.thumbnail(_FLOWER_SIZE, Image.LANCZOS)
    return img


def _make_plant(flower: Image.Image, stem: Image.Image) -> Image.Image:
    """Stack flower on top of stem, both horizontally centred."""
    w = max(flower.width, stem.width)
    h = flower.height + stem.height
    plant = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    plant.paste(flower, ((w - flower.width) // 2, 0),             mask=flower)
    plant.paste(stem,   ((w - stem.width)   // 2, flower.height), mask=stem)
    return plant


def composite_garden(flowers: list[dict], width: int = 900, height: int = 600) -> Image.Image:
    canvas = _load_background(width, height).convert("RGBA")
    stem = _load_stem()

    for f in flowers:
        try:
            flower = _decode_flower(f["image_b64"])
            plant  = _make_plant(flower, stem)
        except Exception:
            continue

        # Anchor: bottom-centre of the plant at the planted (x, y) position
        px = int(f["x"] * width)  - plant.width  // 2
        py = int(f["y"] * height) - plant.height
        canvas.paste(plant, (px, py), mask=plant)

    return canvas.convert("RGB")
