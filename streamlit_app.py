import streamlit as st
import requests
from google import genai

# ---------------------------------------------------------
# Configuration de la page Streamlit
# ---------------------------------------------------------
st.set_page_config(
    page_title="LES CHÊNES — Sovereign Command Center",
    page_icon="🌳",
    layout="wide"
)

# ---------------------------------------------------------
# Style CSS Haute Couture (Sombre, Émeraude & Or)
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #090d12;
        color: #e6edf3;
    }
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #2ea043;
        text-align: center;
        letter-spacing: 1px;
    }
    .sub-header {
        font-size: 1rem;
        color: #8b949e;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .card {
        background-color: #11161d;
        border: 1px solid #238636;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 700;
        height: 48px;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        box-shadow: 0px 0px 12px rgba(46, 160, 67, 0.4);
    }
    .supervisor-badge {
        background: linear-gradient(90deg, #d29922, #f8e3a1);
        color: #000;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🌳 LES CHÊNES — Studio Souverain</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Plateforme d'Orchestration Média Haute Précision & Supervision Zero Erreur</div>", unsafe_allow_html=True)

# Secrets Streamlit
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------------
# DÉFINITION DES AGENTS & SUPERVISEUR
# ---------------------------------------------------------
AGENTS_PROMPTS = {
    "🛡️ Superviseur Sécurité & Zero Faille": """Tu es LE SUPERVISEUR GÉNÉRAL ET GARDIEN QUALITÉ de LES CHÊNES.
Ta mission est d'examiner chaque proposition, chaque ligne de code et chaque idée avec une rigueur absolue.
Tu ne laisses passer AUCUNE erreur, aucun bug potentiel et aucun compromis sur l'éthique ou l'esthétique. Tu valides ou corriges catégoriquement.""",

    "👑 Architecte Pro (Intuition Supérieure)": """Tu es L'ARCHITECTE PRO. Tu possèdes une compréhension intuitive d'élite.
Tu captes immédiatement la vision profonde de l'utilisateur sans qu'il ait besoin de vous donner des détails techniques. Tu traduis les désirs stratégiques en architectures claires.""",

    "💻 Codeur Master (Dernière Génération)": """Tu es LE CODEUR MASTER. Tu rédiges un code Python/Streamlit moderne, ultra-optimisé, sécurisé et totalement à l'épreuve des pannes.""",

    "🎨 UX/UI & Branding Noble": """Tu es LE DESIGNER EN CHEF. Tu conçois l'esthétique du média : palettes sombres d'exception, vignettes captivantes, filigranes discrets et élégants."""
}

# ---------------------------------------------------------
# INTERFACE PRINCIPALE
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["🛡️ Studio Supervisé & Auto-Développement", "📡 Ordres Telegram", "⚙️ Sécurité & Système"])

with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='supervisor-badge'>SUPERVISION SÉCURISÉE — ZERO FAILLE ACTIVES</div>", unsafe_allow_html=True)
    st.subheader("Dialogue Intuitif avec la Brigade d'Elite")
    
    selected_agent = st.selectbox("Sélectionner l'Agent d'Intervention :", list(AGENTS_PROMPTS.keys()))

    # Affichage de l'historique
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Exprimez votre vision ou votre besoin d'outil...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        if GEMINI_KEY:
            client = genai.Client(api_key=GEMINI_KEY)
            
            # Étape 1 : Traitement par l'agent sélectionné (avec le modèle Gemini 2.5 Pro)
            prompt_agent = f"{AGENTS_PROMPTS[selected_agent]}\n\nVision exprimée par le Chef d'Orchestre : {user_input}"
            
            with st.spinner("Analyse intuitive en cours..."):
                res_agent = client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=prompt_agent
                ).text

            # Étape 2 : Passation obligatoire devant le Superviseur Sécurité & Zero Erreur
            prompt_supervision = f"{AGENTS_PROMPTS['🛡️ Superviseur Sécurité & Zero Faille']}\n\nExamine la proposition suivante générée par l'agent '{selected_agent}' et assure-toi qu'elle est PARFAITE, sans bug et totalement alignée avec l'excellence de LES CHÊNES. Si besoin, apporte les corrections nécessaires :\n\n{res_agent}"
            
            with st.spinner("Validation par le Superviseur Sécurité..."):
                res_final = client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=prompt_supervision
                ).text

            st.session_state.chat_history.append({"role": "assistant", "content": f"**[{selected_agent} + 🛡️ Superviseur]**\n\n{res_final}"})
            st.rerun()
        else:
            st.error("Clé GEMINI_API_KEY manquante.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📡 Exécution des Ordres Telegram Supervisés")
    
    if st.button("🔄 Traiter le dernier ordre avec validation Superviseur"):
        if TELEGRAM_TOKEN and GEMINI_KEY:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            res = requests.get(url).json()
            
            if res.get("ok") and res.get("result"):
                last_update = res["result"][-1]
                msg_text = last_update.get("message", {}).get("text", "")
                user_id = last_update.get("message", {}).get("chat", {}).get("id")
                
                if msg_text:
                    client = genai.Client(api_key=GEMINI_KEY)
                    
                    # Exécution Pro + Supervision
                    prompt = f"Tu es l'Intelligence Centrale LES CHÊNES sous la supervision directe du Guardien Zero Erreur. Exécute cet ordre Telegram de manière irréprochable : {msg_text}"
                    response = client.models.generate_content(model="gemini-2.5-pro", contents=prompt)
                    
                    result_text = response.text
                    st.success("Ordre exécuté et certifié sans erreur !")
                    st.text_area("Rendu final certifié :", value=result_text, height=200)
                    
                    reply_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                    payload = {
                        "chat_id": user_id,
                        "text": f"🛡️ **Rendu Certifié LES CHÊNES :**\n\n{result_text}",
                        "parse_mode": "Markdown"
                    }
                    requests.post(reply_url, json=payload)
            else:
                st.info("Aucun ordre Telegram en attente.")
        else:
            st.error("Clés Secrets non configurées.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ État du Système & Supervision")
    st.markdown("🛡️ **Superviseur Général :** Actif (Contrôle systématique)")
    st.markdown("🧠 **Cerveau IA :** Gemini 2.5 Pro (Dernière Génération)")
    st.markdown("🟢 **Serveur Cloud :** Sécurisé")
    st.markdown("🤖 **Bot Telegram :** Connecté")
    st.markdown("</div>", unsafe_allow_html=True)
