import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Audit Patrimonial - Villa Marrakech", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'serif'; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; border: 1px solid #D4AF37; 
        padding: 15px; border-radius: 10px; text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE - CONFIGURATION PERSONNALISABLE
with st.sidebar:
    st.header("⚙️ Paramètres d'Audit")
    
    with st.expander("🏦 Financement (Prêt)", expanded=False):
        type_pret = st.radio("Type de prêt", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Capital emprunté (€)", value=470000)
        tx_annuel = st.slider("Taux d'intérêt global (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée du crédit (ans)", 5, 25, 15)

    with st.expander("📅 Revenus Locatifs (Airbnb)", expanded=True):
        adr = st.number_input("Prix de la nuitée moyen (€)", value=435)
        occ = st.slider("Taux d'occupation estimé (%)", 0, 100, 45)

    with st.expander("💸 Charges & Fiscalité", expanded=True):
        f_fixes_detention = st.number_input("Charges fixes / mois (€)", value=1650, help="Assurance, entretien, taxes locales")
        com_concierge_pct = st.slider("Commission Conciergerie (%)", 0, 30, 20)
        com_airbnb_pct = st.slider("Frais Plateforme Airbnb/Booking (%)", 0, 20, 3)
        statut = st.selectbox("Régime Fiscal Maroc", ["Personne Physique", "Personne Morale (IS)"])

# 3. MOTEUR DE CALCULS FINANCIERS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
cr = m_pret

# --- Calcul du Crédit ---
if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        int_m = cr * tm
        princ = mens - int_m
        cr -= princ
        tableau.append([i, round(mens, 2), round(princ, 2), round(int_m, 2), round(max(0, cr), 2)])
else:
    # Logic In Fine : Intérêts seuls pendant la durée, capital au dernier mois
    mens = m_pret * tm
    for i in range(1, nb_m + 1):
        princ_m = 0 if i < nb_m else m_pret
        echeance_m = mens if i < nb_m else mens + m_pret
        restant_m = m_pret if i < nb_m else 0
        tableau.append([i, round(echeance_m, 2), round(princ_m, 2), round(mens, 2), round(restant_m, 2)])

# --- Calcul de la Rentabilité ---
rev_brut_m = adr * 30.5 * (occ / 100)
frais_concierge = rev_brut_m * (com_concierge_pct / 100)
frais_airbnb = rev_brut_m * (com_airbnb_pct / 100)
total_charges_vars = frais_concierge + frais_airbnb

# --- Logique Fiscale ---
if statut == "Personne Physique":
    # Application de l'abattement de 40% sur le revenu foncier brut
    base_taxable = rev_brut_m * 0.60 
    impot_m = base_taxable * 0.15 # Taux de 15% pour revenus fonciers significatifs
else:
    # Personne Morale : déduction des charges réelles et intérêts
    benefice_avant_is = rev_brut_m - total_charges_vars - f_fixes_detention - mens
    impot_m = max(0, benefice_avant_is * 0.20) # Taux IS cible 20%

profit_net_m = rev_brut_m - total_charges_vars - f_fixes_detention - mens - impot_m

# --- Ratios Experts ---
dscr = (rev_brut_m - total_charges_vars - f_fixes_detention) / mens if mens > 0 else 0
roi_annuel = ((profit_net_m * 12) / m_pret) * 100 if m_pret > 0 else 0

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Tableau de Bord d'Audit Immobilier")

# Bande
