import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Audit Villa Marrakech - Expert", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; border: 1px solid #D4AF37; 
        padding: 15px; border-radius: 10px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE - RÉGLAGES MODULABLES
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    with st.expander("🏦 Financement", expanded=False):
        type_pret = st.radio("Structure du prêt", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Capital emprunté (€)", value=470000)
        tx_annuel = st.slider("Taux d'intérêt annuel (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée du crédit (ans)", 5, 25, 15)

    with st.expander("📅 Hypothèses Airbnb", expanded=True):
        adr = st.number_input("Prix de la nuitée moyen (€)", value=430)
        occ = st.slider("Taux d'occupation estimé (%)", 0, 100, 45)

    with st.expander("💸 Charges & Fiscalité", expanded=True):
        f_fixes = st.number_input("Charges fixes mensuelles (€)", value=1650)
        com_concierge_pct = st.slider("Commission Conciergerie (%)", 0, 30, 20)
        com_airbnb_pct = st.slider("Frais Airbnb/Booking (%)", 0, 20, 3)
        statut = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# 3. MOTEUR DE CALCULS FINANCIERS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
cr = m_pret

# --- Calcul de la mensualité ---
if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        int_m = cr * tm
        princ = mens - int_m
        cr -= princ
        tableau.append([i, round(mens, 2), round(princ, 2), round(int_m, 2), round(max(0, cr), 2)])
else:
    mens = m_pret * tm
    for i in range(1, nb_m + 1):
        p_fin = m_pret if i == nb_m else 0
        tableau.append([i, round(mens + p_fin, 2), p_fin, round(mens, 2), m_pret if i < nb_m else 0])

# --- Analyse de la Rentabilité ---
rev_brut_m = adr * 30.5 * (occ / 100)
frais_concierge = rev_brut_m * (com_concierge_pct / 100)
frais_airbnb = rev_brut_m * (com_airbnb_pct / 100)

# Fiscalité selon le régime (Application de l'abattement de 40% pour PP)
if statut == "Personne Physique":
    base_fonciere = rev_brut_m * 0.60 
    impot_m = base_fonciere * 0.15 
else:
    benef_is = rev_brut_m - frais_concierge - frais_airbnb - f_fixes - mens
    impot_m = max(0, benef_is * 0.20)

profit_net = rev_brut_m - frais_concierge - frais_airbnb - f_fixes - mens - impot_m

# Ratios Experts
dscr = (rev_brut_m - frais_concierge - frais_airbnb - f_fixes) / mens if mens > 0 else 0

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Audit de Performance & Pilotage Financier")

# Bandeau de KPIs (Mise à jour du bandeau image_12a294)
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Cash-Flow Net Mensuel", f"{int(profit_net)} €")
with c2: st.metric("Mensualité Banque", f"{int(mens)} €")
with c3: st.metric("DSCR (Solvabilité)", f"{dscr:.2f}", help="Indice de sécurité (>1.20)")
with c4: st.metric("Impôt Mensuel", f"{int(impot_m)} €", delta=statut, delta_color="off")

st.markdown("---")

# Détails des Flux
col_flux1, col_flux2 = st.columns(2)
with col_flux1:
    st.subheader("📝 Analyse des Flux (Mensuel)")
    st.write(f"• Chiffre d'Affaires : **{int(rev_brut_m)} €**")
    st.write(f"• Conciergerie ({com_concierge_pct}%) : **-{int(frais_concierge)} €**")
    st.write(f"• Frais Airbnb ({com_airbnb_pct}%) : **-{int(frais_airbnb)} €**")
    st.write(f"• Charges Fixes : **-{int(f_fixes)} €**")
    st.divider()
    st.markdown(f"### Cash-Flow : **{int(profit_net)} € / mois**")

with col_flux2:
    st.subheader("🏁 Point d'Équilibre")
    seuil_ca = (f_fixes + mens) / (1 - (com_concierge_pct + com_airbnb_pct + 10)/100)
    occ_seuil = (seuil_ca / (adr * 30.5)) * 100
    st.info(f"Équilibre atteint à **{int(occ_seuil)}%** d'occupation.")
    st.write(f"Soit environ **{int(30.5 * occ_seuil / 100)} nuits** par mois.")

st.markdown("---")

# Tableau d'amortissement interactif (Mise à jour image_11db82)
st.subheader(f"📊 Tableau d'Amortissement Dynamique ({type_pret})")
df_a = pd.DataFrame(tableau, columns=["
