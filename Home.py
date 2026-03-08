import streamlit as st

st.set_page_config(page_title="Flower Garden", layout="centered")

lang = st.toggle("🇫🇷 Français", value=False)

if not lang:
    st.title("Happy International Women's Day 2026!")
    st.markdown("""
#### And welcome to your flower garden 🌸

On this beautiful day meant to celebrate the global social, economic, cultural, and political achievements of women, I wanted to give a more local shoutout to the women in my life! 🩵

You are all making huge differences in the world, in many different ways: some have chosen to climb the corporate ladder and improve the status quo in male dominated fields, some are buried in research papers to uncover the secrets of the world, others are doing incredible work with NGOs, or even healing people and DELIVERING BABIES (are you kidding me this is crazy).

Whether you recognised yourself in this text or not, I want to thank you for being yourself and for having accepted me in your life, as a friend, girlfriend, family, or as a son. Each in your own ways, you embellish my life with your advice, humour, strength, honesty and love. I am truly admirative of every single one of you.

This little project is my way to thank and celebrate you. I hope to see this garden blossom with your flowers, in the same way that my life is flourishing with you in it ❤️

---

**How it works:**

1. Go to **My Flower:** add your first name, adjust the sliders to design your flower, then generate it.
2. Head to **Garden:** click a spot in the garden to plant it.
3. Hover over any flower to see who planted it.

Use the sidebar to navigate between pages.
""")
else:
    st.title("Joyeuse Journée Internationale des Femmes 2026 !")
    st.markdown("""
#### Et bienvenue dans ton jardin fleuri 🌸

En cette belle journée célébrant les accomplissements sociaux, économiques, culturels et politiques des femmes à travers le monde, je veux rendre un hommage un petit peu plus local aux femmes de ma vie ! 🩵

Vous faites toutes des différences immenses dans le monde, chacune à votre façon : certaines ont choisi de gravir le corporate ladder et de changer les choses dans des domaines dominés par les hommes, d'autres sont plongées dans de la recherche pour percer les secrets du monde, certaines font un taff incroyable dans des ONG, ou même soignent des gens et METTENT DES BÉBÉS AU MONDE (non mais c'est une dinguerie sérieux?).

Que vous vous soyez reconnues dans ce texte ou non, je veux vous remercier d'être vous-mêmes et de m'avoir accepté dans votre vie, en tant qu'ami, copain, famille, ou fils. Chacune à votre manière, vous embellissez ma vie par vos conseils, votre humour, votre force, votre honnêteté et votre amour. Je suis tellement admiratif de chacune d'entre vous.

Ce petit projet est ma façon de vous remercier et de vous célébrer. J'espère voir ce jardin s'épanouir avec vos fleurs, de la même façon que ma vie s'épanouit avec vous ❤️

---

**Comment ça marche :**

1. Va dans **My Flower :** ajoute ton prénom, ajuste les curseurs pour créer ta fleur, puis génère-la.
2. Rends-toi dans **Garden :** clique sur un endroit dans le jardin pour la planter.
3. Passe la souris sur une fleur pour voir qui l'a plantée.

Utilise la barre latérale pour naviguer entre les pages.
""")
