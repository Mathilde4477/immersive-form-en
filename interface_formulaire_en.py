import streamlit as st
from fpdf import FPDF
import pandas as pd
import os
import datetime

date_demande = st.date_input("📅 Date de la demande", value=datetime.date.today())
date_visite = st.date_input("📆 Date de la visite")

st.title("Formulaire Immersive - Version Anglaise")



# Champs d'identité
reference = st.text_input("Référence")
institution = st.text_input("Institution")
title = st.selectbox("Title", ["Mr", "Mrs", "Other"])
last_name = st.text_input("Last name")
prelast_name = st.text_input("First name")
address = st.text_input("Address")
address2 = st.text_input("Address 2")
code_postal = st.text_input("Code postal")
city = st.text_input("City")
country = st.text_input("Country")
phone = st.text_input("Phone")
email = st.text_input("Email")

last_name_clients = st.text_area("Last name des clients")

# Champs visite
tour_language = st.selectbox("Tour language", ["French", "Anglais"])
niveau_scolaire = st.text_input("Niveau scolaire")
last_namebre_personnes = st.number_input("Last namebre de personnes", min_value=1, step=1)
capacity_max = st.number_input("Capacité max", min_value=1, step=1)
programme = st.selectbox("Tour program", [
    "D-Day beaches (US sector)",
    "D-Day beaches (British sector)",
    "D-Day beaches (Canadian sector)",
    "D-Day beaches (US/GB)",
    "Mont Saint Michel",
    "Old Bayeux and Cathedral",
    "Medieval",
    "Other"
])
detail_programme = st.text_area("Champ libre programme")

# Champs horaires
start_time = st.selectbox("Heure de début", [f"{h:02d}:{m:02d}" for h in range(6, 21) for m in range(0, 60, 5)])
start_location = st.text_input("Lieu de début")
end_time = st.selectbox("Heure de fin", [f"{h:02d}:{m:02d}" for h in range(6, 22) for m in range(0, 60, 5)])
end_location = st.text_input("Lieu de fin")

# Champs tarifs
type_visite = st.radio("Guide only ou chauffeur-guide", ["Guide only", "Driver-guide"])
guide_fee = st.number_input("Guiding fee HT (€)", min_value=0.0, step=1.0, format="%.2f")
vat_guide_rate = round(guide_fee * 0.20, 2)
driver_fee = st.number_input("Driver fee HT (€)", min_value=0.0, step=1.0, format="%.2f")
vat_driver_rate = round(driver_fee * 0.10, 2)
total_price = round(guide_fee + vat_guide_rate + driver_fee + vat_driver_rate, 2)

# Duration estimée
from datetime import datetime
try:
    fmt = "%H:%M"
    debut = datetime.strptime(start_time, fmt)
    fin = datetime.strptime(end_time, fmt)
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
    "Title": title,
        "Date of request": date_request,
        "Date of visit": date_visit,
    "Last name": last_name,
    "First name": prelast_name,
    "Address": address,
    "Address 2": address2,
    "Code postal": code_postal,
    "City": city,
    "Country": country,
    "Phone": phone,
    "Email": email,
    "Tour language": tour_language,
    "Niveau scolaire": niveau_scolaire,
    "Last namebre de personnes": last_namebre_personnes,
    "Capacité max": capacity_max,
    "Tour program": programme,
    "Détail programme": detail_programme,
    "Heure de début": start_time,
    "Lieu de début": start_location,
    "Heure de fin": end_time,
    "Lieu de fin": end_location,
    "Duration": duree,
    "Type de visite": type_visite,
    "VIP": "Oui" if vip else "Non",
    "Texte VIP": texte_vip,
    "Guiding fee HT": f"{guide_fee:.2f}",
    "TVA guidage (20%)": f"{vat_guide_rate:.2f}",
    "Driver fee HT": f"{driver_fee:.2f}",
    "TVA chauffeur (10%)": f"{vat_driver_rate:.2f}",
    "Total price (incl. VAT)": f"{total_price:.2f}",
    "Last name clients": last_name_clients
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
    last_name_fichier = f"formulaire_{reference or last_name}_{institution or prelast_name}.pdf".replace(" ", "_")
    pdf.output(last_name_fichier)
    with open(last_name_fichier, "rb") as f:
        st.download_button("Télécharger le PDF", f, last_name_fichier, mime="application/pdf")
