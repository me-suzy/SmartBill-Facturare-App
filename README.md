# 💰 SmartBill - Aplicație de Facturare

Aplicație completă de facturare dezvoltată în Flask cu interfață modernă, backend Excel, și funcționalități avansate pentru gestionarea afacerii.

## 🚀 Caracteristici Principale

### 📊 **Dashboard Complet**
- **Statistici în timp real**: vânzări totale, facturi neîncasate, sold clienți
- **Grafice interactive**: evoluția vânzărilor, top clienți, analiza produselor
- **Indicatori KPI**: performanța lunară și anuală
- **Quick actions**: acces rapid la funcționalitățile principale

### 📄 **Sistem de Facturare Avansat**
- **Emitere facturi**: cu calcule automate TVA (19%)
- **Facturi Storno**: anularea facturilor cu motiv și validări
- **Bonuri fiscale**: pentru tranzacții rapide
- **Căutare inteligentă**: după număr, client, sau perioadă

### 👥 **Gestionare Clienți**
- **Baza de date completa**: nume, CIF, contact, adrese
- **Istoric facturi**: toate tranzacțiile pe client
- **Import/Export**: CSV, Excel pentru integrări
- **Validări CIF**: format românesc

### 📦 **Catalogul de Produse**
- **Produse și servicii**: descrieri, prețuri, stocuri
- **Categorii**: organizare ierarhică
- **Prețuri cu TVA**: calcule automate
- **Coduri de bare**: scanare și identificare

### 📈 **Rapoarte Detaliate**
- **Vânzări pe perioade**: zilnic, lunar, anual
- **Analize clienți**: top cumpărători, sold datorii
- **Inventar produse**: stocuri, rotație, profitabilitate
- **Export**: PDF, Excel pentru contabilitate

### ⚙️ **Configurări Avansate**
- **Date firmă**: completarea automată a facturilor
- **TVA și taxe**: rate configurabile
- **Template-uri**: personalizarea facturilor
- **Backup automat**: protecția datelor

## 🛠️ Tehnologii Utilizate

### Backend
- **Flask**: Framework web Python
- **Pandas**: Procesarea datelor Excel
- **OpenPyXL**: Manipularea fișierelor Excel
- **Jinja2**: Template engine pentru HTML

### Frontend
- **HTML5/CSS3**: Interfață modernă și responsivă
- **JavaScript/jQuery**: Interactivitate și AJAX
- **Toastr**: Notificări user-friendly
- **Responsive Design**: Compatible mobile/desktop

### Baza de Date
- **Excel Workbook**: `smartbill_database.xlsx`
- **Sheet-uri**: Facturi, Clienți, Produse, Bonuri, Storno, Configurări
- **Backup automat**: Protecție față de pierderea datelor

## 📋 Instalare și Configurare

### 1. Cerințe de Sistem
```bash
Python 3.8+
Windows/Linux/MacOS
```

### 2. Instalare Dependențe
```bash
pip install -r requirements.txt
```

### 3. Pornire Aplicație
```bash
# Metoda 1 - Direct
python app.py

# Metoda 2 - Script helper
python run_app.py

# Metoda 3 - Batch file (Windows)
RUN_SMARTBILL.bat
```

### 4. Acces la Aplicație
```
URL Principal: http://localhost:5000
Dashboard: http://localhost:5000/dashboard
Facturi: http://localhost:5000/factura
Clienți: http://localhost:5000/clienti
```

## 📁 Structura Proiectului

```
SmartBillLikeApp/
├── 📄 app.py                 # Aplicația principală Flask
├── 📄 run_app.py            # Script de pornire
├── 📄 requirements.txt      # Dependențe Python
├── 📄 RUN_SMARTBILL.bat    # Launcher Windows
│
├── 📁 database/
│   ├── smartbill_database.xlsx      # Baza de date principală
│   ├── generate_excel.py            # Generator date demo
│   └── *.backup_*                   # Backup-uri automate
│
├── 📁 templates/
│   ├── dashboard.html               # Dashboard principal
│   ├── factura.html                # Emitere facturi
│   ├── factura-storno.html         # Facturi storno
│   ├── clienti.html                # Gestionare clienți
│   ├── produse.html                # Catalogul produse
│   ├── bon_fiscal.html             # Bonuri fiscale
│   ├── rapoarte.html               # Rapoarte și analize
│   └── configurare.html            # Setări aplicație
│
├── 📁 static/
│   ├── css/style.css               # Stiluri principale
│   └── js/
│       ├── main.js                 # JavaScript comun
│       └── factura.js              # Logic facturare
│
└── 📁 Coduri Python/              # Module auxiliare
    ├── SmartBill_Application_START.py
    ├── SmartBill_Structure_Creator.py
    └── SmartBill_Launcher_FINAL.py
```

## 🎯 Funcționalități Detaliate

### Emitere Facturi
1. **Selectare client** din baza de date
2. **Adăugare produse** cu cantități și prețuri
3. **Calcule automate**: subtotal, TVA 19%, total
4. **Validări complete**: date obligatorii, format CIF
5. **Generare PDF**: factură printabilă
6. **Trimitere email**: direct către client

