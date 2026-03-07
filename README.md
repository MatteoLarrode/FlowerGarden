# FlowerGarden

A shared virtual garden for International Women's Day. Each recipient generates a personalized dahlia flower and plants it in a garden shared with everyone else.

## How it works

1. **Generate** — adjust sliders to design your flower (shape, petal density, colors)
2. **Plant** — click a spot in the shared garden to place it
3. **Browse** — visit the garden to see everyone's flowers

## Running locally

```bash
# Set up environment (first time only)
python3 -m venv ~/.venvs/flowergarden
source ~/.venvs/flowergarden/bin/activate
pip install -e .

# Add Supabase credentials
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# → fill in SUPABASE_URL and SUPABASE_KEY

# Run
source ~/.venvs/flowergarden/bin/activate
streamlit run Home.py
```

## Project structure

```
Home.py              # Landing page (Streamlit entry point)
pages/
  1_My_Flower.py     # Flower generation UI
  2_Garden.py        # Shared garden — view and plant
flower.py            # Dahlia generation (DahliaParams + generate_flower)
garden/
  storage.py         # Supabase read/write
  render.py          # PIL garden compositing
dev/
  tune.py            # Local matplotlib tuner (dev only)
  generate.py        # CLI flower generator (dev only)
```

## Supabase schema

```sql
create table planted_flowers (
  id         uuid primary key default gen_random_uuid(),
  name       text not null,
  x          float not null,
  y          float not null,
  params     jsonb not null,
  image_b64  text not null,
  planted_at timestamptz default now()
);
```
