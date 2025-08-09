import os
import sys
import sqlite3
import threading
import time
import webbrowser
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import pandas as pd
import numpy as np
import random

class SmartBillApp:
    def __init__(self):
        print("🚀 Inițializare SmartBill App...")

        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        CORS(self.app)  # Adaugă suport CORS
        self.app.secret_key = 'smartbill_secret_2024'
        self.base_path = "d:/SmartBillLikeApp"
        self.db_path = f"{self.base_path}/database/smartbill_database.xlsx"
        self.data_cache = {}  # Cache for Excel data

        # Email configuration
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 465,
            'sender_email': 'ioan.fantanaru@gmail.com',
            'sender_password': 'PUT YOUR PASS HERE',
            'default_receivers': ['neculai.fantanaru@gmail.com', 'me.suzana@gmail.com']
        }

        self.setup_routes()
        self.ensure_database()
        print("✅ SmartBill App inițializată cu succes!")

    def backup_database(self):
        """Creează backup al bazei de date existente"""
        if os.path.exists(self.db_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.db_path}.backup_{timestamp}"
            try:
                import shutil
                shutil.copy2(self.db_path, backup_path)
                print(f"📋 Backup creat: {backup_path}")
                return backup_path
            except Exception as e:
                print(f"⚠️ Nu s-a putut crea backup: {e}")
                return None
        return None

    def load_existing_data(self, sheet_name):
        """Încarcă datele existente dintr-un sheet"""
        try:
            if os.path.exists(self.db_path):
                df = pd.read_excel(self.db_path, sheet_name=sheet_name)
                print(f"📊 Încărcat sheet existent '{sheet_name}': {len(df)} înregistrări")
                return df
            else:
                print(f"📊 Nu există date în sheet '{sheet_name}' - va fi creat nou")
                return None
        except Exception as e:
            print(f"⚠️ Eroare la încărcarea sheet-ului '{sheet_name}': {e}")
            return None

    def ensure_database(self):
        """Verifică și creează baza de date DOAR dacă nu există - PĂSTREAZĂ datele existente"""
        print("="*60)
        print("🔍 VERIFICARE PERSISTENTĂ A BAZEI DE DATE")
        print("="*60)
        print(f"📂 Calea bazei de date: {self.db_path}")
        print(f"📂 Directorul de bază: {self.base_path}")

        # Verifică dacă directorul există
        if not os.path.exists(self.base_path):
            print(f"📁 Creez directorul: {self.base_path}")
            os.makedirs(self.base_path, exist_ok=True)
            os.makedirs(f"{self.base_path}/database", exist_ok=True)

        # Verifică dacă fișierul bazei de date există
        if os.path.exists(self.db_path):
            file_size = os.path.getsize(self.db_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(self.db_path))

            print("✅ BAZA DE DATE EXISTĂ DEJA!")
            print(f"📊 Dimensiune fișier: {file_size} bytes")
            print(f"📅 Ultima modificare: {mod_time}")
            print("🔒 DATELE EXISTENTE VOR FI PĂSTRATE!")

            # Verifică integritatea bazei de date
            self.verify_database_integrity()
            return

        print("❌ BAZA DE DATE NU EXISTĂ")
        print("🆕 Creez baza de date cu structura inițială...")

        # Creează structura inițială cu date demo
        self.create_initial_database()

        print("="*60)
        print("✅ BAZA DE DATE CREATĂ CU SUCCES!")
        print("📊 Datele vor fi păstrate la următoarea pornire")
        print("="*60)

    def verify_database_integrity(self):
        """Verifică integritatea structurii bazei de date"""
        required_sheets = ['Facturi', 'Clienti', 'Produse', 'Bonuri_Fiscale', 'Facturi_Storno', 'Configurare']

        try:
            with pd.ExcelFile(self.db_path) as excel_file:
                existing_sheets = excel_file.sheet_names
                print(f"📋 Sheet-uri existente: {existing_sheets}")

                missing_sheets = []
                for sheet in required_sheets:
                    if sheet not in existing_sheets:
                        missing_sheets.append(sheet)
                    else:
                        # Verifică numărul de înregistrări
                        df = pd.read_excel(self.db_path, sheet_name=sheet)
                        print(f"📊 {sheet}: {len(df)} înregistrări")

                if missing_sheets:
                    print(f"⚠️ Sheet-uri lipsă: {missing_sheets}")
                    self.add_missing_sheets(missing_sheets)
                else:
                    print("✅ Toate sheet-urile necesare există!")

        except Exception as e:
            print(f"❌ Eroare la verificarea integrității: {e}")
            print("🔄 Recreez baza de date...")
            self.create_initial_database()

    def add_missing_sheets(self, missing_sheets):
        """Adaugă sheet-urile lipsă fără a afecta datele existente"""
        print(f"🔧 Adaug sheet-urile lipsă: {missing_sheets}")

        # Încarcă toate sheet-urile existente
        existing_data = {}
        if os.path.exists(self.db_path):
            try:
                with pd.ExcelFile(self.db_path) as excel_file:
                    for sheet_name in excel_file.sheet_names:
                        existing_data[sheet_name] = pd.read_excel(self.db_path, sheet_name=sheet_name)
                        print(f"📊 Păstrez datele din {sheet_name}: {len(existing_data[sheet_name])} înregistrări")
            except Exception as e:
                print(f"❌ Eroare la citirea datelor existente: {e}")

        # Adaugă sheet-urile lipsă cu structura corespunzătoare
        demo_data = self.get_demo_data()

        for sheet in missing_sheets:
            if sheet in demo_data:
                existing_data[sheet] = pd.DataFrame(demo_data[sheet])
                print(f"➕ Adăugat sheet nou: {sheet}")

        # Salvează toate datele (existente + noi)
        self.save_all_sheets(existing_data)

    def create_initial_database(self):
        """Creează baza de date inițială cu date demo"""
        demo_data = self.get_demo_data()

        print("💾 Salvez baza de date inițială...")
        with pd.ExcelWriter(self.db_path, engine='openpyxl') as writer:
            for sheet_name, data in demo_data.items():
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"📝 Salvat {sheet_name}: {len(df)} înregistrări")

        print(f"✅ Baza de date creată: {self.db_path}")
        print(f"📊 Dimensiune: {os.path.getsize(self.db_path)} bytes")

    def get_demo_data(self):
        """Returnează structura datelor demo"""
        return {
            'Facturi': {
                'ID': list(range(1, 11)),
                'Numar_Factura': [f'FACT-{i:03d}' for i in range(1, 11)],
                'Data_Emitere': [
                    (datetime.now() - timedelta(days=i*3)).strftime('%Y-%m-%d')
                    for i in range(10)
                ],
                'Data_Scadenta': [
                    (datetime.now() - timedelta(days=i*3) + timedelta(days=30)).strftime('%Y-%m-%d')
                    for i in range(10)
                ],
                'Serie_Factura': ['FACT'] * 10,
                'Client_CIF': ['RO12345678', 'RO87654321', '1234567890123', 'RO11223344', '9876543210987',
                              'RO99887766', 'RO55443322', '1111111111111', 'RO77778888', 'RO99990000'],
                'Client_Nume': ['SC DEMO SRL', 'SC TEST IMPEX', 'Popescu Ion', 'SC ALPHA BETA', 'Ionescu Maria',
                               'SC GAMMA DELTA', 'SC OMEGA PLUS', 'Vasilescu Ana', 'SC SIGMA TECH', 'Georgescu Dan'],
                'Client_Email': ['demo@test.ro', 'office@testimex.ro', 'popescu@email.ro', 'alpha@beta.ro', 'maria@email.ro',
                                'gamma@delta.ro', 'omega@plus.ro', 'vasilescu@email.ro', 'sigma@tech.ro', 'georgescu@email.ro'],
                'Client_Telefon': ['0721123456', '0732987654', '0743555666', '0755888999', '0766111222',
                                  '0777333444', '0788555666', '0799777888', '0700111222', '0711333444'],
                'Client_Localitate': ['București', 'Cluj-Napoca', 'Timișoara', 'Iași', 'Constanța',
                                     'Brașov', 'Galați', 'Ploiești', 'Oradea', 'Craiova'],
                'Subtotal': [1500.00, 2800.50, 1200.00, 3500.00, 890.00, 2200.00, 1800.00, 950.00, 4200.00, 1600.00],
                'TVA': [285.00, 532.10, 228.00, 665.00, 169.10, 418.00, 342.00, 180.50, 798.00, 304.00],
                'Total': [1785.00, 3332.60, 1428.00, 4165.00, 1059.10, 2618.00, 2142.00, 1130.50, 4998.00, 1904.00],
                'Status': ['Platita', 'Neplatita', 'Platita', 'Neplatita', 'Platita', 'Neplatita', 'Platita', 'Platita', 'Neplatita', 'Platita'],
                'Moneda': ['RON'] * 10,
                'Curs_Schimb': [1.00] * 10,
                'Observatii': ['Factura pentru servicii IT', 'Dezvoltare software', 'Consultanță financiară',
                              'Audit sistem', 'Mentenanță hardware', 'Licențe software', 'Training personal',
                              'Suport tehnic', 'Implementare sistem', 'Optimizare procese'],
                'Termeni_Plata': ['30 zile'] * 10
            },
            'Clienti': {
                'ID': list(range(1, 11)),
                'CIF': ['RO12345678', 'RO87654321', '1234567890123', 'RO11223344', '9876543210987',
                       'RO99887766', 'RO55443322', '1111111111111', 'RO77778888', 'RO99990000'],
                'Nume': ['SC DEMO SRL', 'SC TEST IMPEX', 'Popescu Ion', 'SC ALPHA BETA', 'Ionescu Maria',
                        'SC GAMMA DELTA', 'SC OMEGA PLUS', 'Vasilescu Ana', 'SC SIGMA TECH', 'Georgescu Dan'],
                'Client_Email': ['demo@test.ro', 'office@testimex.ro', 'popescu@email.ro', 'alpha@beta.ro', 'maria@email.ro',
                         'gamma@delta.ro', 'omega@plus.ro', 'vasilescu@email.ro', 'sigma@tech.ro', 'georgescu@email.ro'],
                'Client_Telefon': ['0721123456', '0732987654', '0743555666', '0755888999', '0766111222',
                           '0777333444', '0788555666', '0799777888', '0700111222', '0711333444'],
                'Client_Localitate': ['București', 'Cluj-Napoca', 'Timișoara', 'Iași', 'Constanța',
                              'Brașov', 'Galați', 'Ploiești', 'Oradea', 'Craiova'],
                'Client_Judet': ['București', 'Cluj', 'Timiș', 'Iași', 'Constanța', 'Brașov', 'Galați', 'Prahova', 'Bihor', 'Dolj'],
                'Client_Adresa': ['Str. Exemplu, Nr. 123', 'Bd. Central, Nr. 45', 'Str. Libertății, Nr. 67',
                          'Str. Universității, Nr. 89', 'Str. Mării, Nr. 12', 'Str. Republicii, Nr. 34',
                          'Str. Dunării, Nr. 56', 'Str. Independenței, Nr. 78', 'Str. Revoluției, Nr. 90',
                          'Str. Olteniei, Nr. 11'],
                'Client_Cod_Postal': ['010101', '400001', '300001', '700001', '900001', '500001', '800001', '100001', '410001', '200001'],
                'Tara': ['România'] * 10,
                'Website': ['www.demo.ro', 'www.testimex.ro', '', 'www.alphabeta.ro', '',
                           'www.gammadelta.ro', 'www.omegaplus.ro', '', 'www.sigmatech.ro', ''],
                'Persoana_Contact': ['Ion Popescu', 'Maria Ionescu', 'Popescu Ion', 'Dan Georgescu', 'Ionescu Maria',
                                    'Ana Vasilescu', 'Elena Marinescu', 'Vasilescu Ana', 'Mihai Popa', 'Georgescu Dan'],
                'Observatii': ['Client fidel', 'Client nou', 'Client individual', 'Client corporatist', 'Client ocazional',
                              'Client VIP', 'Client cu discount', 'Client cu termen extins', 'Client preferat', 'Client standard'],
                'Sold_Curent': [0.00, 3332.60, 0.00, 4165.00, 0.00, 2618.00, 0.00, 0.00, 4998.00, 0.00],
                'Status': ['Activ', 'Activ', 'Activ', 'Activ', 'Activ', 'Activ', 'Activ', 'Activ', 'Activ', 'Activ']
            },
            'Produse': {
                'ID': list(range(1, 11)),
                'Cod': ['SERV-001', 'SERV-002', 'PROD-001', 'PROD-002', 'MAT-001', 'MAT-002', 'SOFT-001', 'CONS-001', 'HARD-001', 'LIC-001'],
                'Denumire': [
                    'Consultanță IT', 'Dezvoltare software', 'Laptop Dell Inspiron', 'Monitor Samsung 24"',
                    'Hârtie A4 80g', 'Cartus toner HP', 'Licență Office 365', 'Audit financiar',
                    'Server Dell PowerEdge', 'Licență Windows Server'
                ],
                'UM': ['ore', 'ore', 'buc', 'buc', 'pachet', 'buc', 'licență', 'ore', 'buc', 'licență'],
                'Pret_Vanzare': [150.00, 200.00, 3500.00, 1200.00, 35.00, 200.00, 650.00, 300.00, 8500.00, 1200.00],
                'Pret_Achizitie': [100.00, 150.00, 2800.00, 900.00, 25.00, 150.00, 500.00, 200.00, 6800.00, 900.00],
                'TVA_Procent': [19] * 10,
                'Categorie': ['Servicii IT', 'Servicii IT', 'Hardware', 'Hardware', 'Consumabile', 'Consumabile', 'Software', 'Servicii', 'Hardware', 'Software'],
                'Stoc': [999, 999, 5, 8, 50, 12, 999, 999, 2, 999],
                'Stoc_Minim': [0, 0, 2, 3, 10, 5, 0, 0, 1, 0],
                'Furnizor': ['Intern', 'Intern', 'Dell România', 'Samsung România', 'Office Depot', 'HP România', 'Microsoft', 'Intern', 'Dell România', 'Microsoft'],
                'Descriere': [
                    'Consultanță în tehnologii informaționale',
                    'Dezvoltare aplicații software personalizate',
                    'Laptop Dell Inspiron 15 cu procesor Intel i5',
                    'Monitor Samsung 24" Full HD',
                    'Hârtie A4 80g, 500 foi/pachet',
                    'Cartus toner HP pentru imprimante laser',
                    'Licență Microsoft Office 365 Business',
                    'Audit financiar și contabil',
                    'Server Dell PowerEdge R740',
                    'Licență Windows Server 2019 Standard'
                ],
                'Cod_Bare': ['123456789', '987654321', '456789123', '789123456', '321654987', '654987321', '147258369', '963852741', '258369147', '741963852'],
                'Cod_Furnizor': ['F001', 'F002', 'F003', 'F004', 'F005', 'F006', 'F007', 'F008', 'F009', 'F010'],
                'Greutate': [0, 0, 2.5, 3.2, 0.5, 0.8, 0, 0, 25.0, 0],
                'Volum': [0, 0, 0.015, 0.008, 0.002, 0.001, 0, 0, 0.045, 0],
                'Observatii': ['Serviciu intern', 'Serviciu intern', 'Produs popular', 'Monitor de calitate', 'Consumabil standard', 'Cartus original', 'Licență oficială', 'Serviciu specializat', 'Server enterprise', 'Licență server']
            },
            'Bonuri_Fiscale': {
                'ID': list(range(1, 11)),
                'Numar_Bon': [f'BF-{i:03d}' for i in range(1, 11)],
                'Data_Emitere': [
                    (datetime.now() - timedelta(days=i*2)).strftime('%Y-%m-%d')
                    for i in range(10)
                ],
                'Ora_Emitere': ['09:15', '14:30', '11:45', '16:20', '10:10', '13:25', '15:40', '08:55', '17:15', '12:30'],
                'Serie_Bon': ['BF'] * 10,
                'Numar_Casa': ['CASA-001'] * 10,
                'Operator': ['Operator 1', 'Operator 2', 'Operator 1', 'Operator 3', 'Operator 2', 'Operator 1', 'Operator 3', 'Operator 2', 'Operator 1', 'Operator 3'],
                'Client_Nume': ['Popescu Ion', 'Ionescu Maria', 'Vasilescu Ana', 'Georgescu Dan', 'Marinescu Elena',
                               'Stoica Mihai', 'Dumitrescu Laura', 'Constantinescu Andrei', 'Munteanu Diana', 'Ilie Carmen'],
                'Client_Email': ['popescu@email.ro', 'maria@email.ro', 'ana@email.ro', 'dan@email.ro', 'elena@email.ro',
                                'mihai@email.ro', 'laura@email.ro', 'andrei@email.ro', 'diana@email.ro', 'carmen@email.ro'],
                'Client_Telefon': ['0743555666', '0766111222', '0777333444', '0788555666', '0799777888',
                                  '0700111222', '0711333444', '0722444555', '0733666777', '0744888999'],
                'Subtotal': [150.00, 280.50, 120.00, 350.00, 89.00, 220.00, 180.00, 95.00, 420.00, 160.00],
                'TVA': [28.50, 53.30, 22.80, 66.50, 16.91, 41.80, 34.20, 18.05, 79.80, 30.40],
                'Total': [178.50, 333.80, 142.80, 416.50, 105.91, 261.80, 214.20, 113.05, 499.80, 190.40],
                'Metoda_Plata': ['Card', 'Numerar', 'Card', 'Numerar', 'Card', 'Numerar', 'Card', 'Numerar', 'Card', 'Numerar'],
                'Suma_Primita': [200.00, 350.00, 150.00, 500.00, 110.00, 300.00, 250.00, 120.00, 500.00, 200.00],
                'Rest': [21.50, 16.20, 7.20, 83.50, 4.09, 38.20, 35.80, 6.95, 0.20, 9.60],
                'Observatii': ['Bon pentru servicii', 'Bon pentru produse', 'Bon pentru consumabile', 'Bon pentru hardware', 'Bon pentru software',
                              'Bon pentru licențe', 'Bon pentru training', 'Bon pentru suport', 'Bon pentru audit', 'Bon pentru consultanță']
            },
            'Facturi_Storno': {
                'ID': list(range(1, 6)),
                'Numar_Factura_Originala': ['FACT-001', 'FACT-003', 'FACT-005', 'FACT-007', 'FACT-009'],
                'Data_Emitere': [
                    (datetime.now() - timedelta(days=i*5)).strftime('%Y-%m-%d')
                    for i in range(5)
                ],
                'Serie_Factura': ['STORN'] * 5,
                'Client_CIF': ['RO12345678', '1234567890123', '9876543210987', '1111111111111', 'RO77778888'],
                'Client_Nume': ['SC DEMO SRL', 'Popescu Ion', 'Ionescu Maria', 'Vasilescu Ana', 'SC SIGMA TECH'],
                'Client_Email': ['demo@test.ro', 'popescu@email.ro', 'maria@email.ro', 'vasilescu@email.ro', 'sigma@tech.ro'],
                'Client_Telefon': ['0721123456', '0743555666', '0766111222', '0777333444', '0700111222'],
                'Client_Localitate': ['București', 'Timișoara', 'Constanța', 'Brașov', 'Oradea'],
                'Subtotal_Original': [1500.00, 1200.00, 890.00, 1800.00, 4200.00],
                'TVA_Original': [285.00, 228.00, 169.10, 342.00, 798.00],
                'Total_Original': [1785.00, 1428.00, 1059.10, 2142.00, 4998.00],
                'Subtotal_Storno': [-1500.00, -1200.00, -890.00, -1800.00, -4200.00],
                'TVA_Storno': [-285.00, -228.00, -169.10, -342.00, -798.00],
                'Total_Storno': [-1785.00, -1428.00, -1059.10, -2142.00, -4998.00],
                'Motiv_Storno': ['Eroare în datele clientului', 'Produs indisponibil', 'Client a renunțat', 'Eroare în calculul TVA', 'Factură duplicată'],
                'Status': ['Emis', 'Emis', 'Emis', 'Emis', 'Emis'],
                'Observatii': ['Storno pentru eroare în date', 'Storno pentru indisponibilitate', 'Storno la cererea clientului', 'Storno pentru eroare calcul', 'Storno pentru duplicare']
            },
            'Configurare': {
                'Nume_Companie': ['TIP B. SRL'],
                'CIF': ['RO12345678'],
                'Adresa': ['Str. Exemplu, Nr. 123, București'],
                'Telefon': ['021 123 4567'],
                'Email': ['office@tipb.ro'],
                'Website': ['www.tipb.ro'],
                'Cont_Bancar': ['RO49 AAAA 1B31 0075 9384 0000'],
                'Banca': ['Banca Transilvania'],
                'TVA': [19],
                'Moneda': ['RON']
            }
        }

    def save_all_sheets(self, sheets_data):
        """Salvează toate sheet-urile în Excel"""
        try:
            with pd.ExcelWriter(self.db_path, engine='openpyxl') as writer:
                for sheet_name, df in sheets_data.items():
                    if isinstance(df, dict):
                        df = pd.DataFrame(df)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"💾 Salvat {sheet_name}: {len(df)} înregistrări")
            print("✅ Toate sheet-urile salvate cu succes!")
        except Exception as e:
            print(f"❌ Eroare la salvarea sheet-urilor: {e}")

    def send_email(self, to_email, subject, html_content, cc_email=None, attach_pdf=False, pdf_content=None, pdf_filename=None):
        """Send email with HTML content and optional PDF attachment"""
        try:
            print(f"📧 Attempting to send email to: {to_email}, CC: {cc_email}")

            # Creează mesajul principal
            message = MIMEMultipart('alternative')
            message['From'] = f"SmartBill App <{self.email_config['sender_email']}>"
            message['To'] = to_email
            if cc_email:
                message['Cc'] = cc_email
            message['Subject'] = subject
            message['X-Mailer'] = 'SmartBill App v1.0'
            message['X-Priority'] = '3'
            message['Message-ID'] = f"<{datetime.now().strftime('%Y%m%d%H%M%S')}@smartbill.app>"
            message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

            # Versiunea text simplă
            text_content = f"""
Factură SmartBill

Această factură a fost generată automat de SmartBill App.
Pentru detalii complete, vă rugăm să deschideți versiunea HTML.

Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            """.strip()

            # Adaugă ambele versiuni (text și HTML)
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')

            message.attach(text_part)
            message.attach(html_part)

            if attach_pdf and pdf_content and pdf_filename:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(pdf_content)
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename={pdf_filename}')
                message.attach(attachment)
                print(f"📎 Attached PDF: {pdf_filename}")

            with smtplib.SMTP_SSL(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])

                # Trimite email-uri individuale pentru fiecare destinatar pentru a evita problemele cu CC
                all_recipients = [to_email]
                if cc_email:
                    if isinstance(cc_email, str):
                        all_recipients.extend([email.strip() for email in cc_email.split(',')])
                    else:
                        all_recipients.append(cc_email)

                # Elimină duplicatele
                unique_recipients = list(set(all_recipients))

                successful_sends = 0
                failed_sends = []

                for i, recipient in enumerate(unique_recipients):
                    try:
                        # Creează un mesaj individual pentru fiecare destinatar
                        individual_message = MIMEMultipart('alternative')
                        individual_message['From'] = f"SmartBill App <{self.email_config['sender_email']}>"
                        individual_message['To'] = recipient
                        individual_message['Subject'] = subject
                        individual_message['X-Mailer'] = 'SmartBill App v1.0'
                        individual_message['X-Priority'] = '3'
                        individual_message['Message-ID'] = f"<{datetime.now().strftime('%Y%m%d%H%M%S')}{i}@smartbill.app>"
                        individual_message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

                        # Adaugă conținutul
                        individual_message.attach(MIMEText(text_content, 'plain', 'utf-8'))
                        individual_message.attach(MIMEText(html_content, 'html', 'utf-8'))

                        # Trimite către destinatarul individual
                        server.send_message(individual_message)
                        print(f"✅ Email trimis cu succes către: {recipient}")
                        successful_sends += 1

                        # Pauză scurtă între email-uri pentru a evita rate limiting
                        if i < len(unique_recipients) - 1:
                            time.sleep(1)

                    except Exception as e:
                        print(f"❌ Eroare la trimiterea către {recipient}: {e}")
                        failed_sends.append(recipient)
                        continue

                # Raport final
                print(f"📊 Raport trimitere email:")
                print(f"   ✅ Trimise cu succes: {successful_sends}")
                print(f"   ❌ Eșuate: {len(failed_sends)}")
                if failed_sends:
                    print(f"   📧 Adrese eșuate: {', '.join(failed_sends)}")

                # Returnează True dacă cel puțin un email a fost trimis cu succes
                return successful_sends > 0

                print(f"✅ Procesul de trimitere email finalizat pentru {len(unique_recipients)} destinatari")
                return True
        except smtplib.SMTPAuthenticationError:
            print("❌ Authentication failed. Check email credentials.")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP Error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ General Error: {str(e)}")
            return False

    def load_sheet_to_cache(self, sheet_name):
        """Load sheet data to cache for better performance"""
        if sheet_name not in self.data_cache:
            try:
                df = pd.read_excel(self.db_path, sheet_name=sheet_name)
                df = df.fillna({
                    'Website': '', 'Sold_Curent': 0.0, 'Email': '', 'Telefon': '', 'Localitate': '',
                    'Judet': '', 'Adresa': '', 'Cod_Postal': '', 'Persoana_Contact': '', 'Observatii': '',
                    'Nume': '', 'CIF': '', 'Tara': 'România', 'Descriere': '', 'Pret_Vanzare': 0.0,
                    'Pret_Achizitie': 0.0, 'Stoc': 0, 'Stoc_Minim': 0, 'Greutate': 0.0, 'Volum': 0.0,
                    'Cod_Bare': '', 'Cod_Furnizor': '', 'Furnizor': '', 'Categorie': '', 'UM': 'buc',
                    'Client_Email': '', 'Client_Telefon': '', 'Client_Localitate': '', 'Subtotal': 0.0,
                    'TVA': 0.0, 'Total': 0.0, 'Motiv_Storno': '', 'Subtotal_Original': 0.0,
                    'TVA_Original': 0.0, 'Total_Original': 0.0, 'Subtotal_Storno': 0.0,
                    'TVA_Storno': 0.0, 'Total_Storno': 0.0
                }).replace({np.nan: ''}).replace({np.nan: 0.0})
                self.data_cache[sheet_name] = df
                print(f"📊 Încărcat {len(df)} înregistrări din {sheet_name} în cache")
            except Exception as e:
                print(f"❌ Eroare la încărcarea {sheet_name} în cache: {e}")
                self.data_cache[sheet_name] = pd.DataFrame()
        return self.data_cache[sheet_name]

    def clear_cache(self, sheet_name=None):
        """Clear cache for specific sheet or all sheets"""
        if sheet_name:
            if sheet_name in self.data_cache:
                del self.data_cache[sheet_name]
                print(f"🗑️ Cache șters pentru {sheet_name}")
        else:
            self.data_cache.clear()
            print("🗑️ Toate cache-urile au fost șterse")

    def save_excel_sheet(self, df, sheet_name):
        """Salvează un DataFrame într-un sheet Excel FĂRĂ a afecta alte sheet-uri"""
        try:
            print(f"=== SALVARE PERSISTENTĂ SHEET {sheet_name} ===")
            print(f"📊 Salvez {len(df)} înregistrări în {sheet_name}")

            # Creează backup înainte de salvare
            backup_path = self.backup_database()

            # Citește toate sheet-urile existente
            existing_sheets = {}
            if os.path.exists(self.db_path):
                try:
                    with pd.ExcelFile(self.db_path) as excel_file:
                        for existing_sheet in excel_file.sheet_names:
                            if existing_sheet != sheet_name:
                                existing_sheets[existing_sheet] = pd.read_excel(self.db_path, sheet_name=existing_sheet)
                                print(f"📋 Păstrez {existing_sheet}: {len(existing_sheets[existing_sheet])} înregistrări")
                except Exception as e:
                    print(f"⚠️ Eroare la citirea sheet-urilor existente: {e}")

            # Adaugă sheet-ul nou/actualizat
            existing_sheets[sheet_name] = df

            # Salvează toate sheet-urile
            with pd.ExcelWriter(self.db_path, engine='openpyxl') as writer:
                for sheet, data in existing_sheets.items():
                    data.to_excel(writer, sheet_name=sheet, index=False)
                    print(f"💾 Salvat {sheet}: {len(data)} înregistrări")

            # Șterge cache-ul pentru sheet-ul modificat
            self.clear_cache(sheet_name)

            print(f"✅ Sheet {sheet_name} salvat cu succes!")
            print(f"📊 Dimensiune finală: {os.path.getsize(self.db_path)} bytes")

        except Exception as e:
            print(f"❌ Eroare la salvarea sheet-ului {sheet_name}: {e}")
            # Restaurează backup dacă există
            if backup_path and os.path.exists(backup_path):
                try:
                    import shutil
                    shutil.copy2(backup_path, self.db_path)
                    print(f"🔄 Restaurat backup: {backup_path}")
                except Exception as backup_error:
                    print(f"❌ Eroare la restaurarea backup: {backup_error}")

    def validate_input(self, data, required_fields, field_types=None):
        """Validate input data"""
        errors = []

        # Check required fields
        for field in required_fields:
            if not data.get(field):
                errors.append(f'Câmpul {field} este obligatoriu!')

        # Check field types if provided
        if field_types:
            for field, field_type in field_types.items():
                if field in data:
                    if field_type == 'string' and not isinstance(data[field], str):
                        errors.append(f'Câmpul {field} trebuie să fie text!')
                    elif field_type == 'number' and not isinstance(data[field], (int, float)):
                        errors.append(f'Câmpul {field} trebuie să fie număr!')
                    elif field_type == 'email' and '@' not in str(data[field]):
                        errors.append(f'Câmpul {field} trebuie să fie o adresă de email validă!')

        return len(errors) == 0

    def setup_routes(self):
        """Configurează rutele Flask"""

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/dashboard')
        def dashboard():
            stats = self.get_stats()

            # Activitate recentă
            recent_activities = [
                {
                    'icon': 'fas fa-file-invoice',
                    'title': 'Factură FACT-005 emisă',
                    'description': 'pentru Ionescu Maria - 1,059.10 RON',
                    'date': 'Azi, 14:30'
                },
                {
                    'icon': 'fas fa-user-plus',
                    'title': 'Client nou adăugat',
                    'description': 'SC ALPHA BETA SRL',
                    'date': 'Ieri, 16:45'
                },
                {
                    'icon': 'fas fa-money-bill-wave',
                    'title': 'Plată încasată',
                    'description': 'FACT-001 - 1,785.00 RON',
                    'date': 'Ieri, 10:20'
                },
                {
                    'icon': 'fas fa-box',
                    'title': 'Produs nou adăugat',
                    'description': 'Laptop Dell Inspiron - 3,500.00 RON',
                    'date': 'Acum 2 zile'
                }
            ]

            return render_template('dashboard.html', stats=stats, recent_activities=recent_activities)


        @self.app.route('/api/save_factura_storno', methods=['POST'])
        def save_factura_storno():
            try:
                data = request.get_json()
                
                # Citire date existente
                try:
                    df = pd.read_excel(self.db_path, sheet_name='Facturi_Storno')
                except:
                    # Dacă sheet-ul nu există, creează unul nou
                    df = pd.DataFrame()
                
                # Adăugare factură storno nouă
                new_storno = {
                    'ID': len(df) + 1,
                    'Numar_Factura_Originala': data['original_invoice_number'],
                    'Data_Emitere': data['storno_date'],
                    'Serie_Factura': 'STORNO',
                    'Client_CIF': data['client_cif'],
                    'Client_Nume': data['client_name'],
                    'Client_Email': data['client_email'],
                    'Client_Telefon': '',
                    'Client_Localitate': '',
                    'Subtotal_Original': data['original_subtotal'],
                    'TVA_Original': data['original_tva'],
                    'Total_Original': data['original_total'],
                    'Subtotal_Storno': data['storno_subtotal'],
                    'TVA_Storno': data['storno_tva'],
                    'Total_Storno': data['storno_total'],
                    'Motiv_Storno': data['storno_reason'],
                    'Status': 'In asteptare',
                    'Observatii': data['storno_notes']
                }
                
                df = pd.concat([df, pd.DataFrame([new_storno])], ignore_index=True)
                self.save_excel_sheet(df, 'Facturi_Storno')
                
                return jsonify({'success': True, 'message': 'Factura storno a fost salvată cu succes'})
                
            except Exception as e:
                print(f"Eroare la salvarea storno-ului: {e}")
                return jsonify({'success': False, 'message': str(e)}), 500

        @self.app.route('/api/get_facturi_storno')
        def get_facturi_storno():
            try:
                try:
                    df = pd.read_excel(self.db_path, sheet_name='Facturi_Storno')
                    storno_list = []
                    for _, storno in df.iterrows():
                        storno_list.append({
                            'id': storno['ID'],
                            'numar_factura_originala': storno['Numar_Factura_Originala'],
                            'client_nume': storno['Client_Nume'],
                            'data_emitere': storno['Data_Emitere'],
                            'total_original': storno['Total_Original'],
                            'total_storno': storno['Total_Storno'],
                            'motiv_storno': storno['Motiv_Storno'],
                            'status': storno['Status']
                        })
                    return jsonify(storno_list)
                except:
                    return jsonify([])
                
            except Exception as e:
                print(f"Eroare la încărcarea storno-urilor: {e}")
                return jsonify([]), 500



        @self.app.route('/factura')
        def factura():
            return render_template('factura.html')

        @self.app.route('/bon-fiscal')
        def bon_fiscal():
            return render_template('bon_fiscal.html')

        @self.app.route('/clienti')
        def clienti():
            return render_template('clienti.html')

        @self.app.route('/produse')
        def produse():
            return render_template('produse.html')

        @self.app.route('/rapoarte')
        def rapoarte():
            return render_template('rapoarte.html')

        @self.app.route('/configurare')
        def configurare():
            return render_template('configurare.html')

        @self.app.route('/factura-storno')
        def factura_storno():
            return render_template('factura-storno.html')

        @self.app.route('/test')
        def test():
            return render_template('test.html')

        @self.app.route('/test-simple')
        def test_simple():
            return render_template('test_simple.html')

        # API Routes pentru trimiterea de email-uri
        @self.app.route('/api/send_invoice_email', methods=['POST'])
        def api_send_invoice_email():
            try:
                data = request.get_json()

                # Prepare invoice data for HTML generation
                invoice_data = {
                    'invoice_number': data.get('invoice_number'),
                    'client_name': data.get('client_name'),
                    'client_cif': data.get('client_cif'),
                    'client_email': data.get('client_email'),
                    'client_phone': data.get('client_phone'),
                    'issue_date': data.get('issue_date'),
                    'due_date': data.get('due_date'),
                    'payment_terms': data.get('payment_terms'),
                    'subtotal': float(data.get('subtotal', 0)),
                    'tva': float(data.get('tva', 0)),
                    'total': float(data.get('total', 0))
                }

                # Generate HTML content
                html_content = self.generate_invoice_html(invoice_data)

                # Send email
                success = self.send_email(
                    to_email=data.get('email_to'),
                    subject=data.get('email_subject'),
                    html_content=html_content,
                    cc_email=data.get('email_cc'),
                    attach_pdf=data.get('attach_pdf', False)
                )

                if success:
                    return jsonify({'success': True, 'message': 'Email trimis cu succes!'})
                else:
                    return jsonify({'success': False, 'message': 'Eroare la trimiterea email-ului'})

            except Exception as e:
                print(f"❌ Eroare API send_invoice_email: {e}")
                return jsonify({'success': False, 'message': str(e)})

        @self.app.route('/api/send_storno_email', methods=['POST'])


        def api_send_storno_email():
            try:
                print("=== API SEND STORNO EMAIL ===")
                data = request.get_json()
                print(f"📧 Date email storno: {data}")

                # Prepare storno data for HTML generation
                storno_data = {
                    'storno_id': data.get('storno_id', f"STORN-{len(pd.read_excel(self.db_path, sheet_name='Facturi_Storno')) + 1:03d}"),
                    'original_invoice': data.get('original_invoice'),
                    'client_name': data.get('client_name'),
                    'client_cif': data.get('client_cif'),
                    'client_email': data.get('client_email'),
                    'storno_date': data.get('storno_date'),
                    'reason': data.get('reason'),
                    'notes': data.get('notes', ''),
                    'original_subtotal': float(data.get('original_subtotal', 0)),
                    'original_tva': float(data.get('original_tva', 0)),
                    'original_total': float(data.get('original_total', 0)),
                    'storno_subtotal': -float(data.get('original_subtotal', 0)),
                    'storno_tva': -float(data.get('original_tva', 0)),
                    'storno_total': -float(data.get('original_total', 0))
                }

                # Generate HTML content
                html_content = self.generate_storno_html(storno_data)

                # Send email
                success = self.send_email(
                    to_email=data.get('email_to'),
                    subject=data.get('email_subject', f'Factură Storno pentru {storno_data["original_invoice"]}'),
                    html_content=html_content,
                    cc_email=data.get('email_cc'),
                    attach_pdf=data.get('attach_pdf', False)
                )

                if success:
                    # Salvează factura storno în baza de date după trimiterea cu succes
                    storno_save_data = {
                        'numar_factura_originala': storno_data['original_invoice'],
                        'data_emitere': storno_data['storno_date'],
                        'client_cif': storno_data['client_cif'],
                        'client_nume': storno_data['client_name'],
                        'client_email': storno_data['client_email'],
                        'subtotal_original': storno_data['original_subtotal'],
                        'tva_original': storno_data['original_tva'],
                        'total_original': storno_data['original_total'],
                        'motiv_storno': storno_data['reason'],
                        'observatii': storno_data['notes']
                    }

                    # Salvează în Excel
                    try:
                        df = pd.read_excel(self.db_path, sheet_name='Facturi_Storno')
                        new_storno = {
                            'ID': len(df) + 1,
                            'Numar_Factura_Originala': storno_save_data['numar_factura_originala'],
                            'Data_Emitere': storno_save_data['data_emitere'],
                            'Serie_Factura': 'STORN',
                            'Client_CIF': storno_save_data['client_cif'],
                            'Client_Nume': storno_save_data['client_nume'],
                            'Client_Email': storno_save_data['client_email'],
                            'Client_Telefon': '',
                            'Client_Localitate': '',
                            'Subtotal_Original': storno_save_data['subtotal_original'],
                            'TVA_Original': storno_save_data['tva_original'],
                            'Total_Original': storno_save_data['total_original'],
                            'Subtotal_Storno': -storno_save_data['subtotal_original'],
                            'TVA_Storno': -storno_save_data['tva_original'],
                            'Total_Storno': -storno_save_data['total_original'],
                            'Motiv_Storno': storno_save_data['motiv_storno'],
                            'Status': 'Emis',
                            'Observatii': storno_save_data['observatii']
                        }
                        df = pd.concat([df, pd.DataFrame([new_storno])], ignore_index=True)
                        self.save_excel_sheet(df, 'Facturi_Storno')
                        print("✅ Factură storno salvată în baza de date")
                    except Exception as save_error:
                        print(f"⚠️ Eroare la salvarea în baza de date: {save_error}")

                    return jsonify({'success': True, 'message': 'Email storno trimis cu succes și salvat în baza de date!'})
                else:
                    return jsonify({'success': False, 'message': 'Eroare la trimiterea email-ului storno'})

            except Exception as e:
                print(f"❌ Eroare API send_storno_email: {e}")
                return jsonify({'success': False, 'message': str(e)})

        # API Routes existente
        @self.app.route('/api/dashboard_stats')
        def api_stats():
            return jsonify(self.get_stats())

        @self.app.route('/api/get_clienti')
        def api_clienti():
            try:
                print("=== API GET CLIENTI ===")
                print(f"📂 DB Path: {self.db_path}")
                print(f"📊 DB Path exists: {os.path.exists(self.db_path)}")

                df = pd.read_excel(self.db_path, sheet_name='Clienti')
                df = df.fillna({
                    'Website': '', 'Sold_Curent': 0.0, 'Client_Email': '', 'Client_Telefon': '', 'Client_Localitate': '',
                    'Client_Judet': '', 'Client_Adresa': '', 'Client_Cod_Postal': '', 'Persoana_Contact': '', 'Observatii': '',
                    'Nume': '', 'CIF': '', 'Tara': 'România', 'Status': 'Activ'
                })
                df = df.replace({np.nan: ''}).replace({np.nan: 0.0})

                # Forțează adăugarea ID-urilor pentru toate înregistrările
                df['ID'] = range(1, len(df) + 1)

                print(f"📊 Clienți citiți cu succes: {len(df)} înregistrări")

                result = df.to_dict('records')
                return jsonify(result)
            except Exception as e:
                print(f"❌ Eroare la citirea clienților: {str(e)}")
                return jsonify([])

        @self.app.route('/api/get_produse')
        def api_produse():
            try:
                df = pd.read_excel(self.db_path, sheet_name='Produse')
                df = df.fillna({
                    'Descriere': '', 'Pret_Vanzare': 0.0, 'Pret_Achizitie': 0.0, 'Stoc': 0, 'Stoc_Minim': 0,
                    'Greutate': 0.0, 'Volum': 0.0, 'Cod_Bare': '', 'Cod_Furnizor': '', 'Furnizor': '',
                    'Categorie': '', 'UM': 'buc', 'TVA_Procent': 19, 'Observatii': ''
                })
                df = df.replace({np.nan: ''}).replace({np.nan: 0.0})

                # Forțează adăugarea ID-urilor pentru toate înregistrările
                df['ID'] = range(1, len(df) + 1)

                result = df.to_dict('records')
                print(f"📦 Produse încărcate: {len(result)} înregistrări")
                return jsonify(result)
            except Exception as e:
                print(f"❌ Eroare la încărcarea produselor: {e}")
                return jsonify([])

        @self.app.route('/api/get_bonuri_fiscale')
        def api_bonuri_fiscale():
            try:
                df = pd.read_excel(self.db_path, sheet_name='Bonuri_Fiscale')
                df = df.fillna({
                    'Client_Email': '', 'Client_Telefon': '', 'Observatii': '',
                    'Subtotal': 0.0, 'TVA': 0.0, 'Total': 0.0, 'Suma_Primita': 0.0, 'Rest': 0.0
                })
                df = df.replace({np.nan: ''}).replace({np.nan: 0.0})

                result = df.to_dict('records')
                print(f"🧾 Bonuri fiscale încărcate: {len(result)} înregistrări")
                return jsonify(result)
            except Exception as e:
                print(f"❌ Eroare la încărcarea bonurilor fiscale: {e}")
                return jsonify([])



        # API Endpoints pentru CRUD Clienți
        @self.app.route('/api/add_client', methods=['POST'])
        def api_add_client():
            try:
                print("=== API ADD CLIENT ===")
                data = request.get_json()
                print(f"📝 Date primite: {data}")

                # Validare date
                required_fields = ['cif', 'nume', 'email', 'telefon']
                if not self.validate_input(data, required_fields):
                    return jsonify({'success': False, 'message': 'Toate câmpurile obligatorii trebuie completate'})

                # Citire date existente
                df = pd.read_excel(self.db_path, sheet_name='Clienti')

                # Verificare dacă CIF-ul există deja
                if data['cif'] in df['CIF'].values:
                    return jsonify({'success': False, 'message': 'Un client cu acest CIF există deja'})

                # Adăugare client nou
                new_client = {
                    'ID': len(df) + 1,  # Generează ID unic
                    'CIF': data['cif'],
                    'Nume': data['nume'],
                    'Client_Email': data.get('email', ''),
                    'Client_Telefon': data.get('telefon', ''),
                    'Client_Localitate': data.get('localitate', ''),
                    'Client_Judet': data.get('judet', ''),
                    'Client_Adresa': data.get('adresa', ''),
                    'Client_Cod_Postal': data.get('cod_postal', ''),
                    'Website': data.get('website', ''),
                    'Persoana_Contact': data.get('persoana_contact', ''),
                    'Observatii': data.get('observatii', ''),
                    'Sold_Curent': 0.0,
                    'Tara': 'România',
                    'Status': 'Activ'
                }

                df = pd.concat([df, pd.DataFrame([new_client])], ignore_index=True)
                self.save_excel_sheet(df, 'Clienti')

                print(f"✅ Client adăugat cu succes: {data['nume']}")
                return jsonify({'success': True, 'message': 'Clientul a fost adăugat cu succes!'})

            except Exception as e:
                print(f"❌ Eroare la adăugarea clientului: {str(e)}")
                return jsonify({'success': False, 'message': f'Eroare la adăugarea clientului: {str(e)}'})

        @self.app.route('/api/update_client/<int:client_id>', methods=['PUT'])
        def api_update_client(client_id):
            try:
                print(f"=== API UPDATE CLIENT {client_id} ===")
                data = request.get_json()
                print(f"📝 Date primite: {data}")

                # Validare date
                required_fields = ['cif', 'nume', 'email', 'telefon']
                if not self.validate_input(data, required_fields):
                    return jsonify({'success': False, 'message': 'Toate câmpurile obligatorii trebuie completate'})

                # Citire date existente
                df = pd.read_excel(self.db_path, sheet_name='Clienti')

                # Verificare dacă clientul există după ID
                client_mask = df['ID'] == client_id
                if not client_mask.any():
                    return jsonify({'success': False, 'message': 'Clientul nu a fost găsit'})

                # Verificare dacă CIF-ul există la alt client
                cif_exists = df[(df['ID'] != client_id) & (df['CIF'] == data['cif'])].shape[0] > 0
                if cif_exists:
                    return jsonify({'success': False, 'message': 'Un alt client cu acest CIF există deja'})

                # Actualizare date client
                df.loc[client_mask, 'CIF'] = data['cif']
                df.loc[client_mask, 'Nume'] = data['nume']
                df.loc[client_mask, 'Client_Email'] = data.get('email', '')
                df.loc[client_mask, 'Client_Telefon'] = data.get('telefon', '')
                df.loc[client_mask, 'Client_Localitate'] = data.get('localitate', '')
                df.loc[client_mask, 'Client_Judet'] = data.get('judet', '')
                df.loc[client_mask, 'Client_Adresa'] = data.get('adresa', '')
                df.loc[client_mask, 'Client_Cod_Postal'] = data.get('cod_postal', '')
                df.loc[client_mask, 'Website'] = data.get('website', '')
                df.loc[client_mask, 'Persoana_Contact'] = data.get('persoana_contact', '')
                df.loc[client_mask, 'Observatii'] = data.get('observatii', '')

                self.save_excel_sheet(df, 'Clienti')

                print(f"✅ Client actualizat cu succes: {data['nume']}")
                return jsonify({'success': True, 'message': 'Clientul a fost actualizat cu succes!'})

            except Exception as e:
                print(f"❌ Eroare la actualizarea clientului: {str(e)}")
                return jsonify({'success': False, 'message': f'Eroare la actualizarea clientului: {str(e)}'})

        @self.app.route('/api/delete_client/<int:client_id>', methods=['DELETE'])
        def api_delete_client(client_id):
            try:
                print(f"=== API DELETE CLIENT {client_id} ===")

                # Citire date existente
                df = pd.read_excel(self.db_path, sheet_name='Clienti')

                # Verificare dacă clientul există după ID
                client_mask = df['ID'] == client_id
                if not client_mask.any():
                    return jsonify({'success': False, 'message': 'Clientul nu a fost găsit'})

                # Ștergere client
                df = df[~client_mask].reset_index(drop=True)
                self.save_excel_sheet(df, 'Clienti')

                print(f"✅ Client șters cu succes: ID {client_id}")
                return jsonify({'success': True, 'message': 'Clientul a fost șters cu succes!'})

            except Exception as e:
                print(f"❌ Eroare la ștergerea clientului: {str(e)}")
                return jsonify({'success': False, 'message': f'Eroare la ștergerea clientului: {str(e)}'})

        # API Endpoints pentru CRUD Produse
        @self.app.route('/api/add_produs', methods=['POST'])
        def api_add_produs():
            try:
                print("=== API ADD PRODUS ===")
                data = request.get_json()
                print(f"📝 Date primite: {data}")

                # Validare date
                required_fields = ['cod', 'denumire', 'pret_vanzare']
                if not self.validate_input(data, required_fields):
                    return jsonify({'success': False, 'message': 'Toate câmpurile obligatorii trebuie completate'})

                # Citire date existente
                df = pd.read_excel(self.db_path, sheet_name='Produse')

                # Verificare dacă codul există deja
                if data['cod'] in df['Cod'].values:
                    return jsonify({'success': False, 'message': 'Un produs cu acest cod există deja'})

                # Adăugare produs nou
                new_produs = {
                    'ID': len(df) + 1,  # Generează ID unic
                    'Cod': data['cod'],
                    'Denumire': data['denumire'],
                    'Descriere': data.get('descriere', ''),
                    'Pret_Vanzare': float(data.get('pret_vanzare', 0)),
                    'Pret_Achizitie': float(data.get('pret_achizitie', 0)),
                    'Stoc': int(data.get('stoc', 0)),
                    'Stoc_Minim': int(data.get('stoc_minim', 0)),
                    'Greutate': float(data.get('greutate', 0)),
                    'Volum': float(data.get('volum', 0)),
                    'Cod_Bare': data.get('cod_bare', ''),
                    'Cod_Furnizor': data.get('cod_furnizor', ''),
                    'Furnizor': data.get('furnizor', ''),
                    'Categorie': data.get('categorie', ''),
                    'UM': data.get('um', 'buc'),
                    'TVA_Procent': data.get('tva_procent', 19),
                    'Observatii': data.get('observatii', '')
                }

                df = pd.concat([df, pd.DataFrame([new_produs])], ignore_index=True)
                self.save_excel_sheet(df, 'Produse')

                print(f"✅ Produs adăugat cu succes: {data['denumire']}")
                return jsonify({'success': True, 'message': 'Produsul a fost adăugat cu succes!'})

            except Exception as e:
                print(f"❌ Eroare la adăugarea produsului: {str(e)}")
                return jsonify({'success': False, 'message': f'Eroare la adăugarea produsului: {str(e)}'})

        @self.app.route('/api/update_produs/<int:produs_id>', methods=['PUT'])
        def api_update_produs(produs_id):
            try:
                print(f"=== API UPDATE PRODUS {produs_id} ===")
                data = request.get_json()
                print(f"📝 Date primite: {data}")

                # Validare date
                required_fields = ['cod', 'denumire', 'pret_vanzare']
                if not self.validate_input(data, required_fields):
                    return jsonify({'success': False, 'message': 'Toate câmpurile obligatorii trebuie completate'})

                # Citire date existente
                df = pd.read_excel(self.db_path, sheet_name='Produse')

                # Verificare dacă produsul există după ID
                produs_mask = df['ID'] == produs_id
                if not produs_mask.any():
                    return jsonify({'success': False, 'message': 'Produsul nu a fost găsit'})

                # Verificare dacă codul există la alt produs
                cod_exists = df[(df['ID'] != produs_id) & (df['Cod'] == data['cod'])].shape[0] > 0
                if cod_exists:
                    return jsonify({'success': False, 'message': 'Un alt produs cu acest cod există deja'})

                # Actualizare date produs
                df.loc[produs_mask, 'Cod'] = data['cod']
                df.loc[produs_mask, 'Denumire'] = data['denumire']
                df.loc[produs_mask, 'Descriere'] = data.get('descriere', '')
                df.loc[produs_mask, 'Pret_Vanzare'] = float(data.get('pret_vanzare', 0))
                df.loc[produs_mask, 'Pret_Achizitie'] = float(data.get('pret_achizitie', 0))
                df.loc[produs_mask, 'Stoc'] = int(data.get('stoc', 0))
                df.loc[produs_mask, 'Stoc_Minim'] = int(data.get('stoc_minim', 0))
                df.loc[produs_mask, 'Greutate'] = float(data.get('greutate', 0))
                df.loc[produs_mask, 'Volum'] = float(data.get('volum', 0))
                df.loc[produs_mask, 'Cod_Bare'] = data.get('cod_bare', '')
                df.loc[produs_mask, 'Cod_Furnizor'] = data.get('cod_furnizor', '')
                df.loc[produs_mask, 'Furnizor'] = data.get('furnizor', '')
                df.loc[produs_mask, 'Categorie'] = data.get('categorie', '')
                df.loc[produs_mask, 'UM'] = data.get('um', 'buc')
                df.loc[produs_mask, 'TVA_Procent'] = data.get('tva_procent', 19)
                df.loc[produs_mask, 'Observatii'] = data.get('observatii', '')

                self.save_excel_sheet(df, 'Produse')

                print(f"✅ Produs actualizat cu succes: {data['denumire']}")
                return jsonify({'success': True, 'message': 'Produsul a fost actualizat cu succes!'})

            except Exception as e:
                print(f"❌ Eroare la actualizarea produsului: {str(e)}")
                return jsonify({'success': False, 'message': f'Eroare la actualizarea produsului: {str(e)}'})

        @self.app.route('/api/delete_produs/<int:produs_id>', methods=['DELETE'])
        def api_delete_produs(produs_id):
            try:
                print(f"=== API DELETE PRODUS {produs_id} ===")

                # Citire date existente
                df = pd.read_excel(self.db_path, sheet_name='Produse')

                # Verificare dacă produsul există după ID
                produs_mask = df['ID'] == produs_id
                if not produs_mask.any():
                    return jsonify({'success': False, 'message': 'Produsul nu a fost găsit'})

                # Ștergere produs
                df = df[~produs_mask].reset_index(drop=True)
                self.save_excel_sheet(df, 'Produse')

                print(f"✅ Produs șters cu succes: ID {produs_id}")
                return jsonify({'success': True, 'message': 'Produsul a fost șters cu succes!'})

            except Exception as e:
                print(f"❌ Eroare la ștergerea produsului: {str(e)}")
                return jsonify({'success': False, 'message': f'Eroare la ștergerea produsului: {str(e)}'})

        # API Endpoints pentru Configurare

        @self.app.route('/api/save_bon_fiscal', methods=['POST'])
        def api_save_bon_fiscal():
            try:
                print("=== API SAVE BON FISCAL ===")
                data = request.get_json()
                print(f"📝 Date primite: {data}")

                # Validare date
                if not data:
                    print("❌ Nu s-au primit date")
                    return jsonify({'success': False, 'message': 'Nu s-au primit date'})

                required_fields = ['numar_bon', 'data_emitere', 'total']
                missing_fields = [field for field in required_fields if not data.get(field)]
                if missing_fields:
                    print(f"❌ Câmpuri lipsă: {missing_fields}")
                    return jsonify({'success': False, 'message': f'Câmpurile obligatorii lipsesc: {", ".join(missing_fields)}'})

                print("✅ Validare date completă")

                # Validare sume numerice
                try:
                    subtotal = float(data.get('subtotal', 0))
                    tva = float(data.get('tva', 0))
                    total = float(data.get('total', 0))
                    suma_primita = float(data.get('suma_primita', 0))
                    rest = float(data.get('rest', 0))
                    print(f"✅ Conversie numerică OK: subtotal={subtotal}, total={total}")
                except (ValueError, TypeError) as e:
                    print(f"❌ Eroare la conversie numerică: {e}")
                    return jsonify({'success': False, 'message': 'Valorile numerice sunt invalide'})

                # Verifică dacă fișierul bazei de date există
                print(f"🔍 Verific baza de date: {self.db_path}")
                if not os.path.exists(self.db_path):
                    print(f"❌ Fișierul bazei de date nu există: {self.db_path}")
                    return jsonify({'success': False, 'message': 'Baza de date nu a fost găsită'})

                print("✅ Fișierul bazei de date există")

                # Citire date existente
                print("📖 Încerc să citesc sheet-ul Bonuri_Fiscale...")
                try:
                    df = pd.read_excel(self.db_path, sheet_name='Bonuri_Fiscale')
                    print(f"✅ Sheet Bonuri_Fiscale încărcat: {len(df)} înregistrări")
                except Exception as e:
                    print(f"❌ Eroare la citirea sheet-ului: {e}")
                    return jsonify({'success': False, 'message': f'Eroare la citirea bazei de date: {str(e)}'})

                # Verificare dacă numărul bonului există deja
                print(f"🔍 Verific dacă bonul {data['numar_bon']} există deja...")
                if data['numar_bon'] in df['Numar_Bon'].values:
                    print("❌ Bonul există deja")
                    return jsonify({'success': False, 'message': 'Un bon cu acest număr există deja'})

                print("✅ Numărul bonului este unic")

                # Generare număr bon automat dacă e nevoie
                if not data.get('numar_bon') or data['numar_bon'] == 'BF-001':
                    max_id = df['ID'].max() if len(df) > 0 else 0
                    data['numar_bon'] = f"BF-{max_id + 1:03d}"
                    print(f"🔄 Număr bon generat automat: {data['numar_bon']}")

                # Adăugare bon nou
                print("📝 Creez înregistrarea nouă...")
                new_bon = {
                    'ID': len(df) + 1,
                    'Numar_Bon': data['numar_bon'],
                    'Data_Emitere': data['data_emitere'],
                    'Ora_Emitere': data.get('ora_emitere', ''),
                    'Serie_Bon': 'BF',
                    'Numar_Casa': 'CASA-001',
                    'Operator': data.get('operator', 'Operator 1'),
                    'Client_Nume': data.get('client_nume', 'Client fără nume'),
                    'Client_Email': data.get('client_email', ''),
                    'Client_Telefon': data.get('client_telefon', ''),
                    'Subtotal': subtotal,
                    'TVA': tva,
                    'Total': total,
                    'Metoda_Plata': data.get('metoda_plata', 'Numerar'),
                    'Suma_Primita': suma_primita,
                    'Rest': rest,
                    'Observatii': data.get('observatii', '')
                }

                print(f"✅ Înregistrare creată: {new_bon}")

                # Adaugă la DataFrame
                print("📊 Adaug la DataFrame...")
                try:
                    df = pd.concat([df, pd.DataFrame([new_bon])], ignore_index=True)
                    print(f"✅ DataFrame actualizat - noul număr de înregistrări: {len(df)}")
                except Exception as e:
                    print(f"❌ Eroare la adăugarea în DataFrame: {e}")
                    return jsonify({'success': False, 'message': f'Eroare la procesarea datelor: {str(e)}'})

                # Salvează în Excel
                print("💾 Încerc să salvez în Excel...")
                try:
                    self.save_excel_sheet(df, 'Bonuri_Fiscale')
                    print("✅ Salvare în Excel completă!")
                except Exception as e:
                    print(f"❌ Eroare la salvarea în Excel: {e}")
                    return jsonify({'success': False, 'message': f'Eroare la salvarea în baza de date: {str(e)}'})

                print(f"🎉 BON FISCAL SALVAT CU SUCCES: {data['numar_bon']}")
                print(f"📊 Salvat în: {self.db_path}")

                response_data = {
                    'success': True,
                    'message': 'Bon fiscal a fost emis cu succes!',
                    'bon_number': data['numar_bon']
                }
                print(f"📤 Trimit răspuns: {response_data}")

                return jsonify(response_data)

            except Exception as e:
                print(f"❌ EROARE NEAȘTEPTATĂ la salvarea bonului fiscal: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({'success': False, 'message': f'Eroare neașteptată: {str(e)}'})

        @self.app.route('/api/update_config', methods=['POST'])
        def api_update_config():
            try:
                print("=== API UPDATE CONFIG ===")
                data = request.get_json()
                print(f"📝 Date primite: {data}")

                # Validare date
                required_fields = ['company_name', 'company_cif', 'company_address']
                if not self.validate_input(data, required_fields):
                    return jsonify({'success': False, 'message': 'Toate câmpurile obligatorii trebuie completate'})

                # Citire date existente
                df = pd.read_excel(self.db_path, sheet_name='Configurare')

                # Actualizare configurare
                if len(df) > 0:
                    df.loc[0, 'Nume_Companie'] = data.get('company_name', '')
                    df.loc[0, 'CIF'] = data.get('company_cif', '')
                    df.loc[0, 'Adresa'] = data.get('company_address', '')
                    df.loc[0, 'Telefon'] = data.get('company_phone', '')
                    df.loc[0, 'Email'] = data.get('company_email', '')
                    df.loc[0, 'Website'] = data.get('company_website', '')
                    df.loc[0, 'Cont_Bancar'] = data.get('bank_account', '')
                    df.loc[0, 'Banca'] = data.get('bank_name', '')
                    df.loc[0, 'TVA'] = float(data.get('tva_rate', 19))
                    df.loc[0, 'Moneda'] = data.get('currency', 'RON')
                else:
                    # Creare configurare nouă
                    new_config = {
                        'Nume_Companie': data.get('company_name', ''),
                        'CIF': data.get('company_cif', ''),
                        'Adresa': data.get('company_address', ''),
                        'Telefon': data.get('company_phone', ''),
                        'Email': data.get('company_email', ''),
                        'Website': data.get('company_website', ''),
                        'Cont_Bancar': data.get('bank_account', ''),
                        'Banca': data.get('bank_name', ''),
                        'TVA': float(data.get('tva_rate', 19)),
                        'Moneda': data.get('currency', 'RON')
                    }
                    df = pd.DataFrame([new_config])

                self.save_excel_sheet(df, 'Configurare')

                print(f"✅ Configurare actualizată cu succes")
                return jsonify({'success': True, 'message': 'Configurarea a fost actualizată cu succes!'})

            except Exception as e:
                print(f"❌ Eroare la actualizarea configurarei: {str(e)}")
                return jsonify({'success': False, 'message': f'Eroare la actualizarea configurarei: {str(e)}'})

        @self.app.route('/api/get_config', methods=['GET'])
        def api_get_config():
            try:
                print("=== API GET CONFIG ===")

                df = pd.read_excel(self.db_path, sheet_name='Configurare')
                df = df.fillna({
                    'Nume_Companie': '', 'CIF': '', 'Adresa': '', 'Telefon': '', 'Email': '',
                    'Website': '', 'Cont_Bancar': '', 'Banca': '', 'TVA': 19, 'Moneda': 'RON'
                })
                df = df.replace({np.nan: ''}).replace({np.nan: 19})

                if len(df) > 0:
                    result = df.iloc[0].to_dict()
                else:
                    result = {
                        'Nume_Companie': '', 'CIF': '', 'Adresa': '', 'Telefon': '', 'Email': '',
                        'Website': '', 'Cont_Bancar': '', 'Banca': '', 'TVA': 19, 'Moneda': 'RON'
                    }

                print(f"✅ Configurare încărcată cu succes")
                return jsonify(result)

            except Exception as e:
                print(f"❌ Eroare la încărcarea configurarei: {str(e)}")
                return jsonify({})

        # BON FISCAL



        # Continuă cu rutele de salvare...
        # [Include all other routes from the original code]

    def generate_invoice_html(self, invoice_data):
        """Generate HTML content for invoice email"""
        html_template = f"""
        <!DOCTYPE html>
        <html lang="ro">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Factură {invoice_data['invoice_number']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 2px solid #3498db; }}
                .company-info h1 {{ color: #3498db; font-size: 28px; margin-bottom: 10px; }}
                .invoice-number {{ font-size: 24px; font-weight: bold; color: #3498db; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px; }}
                .info-box {{ background: #f8f9fa; padding: 20px; border-radius: 8px; }}
                .info-title {{ font-weight: bold; color: #3498db; margin-bottom: 15px; }}
                .totals {{ width: 50%; margin-left: auto; }}
                .total-line {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #ddd; }}
                .total-line.final {{ font-weight: bold; font-size: 18px; color: #3498db; border-bottom: 2px solid #3498db; margin-top: 10px; }}
                .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="company-info">
                    <h1>TIP B. SRL</h1>
                    <p><strong>CIF:</strong> RO12345678</p>
                    <p><strong>Adresa:</strong> Str. Exemplu, Nr. 123, București</p>
                    <p><strong>Telefon:</strong> 021 123 4567</p>
                    <p><strong>Email:</strong> office@tipb.ro</p>
                </div>
                <div>
                    <div class="invoice-number">FACTURĂ</div>
                    <div class="invoice-number">{invoice_data['invoice_number']}</div>
                </div>
            </div>

            <div class="info-grid">
                <div class="info-box">
                    <div class="info-title">Facturat către:</div>
                    <p><strong>{invoice_data['client_name']}</strong></p>
                    <p>CIF: {invoice_data['client_cif']}</p>
                    <p>Email: {invoice_data['client_email']}</p>
                    <p>Telefon: {invoice_data['client_phone']}</p>
                </div>
                <div class="info-box">
                    <div class="info-title">Detalii Factură:</div>
                    <p><strong>Data emiterii:</strong> {invoice_data['issue_date']}</p>
                    <p><strong>Data scadenței:</strong> {invoice_data['due_date']}</p>
                    <p><strong>Termeni plată:</strong> {invoice_data['payment_terms']}</p>
                </div>
            </div>

            <div class="totals">
                <div class="total-line">
                    <span>Subtotal:</span>
                    <span>{invoice_data['subtotal']:.2f} RON</span>
                </div>
                <div class="total-line">
                    <span>TVA:</span>
                    <span>{invoice_data['tva']:.2f} RON</span>
                </div>
                <div class="total-line final">
                    <span>TOTAL DE PLATĂ:</span>
                    <span>{invoice_data['total']:.2f} RON</span>
                </div>
            </div>

            <div class="footer">
                <p>Mulțumim pentru încredere!</p>
                <p>Această factură a fost generată electronic de SmartBill.</p>
            </div>
        </body>
        </html>
        """
        return html_template

    def generate_storno_html(self, storno_data):
        """Generate HTML content for storno invoice email"""
        html_template = f"""
        <!DOCTYPE html>
        <html lang="ro">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Factură Storno pentru {storno_data['original_invoice']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 2px solid #e74c3c; }}
                .company-info h1 {{ color: #e74c3c; font-size: 28px; margin-bottom: 10px; }}
                .storno-number {{ font-size: 24px; font-weight: bold; color: #e74c3c; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px; }}
                .info-box {{ background: #f8f9fa; padding: 20px; border-radius: 8px; }}
                .info-title {{ font-weight: bold; color: #e74c3c; margin-bottom: 15px; }}
                .storno-reason {{ background: #ffe6e6; padding: 20px; border-radius: 8px; border-left: 4px solid #e74c3c; margin-bottom: 30px; }}
                .comparison-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
                .comparison-table th {{ background: #e74c3c; color: white; padding: 15px; text-align: left; }}
                .comparison-table td {{ padding: 12px 15px; border-bottom: 1px solid #ddd; }}
                .comparison-table tr:nth-child(even) {{ background: #f8f9fa; }}
                .positive-value {{ color: #27ae60; }}
                .negative-value {{ color: #e74c3c; }}
                .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 15px; border-radius: 8px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="company-info">
                    <h1>TIP B. SRL</h1>
                    <p><strong>CIF:</strong> RO12345678</p>
                    <p><strong>Adresa:</strong> Str. Exemplu, Nr. 123, București</p>
                </div>
                <div>
                    <div class="storno-number">FACTURĂ STORNO</div>
                    <div class="storno-number">STORN-{storno_data['storno_id']}</div>
                </div>
            </div>

            <div class="info-grid">
                <div class="info-box">
                    <div class="info-title">Client:</div>
                    <p><strong>{storno_data['client_name']}</strong></p>
                    <p>CIF: {storno_data['client_cif']}</p>
                    <p>Email: {storno_data['client_email']}</p>
                </div>
                <div class="info-box">
                    <div class="info-title">Detalii Storno:</div>
                    <p><strong>Factură originală:</strong> {storno_data['original_invoice']}</p>
                    <p><strong>Data storno:</strong> {storno_data['storno_date']}</p>
                    <p><strong>Motiv:</strong> {storno_data['reason']}</p>
                </div>
            </div>

            <div class="storno-reason">
                <div class="info-title">Motiv Storno:</div>
                <p><strong>{storno_data['reason']}</strong></p>
                {f"<p>{storno_data['notes']}</p>" if storno_data.get('notes') else ''}
            </div>

            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Tip Valoare</th>
                        <th>Subtotal</th>
                        <th>TVA</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Valori Originale</strong></td>
                        <td class="positive-value">{storno_data['original_subtotal']:.2f} RON</td>
                        <td class="positive-value">{storno_data['original_tva']:.2f} RON</td>
                        <td class="positive-value">{storno_data['original_total']:.2f} RON</td>
                    </tr>
                    <tr>
                        <td><strong>Valori Storno</strong></td>
                        <td class="negative-value">{storno_data['storno_subtotal']:.2f} RON</td>
                        <td class="negative-value">{storno_data['storno_tva']:.2f} RON</td>
                        <td class="negative-value">{storno_data['storno_total']:.2f} RON</td>
                    </tr>
                </tbody>
            </table>

            <div class="warning">
                <strong>⚠️ ATENȚIE:</strong> Această factură storno anulează complet factura originală {storno_data['original_invoice']}.
            </div>

            <div class="footer">
                <p>Pentru orice întrebări, vă rugăm să ne contactați.</p>
                <p>Factură storno generată electronic de SmartBill.</p>
            </div>
        </body>
        </html>
        """
        return html_template

    def get_stats(self):
        """Calculează statisticile pentru dashboard"""
        try:
            facturi_df = pd.read_excel(self.db_path, sheet_name='Facturi')
            clienti_df = pd.read_excel(self.db_path, sheet_name='Clienti')
            produse_df = pd.read_excel(self.db_path, sheet_name='Produse')

            vanzari = float(facturi_df['Total'].sum())
            facturi_neincasate = len(facturi_df[facturi_df['Status'] == 'Neplatita'])
            sold_clienti = float(clienti_df['Sold_Curent'].sum())
            total_facturi = len(facturi_df)
            total_clienti = len(clienti_df)
            total_produse = len(produse_df)
            total_incasari = vanzari  # Pentru dashboard

            print(f"📊 Statistici calculate: Vânzări={vanzari}, Facturi neîncasate={facturi_neincasate}, Sold clienți={sold_clienti}")

            return {
                'vanzari': vanzari,
                'facturi_neincasate': facturi_neincasate,
                'sold_clienti': sold_clienti,
                'cheltuieli': 4704.00,
                'total_facturi': total_facturi,
                'total_clienti': total_clienti,
                'total_produse': total_produse,
                'total_incasari': total_incasari
            }
        except Exception as e:
            print(f"❌ Eroare la calcularea statisticilor: {e}")
            return {
                'vanzari': 11769.70,
                'facturi_neincasate': 2,
                'sold_clienti': 7497.60,
                'cheltuieli': 4704.00,
                'total_facturi': 10,
                'total_clienti': 16,
                'total_produse': 16,
                'total_incasari': 11769.70
            }

    def run(self):
        """Pornește aplicația"""
        print("="*60)
        print("🚀 SMARTBILL APLICAȚIA PORNEȘTE!")
        print("="*60)
        print("🌐 URL: http://localhost:5000")
        print("📊 Dashboard: http://localhost:5000/dashboard")
        print("📄 Factură: http://localhost:5000/factura")
        print("👥 Clienți: http://localhost:5000/clienti")
        print("📦 Produse: http://localhost:5000/produse")
        print("🔄 Factură Storno: http://localhost:5000/factura-storno")
        print("="*60)
        print("🔒 DATELE VOR FI PĂSTRATE PERMANENT ÎN EXCEL!")
        print("="*60)

        # Deschide browserul după 3 secunde pentru a da timp aplicației să pornească
        def open_browser():
            try:
                webbrowser.open('http://localhost:5000')
                print("✅ Browser deschis automat!")
            except Exception as e:
                print(f"⚠️ Nu s-a putut deschide browserul automat: {e}")
                print("🌐 Deschide manual: http://localhost:5000")

        # Endpoint de test pentru a verifica dacă serverul funcționează
        @self.app.route('/api/test', methods=['GET'])
        def api_test():
            print("🧪 === ENDPOINT TEST APELAT ===")
            return jsonify({
                'success': True,
                'message': 'API SmartBill funcționează!',
                'timestamp': str(datetime.now()),
                'version': '1.0'
            })

        # Endpoint pentru verificarea structurii bazei de date Excel
        @self.app.route('/api/db_info', methods=['GET'])
        def api_db_info():
            try:
                # Verifică dacă fișierul Excel există
                if not os.path.exists(self.db_path):
                    return jsonify({
                        'success': False,
                        'message': f'Fișierul bazei de date nu există: {self.db_path}'
                    }), 500
                
                # Citește structura fișierului Excel
                with pd.ExcelFile(self.db_path) as excel_file:
                    sheet_names = excel_file.sheet_names
                
                table_info = {}
                for sheet_name in sheet_names:
                    try:
                        df = pd.read_excel(self.db_path, sheet_name=sheet_name)
                        columns = [{'name': col, 'type': str(df[col].dtype)} for col in df.columns]
                        row_count = len(df)
                        
                        table_info[sheet_name] = {
                            'columns': columns,
                            'row_count': row_count
                        }
                    except Exception as e:
                        table_info[sheet_name] = {
                            'columns': [],
                            'row_count': 0,
                            'error': str(e)
                        }
                
                return jsonify({
                    'success': True,
                    'tables': table_info,
                    'file_path': self.db_path
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': str(e)
                }), 500

        # API endpoint pentru căutarea facturilor - versiunea pentru Excel
        @self.app.route('/api/search_facturi', methods=['POST'])
        def api_search_facturi():
            print("🔍 === ENDPOINT SEARCH_FACTURI APELAT ===")
            
            try:
                # Verifică dacă request-ul are JSON
                if not request.is_json:
                    print("❌ Request-ul nu este JSON")
                    return jsonify({
                        'success': False,
                        'message': 'Request-ul trebuie să fie JSON'
                    }), 400
                
                data = request.get_json()
                print(f"🔍 Date primite: {data}")
                
                # Verifică dacă fișierul Excel există
                if not os.path.exists(self.db_path):
                    print(f"❌ Fișierul Excel nu există: {self.db_path}")
                    return jsonify({
                        'success': False,
                        'message': f'Fișierul bazei de date nu există: {self.db_path}'
                    }), 500
                
                # Citește datele din Excel în loc de SQLite
                print(f"📖 Citesc datele din Excel: {self.db_path}")
                try:
                    df = pd.read_excel(self.db_path, sheet_name='Facturi')
                    print(f"📊 Facturile citite: {len(df)} rânduri")
                    print(f"📊 Coloane disponibile: {list(df.columns)}")
                except Exception as e:
                    print(f"❌ Eroare la citirea din Excel: {e}")
                    return jsonify({
                        'success': False,
                        'message': f'Eroare la citirea din Excel: {str(e)}'
                    }), 500
                # Aplică filtrele pe DataFrame
                filtered_df = df.copy()
                
                print(f"📊 Date demo disponibile în Facturi:")
                print(f"    - Numere facturi: {df['Numar_Factura'].tolist()[:5] if 'Numar_Factura' in df.columns else 'N/A'}")
                print(f"    - Total facturi: {len(df)}")
                
                if data.get('invoice_number'):
                    if 'Numar_Factura' in df.columns:
                        print(f"🔍 Caut factura cu numărul: '{data['invoice_number']}'")
                        print(f"📋 Facturi disponibile: {df['Numar_Factura'].tolist()}")
                        
                        # Încearcă căutare exactă mai întâi
                        exact_match = filtered_df[filtered_df['Numar_Factura'].astype(str) == data['invoice_number']]
                        if len(exact_match) > 0:
                            filtered_df = exact_match
                            print(f"✅ Găsit match exact pentru: {data['invoice_number']}")
                        else:
                            # Încearcă căutare parțială
                            filtered_df = filtered_df[filtered_df['Numar_Factura'].astype(str).str.contains(data['invoice_number'], case=False, na=False)]
                            print(f"🔍 Căutare parțială pentru: {data['invoice_number']} → {len(filtered_df)} rezultate")
                        
                        print(f"🔍 Filtru număr factură: {data['invoice_number']} → {len(filtered_df)} rezultate")
                
                if data.get('client_name'):
                    if 'Client_Nume' in df.columns:
                        filtered_df = filtered_df[filtered_df['Client_Nume'].astype(str).str.contains(data['client_name'], case=False, na=False)]
                        print(f"🔍 Filtru nume client: {data['client_name']} → {len(filtered_df)} rezultate")
                
                if data.get('client_cif'):
                    if 'Client_CIF' in df.columns:
                        filtered_df = filtered_df[filtered_df['Client_CIF'].astype(str).str.contains(data['client_cif'], case=False, na=False)]
                        print(f"🔍 Filtru CIF: {data['client_cif']} → {len(filtered_df)} rezultate")
                
                if data.get('date_from'):
                    if 'Data_Emitere' in df.columns:
                        try:
                            date_from = pd.to_datetime(data['date_from'])
                            filtered_df['Data_Emitere_Parsed'] = pd.to_datetime(filtered_df['Data_Emitere'], errors='coerce')
                            filtered_df = filtered_df[filtered_df['Data_Emitere_Parsed'] >= date_from]
                            print(f"🔍 Filtru dată de la: {data['date_from']} → {len(filtered_df)} rezultate")
                        except Exception as e:
                            print(f"⚠️ Eroare parsare dată 'from': {e}")
                
                if data.get('date_to'):
                    if 'Data_Emitere' in df.columns:
                        try:
                            date_to = pd.to_datetime(data['date_to'])
                            if 'Data_Emitere_Parsed' not in filtered_df.columns:
                                filtered_df['Data_Emitere_Parsed'] = pd.to_datetime(filtered_df['Data_Emitere'], errors='coerce')
                            filtered_df = filtered_df[filtered_df['Data_Emitere_Parsed'] <= date_to]
                            print(f"🔍 Filtru dată până la: {data['date_to']} → {len(filtered_df)} rezultate")
                        except Exception as e:
                            print(f"⚠️ Eroare parsare dată 'to': {e}")
                
                if data.get('status'):
                    if 'Status' in df.columns:
                        status_search = data['status'].lower()
                        filtered_df = filtered_df[filtered_df['Status'].astype(str).str.lower().str.contains(status_search, case=False, na=False)]
                        print(f"🔍 Filtru status: {data['status']} → {len(filtered_df)} rezultate")
                
                if data.get('min_amount'):
                    if 'Total' in df.columns:
                        try:
                            min_amount = float(data['min_amount'])
                            filtered_df = filtered_df[pd.to_numeric(filtered_df['Total'], errors='coerce') >= min_amount]
                            print(f"🔍 Filtru sumă minimă: {data['min_amount']} → {len(filtered_df)} rezultate")
                        except Exception as e:
                            print(f"⚠️ Eroare parsare sumă minimă: {e}")
                
                if data.get('max_amount'):
                    if 'Total' in df.columns:
                        try:
                            max_amount = float(data['max_amount'])
                            filtered_df = filtered_df[pd.to_numeric(filtered_df['Total'], errors='coerce') <= max_amount]
                            print(f"🔍 Filtru sumă maximă: {data['max_amount']} → {len(filtered_df)} rezultate")
                        except Exception as e:
                            print(f"⚠️ Eroare parsare sumă maximă: {e}")
                
                # Sortează după data emiterii (cele mai recente primul)
                if 'Data_Emitere' in filtered_df.columns:
                    filtered_df = filtered_df.sort_values('Data_Emitere', ascending=False)
                
                # Limitează rezultatele la 100
                filtered_df = filtered_df.head(100)
                
                print(f"🔍 Rezultate finale: {len(filtered_df)} facturi")
                
                # Convertește rezultatele în format JSON
                facturi = []
                for index, row in filtered_df.iterrows():
                    factura_dict = {
                        'id': int(row.get('ID', index + 1)) if pd.notna(row.get('ID')) else index + 1,
                        'numar_factura': str(row.get('Numar_Factura', '')) if pd.notna(row.get('Numar_Factura')) else '',
                        'data_emitere': str(row.get('Data_Emitere', '')) if pd.notna(row.get('Data_Emitere')) else '',
                        'data_scadenta': str(row.get('Data_Scadenta', '')) if pd.notna(row.get('Data_Scadenta')) else '',
                        'client_nume': str(row.get('Client_Nume', '')) if pd.notna(row.get('Client_Nume')) else '',
                        'client_cif': str(row.get('Client_CIF', '')) if pd.notna(row.get('Client_CIF')) else '',
                        'client_email': str(row.get('Client_Email', '')) if pd.notna(row.get('Client_Email')) else '',
                        'client_telefon': str(row.get('Client_Telefon', '')) if pd.notna(row.get('Client_Telefon')) else '',
                        'subtotal': float(row.get('Subtotal', 0)) if pd.notna(row.get('Subtotal')) else 0.0,
                        'tva': float(row.get('TVA', 0)) if pd.notna(row.get('TVA')) else 0.0,
                        'total': float(row.get('Total', 0)) if pd.notna(row.get('Total')) else 0.0,
                        'status': str(row.get('Status', 'Emisa')) if pd.notna(row.get('Status')) else 'Emisa',
                        'observatii': str(row.get('Observatii', '')) if pd.notna(row.get('Observatii')) else ''
                    }
                    facturi.append(factura_dict)
                
                print(f"✅ Returnez {len(facturi)} facturi")
                
                response = jsonify({
                    'success': True,
                    'data': facturi,
                    'count': len(facturi)
                })
                response.headers['Content-Type'] = 'application/json'
                return response
                
            except Exception as e:
                import traceback
                print(f"❌ Eroare la căutarea facturilor: {e}")
                print(f"❌ Traceback: {traceback.format_exc()}")
                return jsonify({
                    'success': False,
                    'message': f'Eroare la căutarea facturilor: {str(e)}',
                    'error_type': type(e).__name__
                }), 500

        threading.Timer(3, open_browser).start()

        # Pornește Flask cu debug activat pentru a rămâne în execuție
        self.app.run(debug=True, host='0.0.0.0', port=5000, threaded=True, use_reloader=False)

if __name__ == "__main__":
    app = SmartBillApp()
    app.run()