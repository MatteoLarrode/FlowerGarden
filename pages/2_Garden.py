import base64 as _b64
import io as _io

import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

from garden.storage import get_all_flowers, plant_flower
from garden.render import composite_garden, LILY_THUMBNAIL, SMALL_THUMBNAIL

GARDEN_W = 900
GARDEN_H = 600

st.set_page_config(page_title="The Garden", layout="wide")

fr = st.toggle("🇫🇷 Français", value=False)

if fr:
    st.markdown("*Ce jardin est vide à l'heure où j'écris ça, voyons voir ce qu'il devient! Merci à Joe Larrodé pour cette magnifique illustration !*")
else:
    st.markdown("*This garden was empty at the time of writing, let's see what it becomes! Thanks Joe Larrodé for the wonderful drawing!*")

# Remove header, zero padding, prevent scroll, fill viewport
st.markdown("""
<style>
[data-testid="stHeader"] { display: none; }
[data-testid="stAppViewBlockContainer"],
.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
    max-width: 100% !important;
}
html, body, [data-testid="stAppViewContainer"], .main {
    overflow: hidden !important;
    height: 100vh !important;
}
[data-testid="stPlotlyChart"] {
    height: calc(100vh - 0.5rem) !important;
}
[data-testid="stPlotlyChart"] > div,
[data-testid="stPlotlyChart"] iframe {
    height: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load flowers ──────────────────────────────────────────────────────────────

try:
    flowers = get_all_flowers()
except Exception as e:
    st.error(f"Could not connect to the garden database: {e}")
    st.info("Make sure your Supabase credentials are set in `.streamlit/secrets.toml`.")
    st.stop()

# ── Garden image ──────────────────────────────────────────────────────────────

garden_img = composite_garden(flowers, GARDEN_W, GARDEN_H)

has_flower = "flower_b64" in st.session_state
planting_mode = has_flower and st.session_state.get("flower_name", "")

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    if not has_flower:
        if fr:
            st.info("Va d'abord dans **My Flower** pour générer ta fleur, puis reviens ici pour la planter.")
        else:
            st.info("Head to **My Flower** first to generate your flower, then come back here to plant it.")
    elif planting_mode:
        if fr:
            st.info(
                f"Bonjour **{st.session_state['flower_name']}** ! "
                "Clique n'importe où dans le jardin pour choisir où planter ta fleur."
            )
        else:
            st.info(
                f"Hi **{st.session_state['flower_name']}**! "
                "Click anywhere in the garden to choose where to plant your flower."
            )
    else:
        if fr:
            st.caption("Passe la souris sur une fleur pour voir qui l'a plantée.")
        else:
            st.caption("Hover over a flower to see who planted it.")

# ── Garden image ───────────────────────────────────────────────────────────────

if planting_mode:
    # Click-to-plant mode: use streamlit_image_coordinates for click capture
    coords = streamlit_image_coordinates(garden_img, key="garden_click")
    if coords:
        plant_flower(
            name=st.session_state["flower_name"],
            x=coords["x"] / GARDEN_W,
            y=coords["y"] / GARDEN_H,
            params=st.session_state["flower_params"],
            image_b64=st.session_state["flower_b64"],
        )
        del st.session_state["flower_b64"]
        st.rerun()

else:
    # View mode: Plotly figure with invisible markers for name tooltips on hover.
    # Axes are normalised to [0, 1] with y=0 at the bottom (Plotly default).
    # The image is anchored at (0, 1) top-left so it fills the full [0,1]×[0,1] area.
    # Flower y fractions (0 = top, 1 = bottom) are flipped to match this convention.
    _buf = _io.BytesIO()
    garden_img.save(_buf, format="PNG")
    _img_b64 = _b64.b64encode(_buf.getvalue()).decode()

    # Compute the plotly y of the hover marker for each plant.
    # The flower head sits near the top of the image (stem fills most of the height for stemmed
    # flowers; water lilies have no stem but the blossom is also near the top).  Placing the
    # marker at 80 % of the image height from the bottom anchor keeps it on the visible flower.
    def _flower_top_y(f: dict) -> float:
        _fi = Image.open(_io.BytesIO(_b64.b64decode(f["image_b64"])))
        is_lily = isinstance(f.get("params"), dict) and "num_petals" in f["params"]
        _fi.thumbnail(LILY_THUMBNAIL if is_lily else SMALL_THUMBNAIL)
        return 1 - f["y"] + _fi.height * 0.8 / GARDEN_H

    fig = go.Figure()
    fig.add_layout_image(
        source=f"data:image/png;base64,{_img_b64}",
        xref="x", yref="y",
        x=0, y=1,
        sizex=1, sizey=1,
        xanchor="left", yanchor="top",
        layer="below",
    )
    if flowers:
        fig.add_trace(go.Scatter(
            x=[f["x"] for f in flowers],
            y=[_flower_top_y(f) for f in flowers],
            mode="markers",
            marker=dict(size=45, color="rgba(0,0,0,0)"),
            hovertext=[f["name"] for f in flowers],
            hoverinfo="text",
            hoverlabel=dict(bgcolor="white", font_size=14),
            showlegend=False,
        ))
    fig.update_layout(
        xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False,
                   scaleanchor="x", scaleratio=GARDEN_H / GARDEN_W),
        margin=dict(l=0, r=0, t=0, b=0),
        height=900,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
