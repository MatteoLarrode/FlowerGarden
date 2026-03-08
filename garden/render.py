import base64
import io
from pathlib import Path

from PIL import Image


_ASSETS = Path(__file__).parent.parent / "assets"

# Stem size relative to the flower's tight bounding box
_STEM_WIDTH_RATIO = 0.6   # stem width = 60% of flower width; height is derived from the image's aspect ratio
_OVERLAP_RATIO    = 0.12  # petals overlap the stem top by 12% of flower height

# Garden thumbnail for the full flower+stem composite
LILY_THUMBNAIL  = (80, 140)   # water lily (no stem, floats on water)
SMALL_THUMBNAIL = (40, 75)    # dahlia & rose (with stem)


# ── Stem compositing (called at flower creation time) ─────────────────────────

def compose_with_stem(image_bytes: bytes) -> bytes:
    """Crop transparent padding, attach stem below, return PNG bytes."""
    flower = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    bbox = flower.getbbox()
    if bbox:
        flower = flower.crop(bbox)

    stem_src = Image.open(_ASSETS / "flower_stem.png").convert("RGBA")
    target_w = int(flower.width * _STEM_WIDTH_RATIO)
    target_h = int(target_w * stem_src.height / stem_src.width)
    stem = stem_src.resize((target_w, target_h), Image.LANCZOS)

    overlap = int(flower.height * _OVERLAP_RATIO)
    w = max(flower.width, stem.width)
    h = flower.height + stem.height - overlap
    plant = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # Stem first (behind), then flower on top so petals override the stem tip
    plant.paste(stem,   ((w - stem.width)   // 2, flower.height - overlap), mask=stem)
    plant.paste(flower, ((w - flower.width) // 2, 0),                       mask=flower)

    buf = io.BytesIO()
    plant.save(buf, format="png")
    return buf.getvalue()


# ── Garden compositing ────────────────────────────────────────────────────────

def _load_background(width: int, height: int) -> Image.Image:
    bg_src = Image.open(_ASSETS / "background_garden_joe.png").convert("RGBA")
    bg = bg_src.resize((width, height), Image.LANCZOS)
    return bg.convert("RGB")


def composite_garden(flowers: list[dict], width: int = 900, height: int = 600) -> Image.Image:
    canvas = _load_background(width, height).convert("RGBA")

    for f in flowers:
        try:
            img = Image.open(io.BytesIO(base64.b64decode(f["image_b64"]))).convert("RGBA")
            is_water_lily = isinstance(f.get("params"), dict) and "num_petals" in f["params"]
            thumb = LILY_THUMBNAIL if is_water_lily else SMALL_THUMBNAIL
            img.thumbnail(thumb, Image.LANCZOS)
        except Exception:
            continue

        # Anchor: bottom-centre of the plant at the planted (x, y) position
        px = int(f["x"] * width)  - img.width  // 2
        py = int(f["y"] * height) - img.height
        canvas.paste(img, (px, py), mask=img)

    return canvas.convert("RGB")
