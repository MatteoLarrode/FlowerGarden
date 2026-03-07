import base64
import io

from PIL import Image


_GARDEN_BG = (34, 85, 34)       # dark green
_THUMBNAIL_SIZE = (80, 80)      # flower size when composited into the garden


def _make_background(width: int, height: int) -> Image.Image:
    return Image.new("RGB", (width, height), _GARDEN_BG)


def _decode_flower(image_b64: str, size: tuple[int, int]) -> Image.Image:
    img = Image.open(io.BytesIO(base64.b64decode(image_b64))).convert("RGBA")
    img.thumbnail(size, Image.LANCZOS)
    return img


def composite_garden(flowers: list[dict], width: int = 900, height: int = 600) -> Image.Image:
    canvas = _make_background(width, height)
    for f in flowers:
        try:
            thumb = _decode_flower(f["image_b64"], _THUMBNAIL_SIZE)
        except Exception:
            continue
        px = int(f["x"] * width) - thumb.width // 2
        py = int(f["y"] * height) - thumb.height // 2
        canvas.paste(thumb, (px, py), mask=thumb)
    return canvas