### Facturi Storno
1. **Căutare factură originală** după număr
2. **Validare existență** în baza de date
3. **Populare automată**: client, valori financiare
4. **Selectare motiv**: din listă predefinită
5. **Calcule storno**: valori negative pentru anulare
6. **Documentare completă**: istoric și justificări

### Gestionare Clienți
1. **Adăugare rapid**: formular simplificat
2. **Validare CIF**: verificare format românesc
3. **Istoric complet**: toate facturile clientului
4. **Contact info**: email, telefon, adrese
5. **Import masiv**: din Excel/CSV
6. **Export date**: pentru backup sau integrări

### Catalogul Produse
1. **Categorii**: organizare ierarhică
2. **Prețuri flexibile**: cu sau fără TVA
3. **Gestionare stoc**: intrări, ieșiri, sold curent
4. **Coduri bare**: identificare rapidă
5. **Imagini produse**: vizualizare în facturi
6. **Rapoarte stoc**: analize profitabilitate

## 📊 API Endpoints

### Facturi
```
GET  /api/get_facturi          # Lista toate facturile
POST /api/save_factura         # Salvează factură nouă
POST /api/search_facturi       # Căutare după criterii
```

### Clienți
```
GET  /api/get_clienti          # Lista toți clienții
POST /api/save_client          # Adaugă client nou
PUT  /api/update_client/:id    # Actualizează client
```

### Produse
```
GET  /api/get_produse          # Catalogul complet
POST /api/save_produs          # Produs nou
PUT  /api/update_produs/:id    # Actualizare produs
```

### Storno
```
GET  /api/get_facturi_storno   # Lista facturi storno
POST /api/save_factura_storno  # Emite factură storno
```

## 🔧 Configurare Avansată

### Personalizare Firmă
```python
# În app.py sau configurare.html
COMPANY_INFO = {
    "name": "TIP B. SRL",
    "cif": "RO12345678",
    "address": "Str. Exemplu, Nr. 123, București",
    "phone": "021 123 4567",
    "email": "office@tipb.ro"
}
```

### Rate TVA
```python
# Taxa pe valoarea adăugată
TVA_STANDARD = 0.19  # 19%
TVA_REDUS = 0.09     # 9%
TVA_ZERO = 0.00      # 0%
```

### Backup Automat
- **Frecvență**: La fiecare modificare importantă
- **Format**: `smartbill_database.xlsx.backup_YYYYMMDD_HHMMSS`
- **Locație**: Folderul `database/`
- **Retenție**: Ultimele 10 backup-uri

## 🚀 Dezvoltare și Contribuții

### Mediu de Dezvoltare
```bash
# Clone repository
git clone https://github.com/your-username/SmartBill-Facturare-App.git

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python app.py
```

### Structura pentru Contribuții
1. **Fork** repository-ul
2. **Create branch** pentru feature nou
3. **Implementează** modificările
4. **Testează** toate funcționalitățile
5. **Submit pull request** cu descriere detaliată

### Testare
```bash
# Testează API endpoints
python test_api.py

# Testează formulare
python test_forms.py

# Verifică baza de date
python database/generate_excel.py
```

## 🏆 Avantaje Cheie

- **🔄 Simplu de folosit**: Interfață intuitivă pentru utilizatori non-tehnici
- **💾 Date sigure**: Backup automat și protecție față de pierderi
- **📱 Responsive**: Funcționează pe desktop, tablet, și mobile
- **⚡ Performant**: Procesare rapidă chiar și cu mii de facturi
- **🔧 Configurabil**: Adaptabil pentru diverse tipuri de business
- **📈 Scalabil**: Suportă creșterea business-ului

## 🆘 Suport și Documentație

### Probleme Comune

**Aplicația nu pornește:**
```bash
# Verifică dependențele
pip install -r requirements.txt

# Rulează diagnostic
python -c "import flask, pandas, openpyxl; print('OK')"
```

**Erori în baza de date:**
```bash
# Regenerează baza de date
python database/generate_excel.py
```

**Probleme de permisiuni:**
- Rulează ca Administrator (Windows)
- Verifică permisiunile folderului aplicației

### Loguri și Debug
- **Console output**: Toate operațiile sunt loggate
- **Fișiere erori**: Salvate automat în caz de probleme
- **Debug mode**: Activat prin variabila `debug=True`

### Contact și Suport
- **Issues**: Raportează bug-uri prin GitHub Issues
- **Features**: Sugerează îmbunătățiri prin Pull Requests
- **Documentație**: README.md și comentariile din cod

---

**📞 Ai nevoie de ajutor?** Verifică logs-urile din consolă pentru informații detaliate despre erori.

**🔄 Actualizări**: Aplicația este menținută activ și îmbunătățită pe baza feedback-ului utilizatorilor.

**⭐ Ți-a fost utilă aplicația?** Lasă un star pe GitHub și distribuie către alți antreprenori!
