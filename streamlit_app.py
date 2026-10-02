import streamlit as st
import requests

st.set_page_config(page_title="LES CHÊNES - Command Center", page_icon="🌳", layout="wide")

st.title("🌳 LES CHÊNES — Centre d'Orchestration")
st.caption("Module Webhook & Automatisation Telegram")

# Récupération sécurisée des clés via Streamlit Secrets
bot_token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")

st.sidebar.header("Configuration Webhook")

if bot_token:
    # URL de l'API Telegram pour la gestion des messages
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}"

    st.subheader("📥 Réception & Traitement des Dernières Commandes")
    
    if st.button("🔄 Relever les commandes Telegram"):
        # Récupération des derniers messages reçus par le bot
        updates_url = f"{telegram_api_url}/getUpdates"
        res = requests.get(updates_url).json()
        
        if res.get("ok") and res.get("result"):
            last_update = res["result"][-1]
            message_info = last_update.get("message", {})
            user_text = message_info.get("text", "")
            sender_id = message_info.get("chat", {}).get("id", "")
            
            st.info(f"📩 Dernier ordre reçu sur Telegram : **{user_text}**")
            
            # Exemple de réponse automatique
            reply_text = f"⚙️ Ordre '***{user_text}***' reçu par le serveur Cloud LES CHÊNES. Traitement en cours..."
            send_url = f"{telegram_api_url}/sendMessage"
            payload = {"chat_id": sender_id, "text": reply_text, "parse_mode": "Markdown"}
            
            requests.post(send_url, json=payload)
            st.success("✅ Réponse de confirmation renvoyée à l'utilisateur sur Telegram !")
        else:
            st.write("Aucune nouvelle commande en attente.")

else:
    st.error("Token Bot Telegram non configuré dans les Secrets.")
