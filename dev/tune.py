"""
Interactive flower tuner.
Adjust sliders to explore parameters, then click Save to export a PNG.
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from flower import DahliaParams, draw_flower

# ── Initial parameters ────────────────────────────────────────────────────────

params = DahliaParams()

# ── Layout ────────────────────────────────────────────────────────────────────
#
#   [ sliders | flower ]
#

fig = plt.figure(figsize=(13, 7))
fig.patch.set_facecolor("#111111")

ax_flower = fig.add_axes([0.38, 0.04, 0.60, 0.94], projection="3d")
ax_flower.set_facecolor("#111111")

draw_flower(params, ax_flower)
fig.canvas.draw_idle()

# ── Slider definitions ────────────────────────────────────────────────────────

SLIDER_COLOR = "#333355"
LABEL_COLOR  = "#cccccc"

sliders = {}

def make_slider(ax_rect, label, valmin, valmax, valinit, valstep=None):
    ax = fig.add_axes(ax_rect, facecolor=SLIDER_COLOR)
    kw = dict(valmin=valmin, valmax=valmax, valinit=valinit,
              color=SLIDER_COLOR, handle_style={"facecolor": "#aaaaff", "size": 8})
    if valstep is not None:
        kw["valstep"] = valstep
    s = Slider(ax, label, **kw)
    s.label.set_color(LABEL_COLOR)
    s.valtext.set_color(LABEL_COLOR)
    return s


LEFT  = 0.06   # left edge of slider track
WIDTH = 0.26   # track width
ROW_H = 0.068  # vertical spacing between rows

def row(i):
    """Bottom position for row i (0 = top row)."""
    return 0.92 - i * ROW_H


# Shape sliders
sliders["ppr"]    = make_slider([LEFT, row(0), WIDTH, 0.03], "Petals / rev",   5.0,  20.0, params.petals_per_revolution)
sliders["pn"]     = make_slider([LEFT, row(1), WIDTH, 0.03], "Total petals",  50,   250,   params.total_petals,          valstep=10)
sliders["pf"]     = make_slider([LEFT, row(2), WIDTH, 0.03], "Petal tilt",    -2.5,  0.0,  params.petal_tilt)
sliders["ol_in"]  = make_slider([LEFT, row(3), WIDTH, 0.03], "Openness inner", 0.01, 0.5,  params.openness[0])
sliders["ol_out"] = make_slider([LEFT, row(4), WIDTH, 0.03], "Openness outer", 0.5,  2.5,  params.openness[1])

# Separator label
fig.text(LEFT, row(5) + 0.015, "─── Inner color (RGB) ───", color=LABEL_COLOR, fontsize=7)
sliders["ci_r"] = make_slider([LEFT, row(6), WIDTH, 0.03], "Red",   0.0, 1.0, params.color_inner[0])
sliders["ci_g"] = make_slider([LEFT, row(7), WIDTH, 0.03], "Green", 0.0, 1.0, params.color_inner[1])
sliders["ci_b"] = make_slider([LEFT, row(8), WIDTH, 0.03], "Blue",  0.0, 1.0, params.color_inner[2])

fig.text(LEFT, row(9) + 0.015, "─── Outer color (RGB) ───", color=LABEL_COLOR, fontsize=7)
sliders["co_r"] = make_slider([LEFT, row(10), WIDTH, 0.03], "Red",   0.0, 1.0, params.color_outer[0])
sliders["co_g"] = make_slider([LEFT, row(11), WIDTH, 0.03], "Green", 0.0, 1.0, params.color_outer[1])
sliders["co_b"] = make_slider([LEFT, row(12), WIDTH, 0.03], "Blue",  0.0, 1.0, params.color_outer[2])

# ── Buttons ───────────────────────────────────────────────────────────────────

ax_btn_redraw = fig.add_axes([LEFT,                row(13) - 0.01, WIDTH * 0.48, 0.04])
ax_btn_save   = fig.add_axes([LEFT + WIDTH * 0.52, row(13) - 0.01, WIDTH * 0.48, 0.04])

btn_redraw = Button(ax_btn_redraw, "Redraw",   color="#333355", hovercolor="#444466")
btn_save   = Button(ax_btn_save,   "Save PNG", color="#334433", hovercolor="#446644")
btn_redraw.label.set_color("#aaaaff")
btn_save.label.set_color("#aaffaa")

# ── Callbacks ─────────────────────────────────────────────────────────────────

def read_params() -> DahliaParams:
    return DahliaParams(
        petals_per_revolution=sliders["ppr"].val,
        total_petals=int(sliders["pn"].val),
        petal_tilt=sliders["pf"].val,
        openness=(sliders["ol_in"].val, sliders["ol_out"].val),
        color_inner=(sliders["ci_r"].val, sliders["ci_g"].val, sliders["ci_b"].val),
        color_outer=(sliders["co_r"].val, sliders["co_g"].val, sliders["co_b"].val),
    )


def update(_):
    draw_flower(read_params(), ax_flower)
    fig.canvas.draw_idle()


def save(_):
    p = read_params()
    out = "output.png"
    tmp_fig = plt.figure()
    tmp_ax = tmp_fig.add_subplot(projection="3d")
    draw_flower(p, tmp_ax)
    tmp_fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(tmp_fig)
    print(f"Saved {out}")


btn_redraw.on_clicked(update)
btn_save.on_clicked(save)

# ── Show ──────────────────────────────────────────────────────────────────────

plt.show()
