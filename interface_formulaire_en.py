import streamlit as st
from fpdf import FPDF
import pandas as pd
import os
import datetime

# Date fields

def format_date_en(date):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    weekday = weekdays[date.weekday()]
    return f"{weekday} {date.day} {months[date.month - 1]} {date.year}"
date_request = st.date_input("Date of request", value=datetime.date.today())
date_visit = st.date_input("Date of visit")

st.title("Immersive Form – English version")

# Identity fields
reference = st.text_input("Reference")
institution = st.text_input("Institution")
title = st.selectbox("Title", ["Mr", "Mrs", "Miss"])
last_name = st.text_input("Last name")
first_name = st.text_input("First name")
address = st.text_input("Address")
address2 = st.text_input("Address 2")
postal_code = st.text_input("Postal code")
city = st.text_input("City")
country = st.text_input("Country")
phone = st.text_input("Phone")
email = st.text_input("Email")
client_names = st.text_area("Client names")

# Visit fields
language = st.selectbox("Language", ["French", "English"])
school_level = st.text_input("School level")
num_people = st.number_input("Number of participants", min_value=1, step=1)
max_capacity = st.number_input("Max capacity", min_value=1, step=1)
programme = st.selectbox("Programme", [
    "D-Day beaches (US sector)",
    "D-Day beaches (British sector)",
    "D-Day beaches (Canadian sector)",
    "D-Day beaches (US/GB sectors)",
    "Mont Saint Michel",
    "Old Bayeux and Cathedral",
    "Medieval",
    "Other"
])
programme_detail = st.text_area("Programme details")

# Time fields
start_time = st.selectbox("Start time", [f"{h:02d}:{m:02d}" for h in range(6, 21) for m in range(0, 60, 5)])
start_location = st.text_input("Start location")
end_time = st.selectbox("End time", [f"{h:02d}:{m:02d}" for h in range(6, 22) for m in range(0, 60, 5)])
end_location = st.text_input("End location")

# Duration
from datetime import datetime
try:
    fmt = "%H:%M"
    start = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)
    duration = str(end - start)
except:
    duration = ""

# Pricing
visit_type = st.radio("Guide only or driver-guide", ["Guide only", "Driver-guide"])
guide_fee = st.number_input("Guide fee excl. VAT (€)", min_value=0.0, step=1.0, format="%.2f")
guide_vat = round(guide_fee * 0.20, 2)
driver_fee = st.number_input("Driver fee excl. VAT (€)", min_value=0.0, step=1.0, format="%.2f")
driver_vat = round(driver_fee * 0.10, 2)
total_price = round(guide_fee + guide_vat + driver_fee + driver_vat, 2)

# VIP
vip = st.checkbox("VIP visit?")
vip_text = st.text_area("Additional information for VIP") if vip else ""

# Data dictionary
row = {
    "Reference": reference,
    "Institution": institution,
    "Title": title,
    "Date of request": format_date_en(date_request),
    "Date of visit": format_date_en(date_visit),
    "Last name": last_name,
    "First name": first_name,
    "Address": address,
    "Address 2": address2,
    "Postal code": postal_code,
    "City": city,
    "Country": country,
    "Phone": phone,
    "Email": email,
    "Client names": client_names,
    "Language": language,
    "School level": school_level,
    "Number of participants": num_people,
    "Max capacity": max_capacity,
    "Programme": programme,
    "Programme details": programme_detail,
    "Start time": start_time,
    "Start location": start_location,
    "End time": end_time,
    "End location": end_location,
    "Duration": duration,
    "Visit type": visit_type,
    "VIP": "Yes" if vip else "No",
    "VIP notes": vip_text,
    "Guide fee excl. VAT": f"{guide_fee:.2f}",
    "Guide VAT (20%)": f"{guide_vat:.2f}",
    "Driver fee excl. VAT": f"{driver_fee:.2f}",
    "Driver VAT (10%)": f"{driver_vat:.2f}",
    "Total incl. VAT": f"{total_price:.2f}"
}
ligne = {
    "Reference": reference,
    "Institution": institution,
    "Title": title,
    "Date of request": date_request.strftime("%A %d %B %Y"),
    "Date of visit": date_visit.strftime("%A %d %B %Y"),
    "Last name": last_name,
    "First name": first_name,
    "Address": address,
    "Address 2": address2,
    "Postal Code": postal_code,
    "City": city,
    "Country": country,
    "Phone": phone,
    "Email": email,
    "Client names": client_names,
    "Language": language,
    "School level": school_level,
    "Number of people": num_people,
    "Maximum capacity": max_capacity,
    "Programme": programme,
    "Programme details": programme_detail,
    "Start time": start_time,
    "Start location": start_location,
    "End time": end_time,
    "End location": end_location,
    "Duration": duration,
    "Visit type": visit_type,
    "VIP": "Yes" if vip else "No",
    "VIP notes": vip_text,
    "Guide fee (excl. tax)": f"{guide_fee:.2f}",
    "Guide VAT (20%)": f"{guide_vat:.2f}",
    "Driver fee (excl. tax)": f"{driver_fee:.2f}",
    "Driver VAT (10%)": f"{driver_vat:.2f}",
    "Total incl. VAT": f"{total_price:.2f}"
}

