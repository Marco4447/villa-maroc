with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🏦 Financement", expanded=False):
        # ... (Garder le code précédent pour le prêt)
    
    with st.expander("💸 Structure des Charges", expanded=True):
        # CHARGES FIXES : Montants en Euros
        f_fixes_mensuels = st.number_input("Total Charges Fixes / mois (€)", value=1650)
        
        # CHARGES VARIABLES : Pourcentage global du CA
        # Inclut Conciergerie (20%) + Frais de plateforme + Energie variable
        total_vars_pct = st.slider("Total Charges Variables (% du CA)", 10, 50, 30)
        
        statut = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# LOGIQUE DE CALCUL
rev_brut_mois = adr * 30.5 * (occ / 100)
montant_charges_vars = rev_brut_mois * (total_vars_pct / 100)

# Le profit net déduit maintenant automatiquement la part variable du CA
profit_net = rev_brut_mois - montant_charges_vars - f_fixes_mensuels - mens_banque - impot_mois
