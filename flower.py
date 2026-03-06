from dataclasses import dataclass, field

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


@dataclass
class DahliaParams:
    # Shape
    petals_per_revolution: float = 12.6
    total_petals: int = 140
    radius_resolution: int = 30
    petal_resolution: int = 10
    petal_tilt: float = -1.2          # negative = petal tips tilt outward
    openness: tuple[float, float] = field(default_factory=lambda: (0.11, 1.1))  # [inner, outer]

    # Color — RGB components at the inner and outer edge of the petals
    color_inner: tuple[float, float, float] = (0.6, 0.1, 0.7)
    color_outer: tuple[float, float, float] = (1.0, 0.8, 1.0)


def draw_flower(params: DahliaParams, ax) -> None:
    """Draw the flower onto an existing 3D axes (clears it first)."""
    ppr = params.petals_per_revolution
    nr = params.radius_resolution
    pr = params.petal_resolution
    pn = params.total_petals
    pf = params.petal_tilt
    ol = params.openness

    pt = (1 / ppr) * np.pi * 2
    theta = np.linspace(0, pn * pt, pn * pr + 1)
    R, THETA = np.meshgrid(np.linspace(0, 1, nr), theta, indexing="ij")

    x = 1 - ((1 - np.mod(ppr * THETA, 2 * np.pi) / np.pi) ** 2) * 0.7
    phi = (np.pi / 2) * ((np.linspace(ol[0], ol[1], pn * pr + 1)) ** 2)
    y = pf * (R ** 2) * ((1.28 * R - 1) ** 2) * np.sin(phi)
    R2 = (x * (R * np.sin(phi))) + (y * np.cos(phi))

    X = R2 * np.sin(THETA)
    Y = R2 * np.cos(THETA)
    Z = x * ((R * np.cos(phi)) - (y * np.sin(phi)))

    vals = np.zeros((256, 3))
    for i, (c_in, c_out) in enumerate(zip(params.color_inner, params.color_outer)):
        vals[:, i] = np.linspace(c_in, c_out, 256)
    cmap = colors.ListedColormap(vals)

    ax.cla()
    ax.plot_surface(X, Y, Z, cmap=cmap, rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax.axis("equal")
    ax.axis("off")


def generate_flower(params: DahliaParams) -> plt.Figure:
    """Generate a flower into a new figure and return it."""
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    draw_flower(params, ax)
    return fig
