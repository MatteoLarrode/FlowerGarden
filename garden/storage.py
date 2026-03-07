from dataclasses import asdict

import streamlit as st
from supabase import create_client

from flower import DahliaParams


@st.cache_resource
def _client():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


def get_all_flowers() -> list[dict]:
    return _client().table("planted_flowers").select("*").order("planted_at").execute().data


def plant_flower(name: str, x: float, y: float, params: DahliaParams, image_b64: str) -> None:
    _client().table("planted_flowers").insert({
        "name": name,
        "x": x,
        "y": y,
        "params": asdict(params),
        "image_b64": image_b64,
    }).execute()
