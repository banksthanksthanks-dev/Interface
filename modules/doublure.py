import streamlit as st
from google import genai
import random

SYSTEM_PROMPT_DOUBLURE = """
Tu es l'Agent Ombre (La Doublure Stratégique) de la plateforme LES CHÊNES.
Ton rôle est d'agir comme un double virtuel du fondateur.
Tu possèdes une culture aiguisée sur la gestion du risque, la souveraineté numérique, l'autonomie et l'asymétrie.

Mission :
1. Analyser les tendances, thématiques et sujets soumis.
2. Détecter l'Information Capitale en éliminant le bruit.
3. Proposer 3 angles de contenus incisifs (YouTube / Telegram).
4. Donner 1 conseil stratégique direct et sans filtre.
"""

def get_keys():
    keys = []
    for i in range(1, 10):
        key_name = f"GEMINI_API_KEY_{i}"
        if key_name in st.secrets:
            keys.append(st.secrets[key_name])
    if not keys and "GEMINI_API_KEY" in st.secrets:
        keys.append(st.secrets["GEMINI_API_KEY"])
    return keys

def render_doublure():
    st.subheader("👤 Agent Ombre — Veille & Doublure Stratégique")
    st.caption("Alimenté par Gemini 3.7 Pro avec rotation multi-clés.")

    keys = get_keys()
    if not keys:
        st.error("⚠️ Aucune clé GEMINI_API_KEY détectée dans les Secrets.")
        return

    sujet = st.text_input("Sujet, tendance ou niche à analyser :", key="input_doublure_mod")

    if st.button("👁️ Lancer l'Analyse Stratégique", key="btn_doublure_mod"):
        if not sujet:
            st.warning("Veuillez saisir un sujet.")
            return

        with st.spinner("La Doublure analyse la thématique via Gemini 3.7 Pro..."):
            primary_key = random.choice(keys)
            try:
                client = genai.Client(api_key=primary_key)
                response = client.models.generate_content(
                    model="gemini-3.7-pro",
                    contents=f"SUJET À ANALYSER : {sujet}",
                    config={"system_instruction": SYSTEM_PROMPT_DOUBLURE}
                )
                st.markdown("### 📊 Diagnostic de la Doublure :")
                st.markdown(response.text)

            except Exception as e:
                if "429" in str(e) and len(keys) > 1:
                    st.warning("🔄 Quota atteint. Basculement sur la clé suivante...")
                    fallback_keys = [k for k in keys if k != primary_key]
                    for fb_key in fallback_keys:
                        try:
                            client_fb = genai.Client(api_key=fb_key)
                            response = client_fb.models.generate_content(
                                model="gemini-3.7-pro",
                                contents=f"SUJET À ANALYSER : {sujet}",
                                config={"system_instruction": SYSTEM_PROMPT_DOUBLURE}
                            )
                            st.markdown("### 📊 Diagnostic de la Doublure :")
                            st.markdown(response.text)
                            return
                        except Exception:
                            continue
                st.error(f"Erreur d'exécution : {str(e)}") 
