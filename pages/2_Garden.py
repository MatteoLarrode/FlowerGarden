import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

from garden.storage import get_all_flowers, plant_flower
from garden.render import composite_garden

GARDEN_W = 900
GARDEN_H = 600

st.set_page_config(page_title="The Garden", layout="wide")
st.title("The Garden")

# ── Load flowers ──────────────────────────────────────────────────────────────

try:
    flowers = get_all_flowers()
except Exception as e:
    st.error(f"Could not connect to the garden database: {e}")
    st.info("Make sure your Supabase credentials are set in `.streamlit/secrets.toml`.")
    st.stop()

col_refresh, _ = st.columns([1, 5])
with col_refresh:
    if st.button("Refresh"):
        st.rerun()

# ── Garden image ──────────────────────────────────────────────────────────────

garden_img = composite_garden(flowers, GARDEN_W, GARDEN_H)

has_flower = "flower_b64" in st.session_state
planting_mode = has_flower and st.session_state.get("flower_name", "")

if planting_mode and "pending_plant" not in st.session_state:
    st.info(
        f"Hi **{st.session_state['flower_name']}**! "
        "Click anywhere in the garden to choose where to plant your flower."
    )

# streamlit_image_coordinates returns {x, y} pixel coords on click, else None
coords = streamlit_image_coordinates(garden_img, key="garden_click")

if coords and planting_mode and "pending_plant" not in st.session_state:
    x = coords["x"] / GARDEN_W
    y = coords["y"] / GARDEN_H
    st.session_state["pending_plant"] = (x, y)
    st.rerun()

# ── Confirm planting ──────────────────────────────────────────────────────────

if "pending_plant" in st.session_state:
    x, y = st.session_state["pending_plant"]
    st.markdown(f"**Plant your flower here?** (position {x:.2f}, {y:.2f})")
    col_yes, col_no, _ = st.columns([1, 1, 4])
    with col_yes:
        if st.button("Plant it!", type="primary"):
            plant_flower(
                name=st.session_state["flower_name"],
                x=x,
                y=y,
                params=st.session_state["flower_params"],
                image_b64=st.session_state["flower_b64"],
            )
            del st.session_state["pending_plant"]
            del st.session_state["flower_b64"]
            st.success("Your flower has been planted!")
            st.rerun()
    with col_no:
        if st.button("Cancel"):
            del st.session_state["pending_plant"]
            st.rerun()

# ── Flower list (replaces hover) ──────────────────────────────────────────────

if flowers:
    st.markdown("---")
    st.markdown("**Flowers planted so far:**")
    st.markdown("  ".join(f"🌸 {f['name']}" for f in flowers))

# ── Prompt if no flower yet ───────────────────────────────────────────────────

if not has_flower:
    st.markdown("---")
    st.info("Generate your flower on the **My Flower** page first, then come back here to plant it.")