# Export Excel
if st.button("Export to Excel"):
    df = pd.DataFrame([row])
    df = df[['Date of request', 'Reference', 'Date of visit', 'Institution', 'Title', 'Last name', 'First name', 'Address', 'Address 2', 'Postal code', 'City', 'Country', 'Phone', 'Email', 'Client names', 'Language', 'School level', 'Number of participants', 'Max capacity', 'Programme', 'Programme details', 'Start time', 'Start location', 'End time', 'End location', 'Duration', 'Guide fee excl. VAT', 'Guide VAT (20%)', 'Driver fee excl. VAT', 'Driver VAT (10%)', 'Total incl. VAT', 'VIP', 'VIP notes']]
    excel_file = "immersive_form_en.xlsx"
    df.to_excel(excel_file, index=False)
    with open(excel_file, "rb") as f:
        st.download_button("Download Excel file", f, excel_file)

# Fonction utilitaire pour les titres de section
def section_title(pdf, title):
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Times", 'B', 14)
    pdf.cell(0, 10, title, ln=True, fill=True)
    pdf.ln(2)

# Fonction utilitaire pour ajouter un champ proprement
def add_field(pdf, label, value):
    try:
        value_str = str(value).encode('latin-1', 'replace').decode('latin-1')
    except:
        value_str = "[Invalid character]"

    # Découpe automatique si chaîne trop longue sans espace
    if len(value_str) > 100 and " " not in value_str:
        value_str = " ".join([value_str[i:i+40] for i in range(0, len(value_str), 40)])

    pdf.set_font("Times", style='B', size=12)
    pdf.multi_cell(180, 7, f"{label} :", border=0)

    pdf.set_font("Times", style='', size=12)
    pdf.multi_cell(180, 7, value_str, border=0)
    pdf.ln(2)

# ===== GÉNÉRATION PDF =====
if st.button("Generate PDF"):
    pdf = FPDF()
    pdf.set_margins(15, 20)
    pdf.add_page()

    # Logo centré
    pdf.image("logo.png", x=(210 - 30) / 2, y=8, w=30)
    pdf.ln(30)

    pdf.set_font("Times", 'B', 16)
    pdf.cell(0, 10, "Immersive Form - English Version", ln=True, align="C")
    pdf.ln(10)

    # Bloc : Personal Information
    section_title(pdf, "Personal Information")
    for field in ["Reference", "Institution", "Title", "Date of request", "Date of visit", "Last name", "First name", "Address", "Address 2", "Postal Code", "City", "Country", "Phone", "Email", "Client names"]:
        add_field(pdf, field, ligne.get(field, ''))

    # Bloc : Visit
    section_title(pdf, "Visit")
    for field in ["Language", "School level", "Number of people", "Max capacity", "Program", "Program details"]:
        add_field(pdf, field, ligne.get(field, ''))

    # Bloc : Timing
    section_title(pdf, "Timing")
    for field in ["Start time", "Start location", "End time", "End location", "Duration"]:
        add_field(pdf, field, ligne.get(field, ''))

    # Bloc : Price
    section_title(pdf, "Rates")
    for field in ["Visit type", "Guiding fee (excl. VAT)", "VAT on guiding (20%)", "Driver fee (excl. VAT)", "VAT on driver (10%)", "Total incl. VAT"]:
        add_field(pdf, field, ligne.get(field, ''))

    # Bloc : VIP
    section_title(pdf, "VIP Option")
    for field in ["VIP", "VIP notes"]:
        add_field(pdf, field, ligne.get(field, ''))

    # Génération et téléchargement
    nom_fichier = f"form_{ligne.get('Reference') or ligne.get('Last name')}_{ligne.get('Institution') or ligne.get('First name')}.pdf".replace(" ", "_")
    pdf.output(nom_fichier)
    with open(nom_fichier, "rb") as f:
        st.download_button("Download PDF", f, nom_fichier, mime="application/pdf")




