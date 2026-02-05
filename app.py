import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Audit Rentabilité Villa Marrakech", layout="wide")

# 2. DESIGN PERSONNALISÉ (OR ET NOIR)
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'serif'; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; border: 1px solid #D4AF37; 
        padding: 15px; border-radius: 10px; text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    .stSelectSlider [data-baseweb="slider"] { color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 Audit de Rentabilité & Pricing Dynamique")
st.markdown("---")

# --- SYSTÈME DE SÉCURITÉ ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "MARRAKECH2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Accès Propriétaire - Entrez le code :", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Code incorrect. Réessayez :", type="password", on_change=password_entered, key="password")
        st.error("🔒 Accès refusé")
        return False
    else:
        return True

if not check_password():
    st.stop()
# --- FIN SÉCURITÉ ---

# 3. BARRE LATÉRALE (CONFIGURATION)
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    with st.expander("🏦 Financement", expanded=False):
        type_pret = st.radio("Type de crédit", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000)
        tx_annuel = st.number_input("Taux annuel (%)", value=3.70)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Saisonnalité & Revenus", expanded=True):
        mois_choisi = st.select_slider(
            "Mois de l'année",
            options=["Janv", "Févr", "Mars", "Avril", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"],
            value="Avril"
        )
        
        if mois_choisi in ["Déc", "Avril", "Mai", "Oct"]:
            coeff = 1.3  
            saison_txt = "🏷️ Haute Saison (+30%)"
        elif mois_choisi in ["Juil", "Août", "Janv"]:
            coeff = 0.8  
            s
