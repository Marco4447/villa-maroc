import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Patrimoine Valentin - Villa n°31",
    page_icon="🏰",
    layout="wide"
)

# 2. DESIGN PERSONNALISÉ (CSS)
st.markdown("""
    <style>
    /* Fond sombre anthracite */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    /* Titres en Or */
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Playfair Display', serif;
    }
    /* Cartes de résultats */
    div[data-testid="stMetric"] {
        background-color: #1E1E1E;
        border: 1px solid #D4AF37;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    /* Couleur des chiffres metrics */
    div[data-testid="stMetricValue"] > div {
        color: #D4AF37 !important;
    }
    /* Sidebar style */
    .css-1d391kg {
        background-color: #161B22;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ENTÊTE
st.title("🏰 Villa n°31 - The Valley Marrakech")
st.subheader("Ingénierie Patrimoniale & Simulation de Performance")
st.markdown("---")

# 4. BARRE LATÉRALE (INPUTS)
with st.sidebar:
    st.image("https://img.freepik.com/vecteurs-premium/logo-immobilier-luxe-maison-or_23-2148463214.jpg", width=100)
    st.header("⚙️ Configuration")
    
    with st.expander("💳 Financement In Fine", expanded=True):
        prix_total = st.slider("Investissement Global (€)", 500000, 1500000, 670000, step=10000)
        apport = st.slider("Apport Personnel (€)", 0, 1000000, 200000, step=10000)
        taux_interet = st.number_input("Taux Crédit (%)", value=3.70, step=0.05)
    
    with st.expander("📅 Exploitation OpCo", expanded=True):
        adr = st.slider("Prix Nuitée (ADR €)", 300, 1500, 435, step=25)
        to = st.slider("Occupation Annuelle (%)", 0, 100, 45, step=1)

# 5. LOGIQUE DE CALCUL (Source : Rapport Pierre Valentin)
nb_nuits = 365 * (to / 100)
revenus_annuels = nb_nuits * adr

# Charges OpCo & Personnel
commissions = revenus_annuels * 0.25 # Conciergerie 20% + Plateformes 3% + Maint 2% [cite: 313]
frais_menage = nb_nuits * 35 # 35€ par nuit louée [cite: 313]
charges_fixes = 14000 # Syndic, Jardin, Assurance [cite: 313, 317]

montant_pret = prix_total - apport # [cite: 131, 339]
interets_annuels = montant_pret * (taux_interet / 100) # [cite: 204, 927]

# Performance Finale
profit_global_annuel = revenus_annuels - commissions - frais_menage - charges_fixes - interets_annuels
profit_global_mensuel = profit_global_annuel / 12

# 6. AFFICHAGE DU TABLEAU DE BORD
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Chiffre d'Affaires", f"{revenus_annuels:,.0f} €".replace(",", " "))

with col2:
    st.metric("Profit Net / Mois", f"{profit_global_mensuel:,.0f} €".replace(",", " "), delta=f"TO {to}%")

with col3:
    renta_apport = (profit_global_annuel / apport * 100) if apport > 0 else 0
    st.metric("Rendement / Apport", f"{renta_apport:.1f} %")

st.markdown("---")

# 7. ANALYSE ET SÉCURITÉ
c1, c2 = st.columns([2, 1])

with c1:
    st.write("### 💎 Analyse du Montage")
    st.write(f"""
    Le projet repose sur un **crédit In Fine de {montant_pret:,.0f} €**[cite: 131, 339]. 
    Le service de la dette s'élève à **{interets_annuels/12:,.0f} € / mois**[cite: 928, 929].
    """)
    
    # Point d'équilibre
    marge_nuit = adr * 0.75 - 35
    seuil_to = ((charges_fixes + interets_annuels) / marge_nuit / 365 * 100) if marge_nuit > 0 else 0
    
    if to >= seuil_to:
        st.success(f"✅ Seuil d'équilibre atteint à **{seuil_to:.1f}%** d'occupation.")
    else:
        st.error(f"⚠️ Seuil d'équilibre non atteint (Requis : {seuil_to:.1f}%)")

with c2:
    st.write("### 🛡️ Protection")
    st.info(f"**Liquidités :** 80 000 €[cite: 80, 911].")
    st.caption("Cette réserve couvre 4,6 ans de service de dette sans aucun loyer[cite: 220, 324].")
    st.write("**Bénéficiaires :**")
    st.caption("Paul (Nue-propriété)[cite: 48, 60, 295, 338, 1184].")
    st.caption("Emmanuelle (Réversion)[cite: 1185, 1186].")
