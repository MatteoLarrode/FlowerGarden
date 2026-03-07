import base64
import io

import streamlit as st

from flower import DahliaParams, generate_flower

st.set_page_config(page_title="My Flower", layout="wide")
st.title("Generate your flower")

with st.sidebar:
    st.header("Shape")
    ppr    = st.slider("Petals per revolution", 5.0,  20.0, 12.6)
    pn     = st.slider("Total petals",          50,   250,  140,  step=10)
    pf     = st.slider("Petal tilt",           -2.5,  0.0, -1.2)
    ol_in  = st.slider("Openness inner",        0.01, 0.5,  0.11)
    ol_out = st.slider("Openness outer",        0.5,  2.5,  1.1)

    st.header("Inner color (RGB)")
    ci_r = st.slider("Red",   0.0, 1.0, 0.6, key="ci_r")
    ci_g = st.slider("Green", 0.0, 1.0, 0.1, key="ci_g")
    ci_b = st.slider("Blue",  0.0, 1.0, 0.7, key="ci_b")

    st.header("Outer color (RGB)")
    co_r = st.slider("Red",   0.0, 1.0, 1.0, key="co_r")
    co_g = st.slider("Green", 0.0, 1.0, 0.8, key="co_g")
    co_b = st.slider("Blue",  0.0, 1.0, 1.0, key="co_b")

    name = st.text_input("Your name", placeholder="e.g. Marie")
    clicked = st.button("Generate", type="primary", use_container_width=True)

if clicked:
    params = DahliaParams(
        petals_per_revolution=ppr,
        total_petals=pn,
        petal_tilt=pf,
        openness=(ol_in, ol_out),
        color_inner=(ci_r, ci_g, ci_b),
        color_outer=(co_r, co_g, co_b),
    )
    fig = generate_flower(params)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", transparent=True)
    image_bytes = buf.getvalue()

    # Store in session state so the Garden page can use it
    st.session_state["flower_params"] = params
    st.session_state["flower_b64"] = base64.b64encode(image_bytes).decode()
    st.session_state["flower_name"] = name or "Anonymous"

    st.pyplot(fig)
    st.download_button("Download PNG", image_bytes, "my_flower.png", "image/png")

    if name:
        st.success("Head to the Garden page to plant your flower!")
    else:
        st.info("Enter your name above to be able to plant it in the garden.")
