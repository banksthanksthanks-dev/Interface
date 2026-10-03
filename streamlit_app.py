import streamlit as st
import requests

# Configuration de la page
st.set_page_config(
    page_title="LES CHÊNES — Command Center",
    page_icon="🌳",
    layout="wide"
)

# Injection de style CSS personnalisé (Thème sombre teinté & habillage haut de gamme)
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2ea043;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #8b949e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête principal
st.markdown("<div class='main-header'>🌳 LES CHÊNES — Centre de Contrôle</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Plateforme Souveraine d'Orchestration Média Automation</div>", unsafe_allow_html=True)

# Récupération des secrets
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID")

# Interface du tableau de bord
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📡 Commandes & Derniers Ordres")
    
    if st.button("🔄 Relever les commandes Telegram"):
        if TELEGRAM_TOKEN:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            res = requests.get(url).json()
            if res.get("ok") and res.get("result"):
                last_update = res["result"][-1]
                msg_text = last_update.get("message", {}).get("text", "Commande inconnue")
                user_id = last_update.get("message", {}).get("chat", {}).get("id")
                
                st.success(f"Dernier ordre reçu : {msg_text}")
                
                # Envoi de la réponse avec des boutons interactifs sur Telegram
                reply_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                payload = {
                    "chat_id": user_id,
                    "text": f"⚙️ Ordre '{msg_text}' reçu avec succès.\nSélectionnez l'action à exécuter :",
                    "reply_markup": {
                        "inline_keyboard": [
                            [{"text": "🎬 Générer Script IA", "callback_data": "gen_script"},
                             {"text": "🖼️ Créer Miniature", "callback_data": "gen_thumb"}],
                            [{"text": "💧 Filigrane & Branding", "callback_data": "watermark"},
                             {"text": "🎙️ Synthèse Vocale", "callback_data": "audio"}],
                            [{"text": "🚀 Publier sur le Canal", "callback_data": "publish"}]
                        ]
                    }
                }
                requests.post(reply_url, json=payload)
            else:
                st.info("Aucune nouvelle commande en attente.")
        else:
            st.error("Token Telegram manquant dans les Secrets.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ État du Système")
    st.markdown("🟢 **Serveur Cloud :** Actif")
    st.markdown("🤖 **Bot Commandes :** Connecté")
    st.markdown("📢 **Canal Cible :** Configuré")
    st.markdown("</div>", unsafe_allow_html=True)
