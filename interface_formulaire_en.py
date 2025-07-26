
import streamlit as st
from fpdf import FPDF
import pandas as pd
import os

st.title("Formulaire Immersive - Version Complète")

# Champs d'identité
reference = st.text_input("Référence")
institution = st.text_input("Institution")
titre = st.selectbox("Title", ["M.", "Mme", "Mlle"])
nom = st.text_input("Last name")
prenom = st.text_input("First name")
adresse = st.text_input("Address")
adresse2 = st.text_input("Address 2")
code_postal = st.text_input("Code postal")
commune = st.text_input("City")
pays = st.text_input("Country")
telephone = st.text_input("Phone")
email = st.text_input("Email")

nom_clients = st.text_area("Last name des clients")

# Champs visite
langue = st.selectbox("Tour language", ["French", "Anglais"])
niveau_scolaire = st.text_input("Niveau scolaire")
nombre_personnes = st.number_input("Last namebre de personnes", min_value=1, step=1)
capacite_max = st.number_input("Capacité max", min_value=1, step=1)
programme = st.selectbox("Tour program", [
    "Plages du Débarquement (secteur US)", 
    "Plages du Débarquement (secteur GB)",
    "Plages du Débarquement (secteur Canadien)",
    "Plages du Débarquement (US/GB)", 
    "Mont Saint Michel",
    "Old Bayeux and Cathedral",
    "Medieval",
    "Other"
])
detail_programme = st.text_area("Champ libre programme")

# Champs horaires
heure_debut = st.selectbox("Heure de début", [f"{h:02d}:{m:02d}" for h in range(6, 21) for m in range(0, 60, 5)])
lieu_debut = st.text_input("Lieu de début")
heure_fin = st.selectbox("Heure de fin", [f"{h:02d}:{m:02d}" for h in range(6, 22) for m in range(0, 60, 5)])
lieu_fin = st.text_input("Lieu de fin")

# Champs tarifs
type_visite = st.radio("Guide only ou chauffeur-guide", ["Guide only", "Driver-guide"])
tarif_guidage = st.number_input("Guiding fee HT (€)", min_value=0.0, step=1.0, format="%.2f")
tva_guidage = round(tarif_guidage * 0.20, 2)
tarif_chauffeur = st.number_input("Driver fee HT (€)", min_value=0.0, step=1.0, format="%.2f")
tva_chauffeur = round(tarif_chauffeur * 0.10, 2)
tarif_ttc = round(tarif_guidage + tva_guidage + tarif_chauffeur + tva_chauffeur, 2)

# Duration estimée
from datetime import datetime
try:
    fmt = "%H:%M"
    debut = datetime.strptime(heure_debut, fmt)
    fin = datetime.strptime(heure_fin, fmt)
    duree = str(fin - debut)
except:
    duree = ""

# VIP
vip = st.checkbox("Visite VIP ?")
texte_vip = st.text_area("Informations supplémentaires en cas de VIP") if vip else ""

# Données
ligne = {
    "Référence": reference,
    "Institution": institution,
    "Title": titre,
    "Last name": nom,
    "First name": prenom,
    "Address": adresse,
    "Address 2": adresse2,
    "Code postal": code_postal,
    "City": commune,
    "Country": pays,
    "Phone": telephone,
    "Email": email,
    "Tour language": langue,
    "Niveau scolaire": niveau_scolaire,
    "Last namebre de personnes": nombre_personnes,
    "Capacité max": capacite_max,
    "Tour program": programme,
    "Détail programme": detail_programme,
    "Heure de début": heure_debut,
    "Lieu de début": lieu_debut,
    "Heure de fin": heure_fin,
    "Lieu de fin": lieu_fin,
    "Duration": duree,
    "Type de visite": type_visite,
    "VIP": "Oui" if vip else "Non",
    "Texte VIP": texte_vip,
    "Guiding fee HT": f"{tarif_guidage:.2f}",
    "TVA guidage (20%)": f"{tva_guidage:.2f}",
    "Driver fee HT": f"{tarif_chauffeur:.2f}",
    "TVA chauffeur (10%)": f"{tva_chauffeur:.2f}",
    "Total price (incl. VAT)": f"{tarif_ttc:.2f}",
    "Last name clients": nom_clients
}

# Export Excel
if st.button("Exporter vers Excel"):
    df = pd.DataFrame([ligne])
    fichier_excel = "formulaire_complet.xlsx"
    df.to_excel(fichier_excel, index=False)
    with open(fichier_excel, "rb") as f:
        st.download_button("Télécharger le fichier Excel", f, fichier_excel)

# Export PDF
if st.button("Générer le PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Formulaire Immersive - Données complètes")
    for key, value in ligne.items():
        pdf.multi_cell(0, 10, txt=f"{key} : {value}")
    nom_fichier = f"formulaire_{reference or nom}_{institution or prenom}.pdf".replace(" ", "_")
    pdf.output(nom_fichier)
    with open(nom_fichier, "rb") as f:
        st.download_button("Télécharger le PDF", f, nom_fichier, mime="application/pdf")
