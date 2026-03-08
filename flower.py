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


# ---------------------------------------------------------------------------
# Red Rose
# ---------------------------------------------------------------------------

@dataclass
class RedRoseParams:
    # Shape
    petals_per_revolution: float = 3.6
    total_petals: int = 40
    radius_resolution: int = 30
    petal_resolution: int = 30
    petal_tilt: float = 2.0
    petal_separation: float = 1.25
    openness: tuple[float, float] = field(default_factory=lambda: (0.2, 1.02))


def draw_red_rose(params: RedRoseParams, ax) -> None:
    """Draw a red rose onto an existing 3D axes (clears it first)."""
    ppr = params.petals_per_revolution
    nr = params.radius_resolution
    pr = params.petal_resolution
    pn = params.total_petals
    pf = params.petal_tilt
    ps = params.petal_separation
    ol = params.openness

    pt = (1 / ppr) * np.pi * 2
    theta = np.linspace(0, pn * pt, pn * pr + 1)
    R, THETA = np.meshgrid(np.linspace(0, 1, nr), theta, indexing="ij")

    x = 1 - ((ps * ((1 - np.mod(ppr * THETA, 2 * np.pi) / np.pi) ** 2) - 0.25) ** 2) / 2
    phi = (np.pi / 2) * (np.linspace(ol[0], ol[1], pn * pr + 1)) ** 2
    y = pf * (R ** 2) * ((1.28 * R - 1) ** 2) * np.sin(phi)
    R2 = (x * (R * np.sin(phi))) + (y * np.cos(phi))

    X = R2 * np.sin(THETA)
    Y = R2 * np.cos(THETA)
    Z = x * ((R * np.cos(phi)) - (y * np.sin(phi)))

    C = np.hypot(np.hypot(X, Y), Z)
    C_norm = (C - C.min()) / (C.max() - C.min())
    C_face = (C_norm[:-1, :-1] + C_norm[1:, :-1] + C_norm[:-1, 1:] + C_norm[1:, 1:]) / 4

    ax.cla()
    ax.plot_surface(X, Y, Z, facecolors=plt.cm.hot_r(C_face),
                    rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax.axis("equal")
    ax.axis("off")


def generate_red_rose(params: RedRoseParams | None = None) -> plt.Figure:
    """Generate a red rose into a new figure and return it."""
    if params is None:
        params = RedRoseParams()
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    draw_red_rose(params, ax)
    return fig


# ---------------------------------------------------------------------------
# Water Lily
# ---------------------------------------------------------------------------

@dataclass
class WaterLilyParams:
    num_petals: int = 60
    vertices_per_petal_theta: int = 23
    vertices_per_petal_r: int = 15
    # 4 hex colours used as colormap control points: innermost → outermost
    petal_colors: tuple[str, str, str, str] = field(
        default_factory=lambda: ("#c7d49c", "#d5ebbd", "#f8e70c", "#bf5700")
    )


def draw_water_lily(params: WaterLilyParams, ax) -> None:
    """Draw a water lily onto an existing 3D axes (clears it first)."""
    npetals = params.num_petals
    vpp = params.vertices_per_petal_theta
    vrpp = params.vertices_per_petal_r

    def lsp(n):
        return np.linspace(0, 1, n)

    def lsv(n):
        return np.linspace(-1, 1, n)

    def ip1(r, v, n):
        return np.interp(np.arange(n), np.array(r) * (n - 1), v)

    PR = 1 - np.abs(lsv(vpp))  # (vpp,) — V-shaped petal profile

    # Fibonacci spiral angles, modulated by petal-width scale
    scale = ip1([0, .5, 1], [.3, .8, .1], npetals)          # (npetals,)
    PT_ROWS = (lsv(vpp) / 2)[np.newaxis, :] * scale[:, np.newaxis]  # (npetals, vpp)
    phi_offset = (1 + np.sqrt(5)) * np.arange(1, npetals + 1)
    PTHETA_VEC = (PT_ROWS + phi_offset[:, np.newaxis]).ravel()       # (npetals*vpp,)

    # Polar elevation (phi) for each petal, increasing outward
    rescaled = lsp(npetals) ** 0.9 * 0.4                             # (npetals,)
    PPHI_VEC = (np.ones((npetals, vpp)) * rescaled[:, np.newaxis]).ravel()  # (npetals*vpp,)

    # PPHI_MESH adds a U-shaped warp across each petal's radial extent
    PPHI_MESH = PPHI_VEC[np.newaxis, :] + (lsp(vrpp) ** 4 * 0.03)[:, np.newaxis]  # (vrpp, npetals*vpp)

    # Small per-petal phi correction for tip tilt
    dphi_scale = ip1([0, .5, 1], [0, .05, .1], npetals)             # (npetals,)
    DPHI = (PR[np.newaxis, :] * dphi_scale[:, np.newaxis]).ravel()   # (npetals*vpp,)

    # Radial extent of each petal, shrinking toward the outside
    petal_scale = np.linspace(1, .5, npetals) ** 2                   # (npetals,)
    PMR_cols = (PR[np.newaxis, :] * petal_scale[:, np.newaxis]).ravel()  # (npetals*vpp,)
    PMR_MESH = PMR_cols[np.newaxis, :] * lsp(vrpp)[:, np.newaxis]   # (vrpp, npetals*vpp)

    CORE = lsp(vpp * npetals) ** 2 * 0.6                            # (npetals*vpp,)

    PHI_TOTAL = PPHI_MESH + DPHI[np.newaxis, :]
    W = np.cos(np.pi * PHI_TOTAL) * (PMR_MESH + CORE[np.newaxis, :])

    X = np.cos(np.pi * PTHETA_VEC)[np.newaxis, :] * W
    Y = np.sin(np.pi * PTHETA_VEC)[np.newaxis, :] * W
    Z = np.sin(np.pi * PHI_TOTAL) * PMR_MESH * 1.7 + CORE[np.newaxis, :] * 0.4

    # Custom colormap interpolated through the 4 petal control colours
    yellow_rgb = np.array([colors.to_rgb(c) for c in params.petal_colors])
    ctrl_pts = np.array([0, .4, .8, 1]) * 255
    cmap_vals = np.zeros((256, 3))
    for ch in range(3):
        cmap_vals[:, ch] = np.interp(np.arange(256), ctrl_pts, yellow_rgb[:, ch])
    cmap = colors.ListedColormap(cmap_vals)

    C_face = (PPHI_MESH[:-1, :-1] + PPHI_MESH[1:, :-1] + PPHI_MESH[:-1, 1:] + PPHI_MESH[1:, 1:]) / 4
    C_norm = (C_face - C_face.min()) / (C_face.max() - C_face.min())

    ax.cla()
    ax.plot_surface(X, Y, Z, facecolors=cmap(C_norm),
                    rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax.axis("equal")
    ax.axis("off")


def generate_water_lily(params: WaterLilyParams | None = None) -> plt.Figure:
    """Generate a water lily into a new figure and return it."""
    if params is None:
        params = WaterLilyParams()
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    draw_water_lily(params, ax)
    return fig
