from flower import DahliaParams, generate_flower

params = DahliaParams(
    petals_per_revolution=12.6,
    total_petals=140,
    petal_tilt=-1.2,
    openness=(0.11, 1.1),
    color_inner=(0.6, 0.1, 0.7),
    color_outer=(1.0, 0.8, 1.0),
)

fig = generate_flower(params)
fig.savefig("output.png", dpi=150, bbox_inches="tight")
print("Saved output.png")
