import os
import sys
import subprocess
import threading
import time
import webbrowser
from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
from datetime import datetime
import json

class SmartBillApp:
    def __init__(self):
        self.app = Flask(__name__,
                        template_folder='templates',
                        static_folder='static')
        self.setup_routes()
        self.create_database()

    def create_folder_structure(self):
        """Creează structura de foldere și fișiere"""
        base_path = "d:/SmartBillLikeApp"

        folders = [
            base_path,
            f"{base_path}/templates",
            f"{base_path}/static",
            f"{base_path}/static/css",
            f"{base_path}/static/js",
            f"{base_path}/static/images",
            f"{base_path}/database",
            f"{base_path}/reports"
        ]

        for folder in folders:
            os.makedirs(folder, exist_ok=True)

        return base_path

    def create_database(self):
        """Creează baza de date Excel"""
        base_path = self.create_folder_structure()

        # Factuni
        facturi_data = {
            'ID': [],
            'Numar_Factura': [],
            'Data_Emitere': [],
            'Client_CIF': [],
            'Client_Nume': [],
            'Valoare_Totala': [],
            'TVA': [],
            'Status': [],
            'Data_Scadenta': []
        }

        # Clienti
        clienti_data = {
            'ID': [],
            'CIF': [],
            'Nume': [],
            'Adresa': [],
            'Telefon': [],
            'Email': [],
            'Sold_Curent': []
        }

        # Produse
        produse_data = {
            'ID': [],
            'Cod': [],
            'Denumire': [],
            'UM': [],
            'Pret_Unitar': [],
            'TVA_Procent': [],
            'Categorie': []
        }

        # Cheltuieli
        cheltuieli_data = {
            'ID': [],
            'Data': [],
            'Furnizor': [],
            'Descriere': [],
            'Valoare': [],
            'TVA': [],
            'Categorie': []
        }

        # Salvează în Excel
        with pd.ExcelWriter(f"{base_path}/database/smartbill_database.xlsx") as writer:
            pd.DataFrame(facturi_data).to_excel(writer, sheet_name='Facturi', index=False)
            pd.DataFrame(clienti_data).to_excel(writer, sheet_name='Clienti', index=False)
            pd.DataFrame(produse_data).to_excel(writer, sheet_name='Produse', index=False)
            pd.DataFrame(cheltuieli_data).to_excel(writer, sheet_name='Cheltuieli', index=False)

    def setup_routes(self):
        """Configurează rutele Flask"""

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/dashboard')
        def dashboard():
            stats = self.get_dashboard_stats()
            return render_template('dashboard.html', stats=stats)

        @self.app.route('/factura')
        def factura():
            return render_template('factura.html')

        @self.app.route('/bon-fiscal')
        def bon_fiscal():
            return render_template('bon_fiscal.html')

        @self.app.route('/factura-storno')
        def factura_storno():
            return render_template('factura_storno.html')

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

        # API Routes
        @self.app.route('/api/save_factura', methods=['POST'])
        def save_factura():
            data = request.get_json()
            success = self.save_to_database('Facturi', data)
            return jsonify({'success': success})

        @self.app.route('/api/get_clienti')
        def get_clienti():
            data = self.load_from_database('Clienti')
            return jsonify(data.to_dict('records') if not data.empty else [])

        @self.app.route('/api/get_produse')
        def get_produse():
            data = self.load_from_database('Produse')
            return jsonify(data.to_dict('records') if not data.empty else [])

    def get_dashboard_stats(self):
        """Calculează statisticile pentru dashboard"""
        try:
            facturi = self.load_from_database('Facturi')
            cheltuieli = self.load_from_database('Cheltuieli')
            clienti = self.load_from_database('Clienti')

            vanzari = facturi['Valoare_Totala'].sum() if not facturi.empty else 7618
            cheltuieli_total = cheltuieli['Valoare'].sum() if not cheltuieli.empty else 4704
            sold_clienti = clienti['Sold_Curent'].sum() if not clienti.empty else 0

            return {
                'vanzari': vanzari,
                'cheltuieli': cheltuieli_total,
                'sold_clienti': sold_clienti,
                'facturi_neincasate': len(facturi[facturi['Status'] == 'Neincasata']) if not facturi.empty else 0
            }
        except:
            return {
                'vanzari': 7618,
                'cheltuieli': 4704,
                'sold_clienti': 0,
                'facturi_neincasate': 0
            }

    def load_from_database(self, sheet_name):
        """Încarcă date din Excel"""
        try:
            base_path = "d:/SmartBillLikeApp"
            return pd.read_excel(f"{base_path}/database/smartbill_database.xlsx", sheet_name=sheet_name)
        except:
            return pd.DataFrame()

    def save_to_database(self, sheet_name, data):
        """Salvează date în Excel"""
        try:
            base_path = "d:/SmartBillLikeApp"
            file_path = f"{base_path}/database/smartbill_database.xlsx"

            # Încarcă datele existente
            existing_data = pd.read_excel(file_path, sheet_name=sheet_name)

            # Adaugă noile date
            new_row = pd.DataFrame([data])
            updated_data = pd.concat([existing_data, new_row], ignore_index=True)

            # Salvează înapoi
            with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
                updated_data.to_excel(writer, sheet_name=sheet_name, index=False)

            return True
        except Exception as e:
            print(f"Eroare la salvare: {e}")
            return False

    def create_html_files(self):
        """Creează toate fișierele HTML"""
        base_path = "d:/SmartBillLikeApp"

        # Index.html cu loader
        index_html = '''<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartBill - Loading</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div id="loader">
        <div class="loader-content">
            <div class="loader-spinner"></div>
            <h2>SmartBill</h2>
            <p>Se încarcă aplicația...</p>
        </div>
    </div>

    <script>
        setTimeout(function() {
            window.location.href = '/dashboard';
        }, 3000);
    </script>
</body>
</html>'''

        # Dashboard.html
        dashboard_html = '''<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartBill - Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="logo">
                <h2>SmartBill</h2>
                <span>FACTURARE</span>
            </div>
            <nav class="nav-menu">
                <a href="/dashboard" class="nav-item active">
                    <span>📊</span> Dashboard
                </a>
                <div class="nav-group">
                    <span class="nav-title">📄 Emitere</span>
                    <a href="/factura" class="nav-subitem">Factură</a>
                    <a href="/bon-fiscal" class="nav-subitem">Bon Fiscal</a>
                    <a href="/factura-storno" class="nav-subitem">Factură Storno</a>
                </div>
                <a href="/rapoarte" class="nav-item">
                    <span>📈</span> Rapoarte
                </a>
                <a href="/configurare" class="nav-item">
                    <span>⚙️</span> Configurare
                </a>
                <div class="nav-group">
                    <span class="nav-title">📝 Nomenclatoare</span>
                    <a href="/produse" class="nav-subitem">Produse</a>
                    <a href="/clienti" class="nav-subitem">Clienți</a>
                </div>
            </nav>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <header>
                <h1>Dashboard</h1>
                <div class="user-info">
                    <span>TIP B. SRL</span>
                </div>
            </header>

            <div class="dashboard-grid">
                <div class="stat-card">
                    <h3>VÂNZĂRI</h3>
                    <div class="stat-value">{{ stats.vanzari }}</div>
                    <button class="btn-primary">Emite factură</button>
                </div>

                <div class="stat-card">
                    <h3>SOLD CLIENȚI</h3>
                    <div class="stat-value">{{ stats.sold_clienti }}</div>
                    <button class="btn-primary">Emite factură</button>
                </div>

                <div class="stat-card">
                    <h3>FACTURI NEÎNCASATE</h3>
                    <div class="stat-value">{{ stats.facturi_neincasate }}</div>
                    <button class="btn-primary">Emite factură</button>
                </div>

                <div class="stat-card">
                    <h3>CHELTUIELI</h3>
                    <div class="stat-value">{{ stats.cheltuieli }}</div>
                    <button class="btn-primary">Adaugă cheltuială</button>
                </div>

                <div class="stat-card">
                    <h3>SUME DE PLĂTIT</h3>
                    <div class="stat-value">1467</div>
                    <button class="btn-primary">Adaugă cheltuială</button>
                </div>

                <div class="activity-card">
                    <h3>ACTIVITATE</h3>
                    <div class="activity-list">
                        <div class="activity-item">
                            <span>Adăugare utilizator Făntănaru Neculai</span>
                            <small>ieri, 29 iul, ora 23:59</small>
                        </div>
                        <div class="activity-item">
                            <span>Creare companie TIP B. SRL</span>
                            <small>Făntănaru Neculai - ieri, 29 iul, ora 23:59</small>
                        </div>
                    </div>
                </div>

                <div class="stat-card">
                    <h3>SOLD CASA</h3>
                    <p>Setează soldul inițial, astfel încât soldul de casă să poată fi calculat.</p>
                    <button class="btn-primary">Setează soldul inițial</button>
                </div>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>'''

        # Salvează fișierele HTML
        files_to_create = {
            f"{base_path}/templates/index.html": index_html,
            f"{base_path}/templates/dashboard.html": dashboard_html,
        }

        for file_path, content in files_to_create.items():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def create_additional_pages(self):
        """Creează paginile HTML suplimentare"""
        base_path = "d:/SmartBillLikeApp"

        # Pagina Factură
        factura_html = '''<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartBill - Factură</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <!-- Include sidebar -->
        <div class="sidebar">
            <div class="logo">
                <h2>SmartBill</h2>
                <span>FACTURARE</span>
            </div>
            <nav class="nav-menu">
                <a href="/dashboard" class="nav-item">📊 Dashboard</a>
                <div class="nav-group">
                    <span class="nav-title">📄 Emitere</span>
                    <a href="/factura" class="nav-subitem active">Factură</a>
                    <a href="/bon-fiscal" class="nav-subitem">Bon Fiscal</a>
                </div>
                <a href="/rapoarte" class="nav-item">📈 Rapoarte</a>
                <a href="/configurare" class="nav-item">⚙️ Configurare</a>
            </nav>
        </div>

        <div class="main-content">
            <header>
                <h1>Emitere › Factură</h1>
            </header>

            <div class="form-container">
                <form id="facturaForm">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Nume sau CIF/CNP</label>
                            <input type="text" id="clientCIF" placeholder="Cif pt. firme/CNP dacă sunt semnul minus între caractere">
                            <button type="button" id="addClient">+ Adaugă Client</button>
                        </div>

                        <div class="form-group">
                            <label>Data emiterii</label>
                            <input type="date" id="dataEmitere" value="{{ datetime.now().strftime('%Y-%m-%d') }}">
                        </div>

                        <div class="form-group">
                            <label>Moneda facturii</label>
                            <select id="moneda">
                                <option value="RON">RON - Leu</option>
                                <option value="EUR">EUR - Euro</option>
                                <option value="USD">USD - Dolar</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Limba</label>
                            <select id="limba">
                                <option value="ro">Română</option>
                                <option value="en">English</option>
                            </select>
                        </div>
                    </div>

                    <div class="products-section">
                        <h3>Produse/Servicii</h3>
                        <table id="productsTable">
                            <thead>
                                <tr>
                                    <th>Nr. crt.</th>
                                    <th>Denumire produs/serviciu</th>
                                    <th>U.M.</th>
                                    <th>Cant.</th>
                                    <th>Preț (RON)</th>
                                    <th>Valoare</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr id="addProductRow">
                                    <td colspan="6" style="text-align: center; padding: 20px;">
                                        <button type="button" id="addProduct">Adaugă produse/servicii pe factură completând datele de mai sus</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>Întocmit de</label>
                            <input type="text" value="Neculai Fantanaru" readonly>
                        </div>

                        <div class="form-group">
                            <label>CNP</label>
                            <input type="text">
                        </div>

                        <div class="form-group">
                            <label>Delegat</label>
                            <input type="text">
                        </div>

                        <div class="form-group">
                            <label>Buletin</label>
                            <input type="text">
                        </div>

                        <div class="form-group">
                            <label>Auto</label>
                            <input type="text">
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn-success">Salvează și Emite Factură</button>
                        <button type="button" class="btn-secondary">Salvează fără tipărire</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/factura.js') }}"></script>
</body>
</html>'''

        # Salvează pagina factură
        with open(f"{base_path}/templates/factura.html", 'w', encoding='utf-8') as f:
            f.write(factura_html)

    def create_css_files(self):
        """Creează fișierele CSS"""
        base_path = "d:/SmartBillLikeApp"

        css_content = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f5f5f5;
    color: #333;
}

/* Loader Styles */
#loader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

.loader-content {
    text-align: center;
    color: white;
}

.loader-spinner {
    width: 50px;
    height: 50px;
    border: 3px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s ease-in-out infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Container Layout */
.container {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 250px;
    background: #2c3e50;
    color: white;
    padding: 0;
}

.logo {
    padding: 20px;
    background: #34495e;
    text-align: center;
}

.logo h2 {
    font-size: 24px;
    margin-bottom: 5px;
}

.logo span {
    font-size: 12px;
    opacity: 0.8;
}

.nav-menu {
    padding: 20px 0;
}

.nav-item, .nav-subitem {
    display: block;
    padding: 12px 20px;
    color: white;
    text-decoration: none;
    transition: background 0.3s;
}

.nav-item:hover, .nav-subitem:hover {
    background: #34495e;
}

.nav-item.active {
    background: #3498db;
}

.nav-subitem.active {
    background: #2980b9;
    padding-left: 40px;
}

.nav-title {
    display: block;
    padding: 15px 20px 5px;
    font-size: 14px;
    font-weight: bold;
    opacity: 0.8;
}

.nav-subitem {
    padding-left: 40px;
    font-size: 14px;
}

/* Main Content */
.main-content {
    flex: 1;
    padding: 0;
}

header {
    background: white;
    padding: 20px 30px;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

header h1 {
    font-size: 28px;
    color: #2c3e50;
}

.user-info {
    background: #3498db;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
}

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    padding: 30px;
}

.stat-card {
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}

.stat-card h3 {
    font-size: 14px;
    color: #666;
    margin-bottom: 15px;
    font-weight: 600;
}

.stat-value {
    font-size: 36px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 20px;
}

.btn-primary {
    background: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.3s;
}

.btn-primary:hover {
    background: #2980b9;
}

.btn-success {
    background: #27ae60;
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    margin-right: 10px;
}

.btn-secondary {
    background: #95a5a6;
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

.activity-card {
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    grid-column: 1 / -1;
}

.activity-card h3 {
    font-size: 14px;
    color: #666;
    margin-bottom: 15px;
    font-weight: 600;
}

.activity-item {
    padding: 10px 0;
    border-bottom: 1px solid #eee;
}

.activity-item span {
    display: block;
    font-weight: 500;
}

.activity-item small {
    color: #666;
    font-size: 12px;
}

/* Form Styles */
.form-container {
    padding: 30px;
    background: white;
    margin: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.form-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    margin-bottom: 8px;
    font-weight: 500;
    color: #2c3e50;
}

.form-group input,
.form-group select {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.form-group input:focus,
.form-group select:focus {
    outline: none;
    border-color: #3498db;
}

/* Products Table */
.products-section {
    margin: 30px 0;
}

.products-section h3 {
    margin-bottom: 15px;
    color: #2c3e50;
}

#productsTable {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

#productsTable th,
#productsTable td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #eee;
}

#productsTable th {
    background: #f8f9fa;
    font-weight: 600;
    color: #2c3e50;
}

#addProduct {
    background: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
}

.form-actions {
    text-align: right;
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        height: auto;
    }

    .dashboard-grid {
        grid-template-columns: 1fr;
        padding: 15px;
    }
}'''

        with open(f"{base_path}/static/css/style.css", 'w', encoding='utf-8') as f:
            f.write(css_content)

    def create_js_files(self):
        """Creează fișierele JavaScript"""
        base_path = "d:/SmartBillLikeApp"

        # Main.js
        main_js = '''document.addEventListener('DOMContentLoaded', function() {
    // Animații pentru carduri
    const cards = document.querySelectorAll('.stat-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Actualizare automată a datelor
    setInterval(updateDashboard, 30000); // 30 secunde

    function updateDashboard() {
        fetch('/api/dashboard_stats')
            .then(response => response.json())
            .then(data => {
                // Actualizează valorile
                updateStatValue('vanzari', data.vanzari);
                updateStatValue('cheltuieli', data.cheltuieli);
                updateStatValue('sold_clienti', data.sold_clienti);
            })
            .catch(error => console.error('Eroare:', error));
    }

    function updateStatValue(type, value) {
        const element = document.querySelector(`[data-stat="${type}"] .stat-value`);
        if (element) {
            element.textContent = value;
        }
    }
});'''

        # Factura.js
        factura_js = '''document.addEventListener('DOMContentLoaded', function() {
    const facturaForm = document.getElementById('facturaForm');
    const addProductBtn = document.getElementById('addProduct');
    const productsTable = document.getElementById('productsTable');

    // Adaugă produs
    addProductBtn.addEventListener('click', function() {
        addProductRow();
    });

    // Salvează factura
    facturaForm.addEventListener('submit', function(e) {
        e.preventDefault();
        saveFactura();
    });

    function addProductRow() {
        const tbody = productsTable.querySelector('tbody');
        const rowCount = tbody.children.length;

        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${rowCount}</td>
            <td><input type="text" name="denumire" placeholder="Denumire produs/serviciu" required></td>
            <td>
                <select name="um">
                    <option value="buc">buc</option>
                    <option value="kg">kg</option>
                    <option value="ore">ore</option>
                    <option value="mp">mp</option>
                </select>
            </td>
            <td><input type="number" name="cantitate" min="1" value="1" required></td>
            <td><input type="number" name="pret" step="0.01" min="0" required></td>
            <td class="valoare">0.00</td>
        `;

        // Înlocuiește rândul de adăugare
        const addRow = document.getElementById('addProductRow');
        tbody.insertBefore(newRow, addRow);

        // Adaugă event listeners pentru calcul
        const cantitateInput = newRow.querySelector('input[name="cantitate"]');
        const pretInput = newRow.querySelector('input[name="pret"]');
        const valoareCell = newRow.querySelector('.valoare');

        function calculateValue() {
            const cantitate = parseFloat(cantitateInput.value) || 0;
            const pret = parseFloat(pretInput.value) || 0;
            const valoare = cantitate * pret;
            valoareCell.textContent = valoare.toFixed(2);
        }

        cantitateInput.addEventListener('input', calculateValue);
        pretInput.addEventListener('input', calculateValue);
    }

    function saveFactura() {
        const formData = new FormData(facturaForm);
        const facturaData = {
            client_cif: formData.get('clientCIF'),
            data_emitere: formData.get('dataEmitere'),
            moneda: formData.get('moneda'),
            limba: formData.get('limba'),
            produse: []
        };

        // Colectează produsele
        const rows = productsTable.querySelectorAll('tbody tr:not(#addProductRow)');
        rows.forEach(row => {
            const inputs = row.querySelectorAll('input, select');
            if (inputs.length > 0) {
                const produs = {
                    denumire: row.querySelector('input[name="denumire"]').value,
                    um: row.querySelector('select[name="um"]').value,
                    cantitate: row.querySelector('input[name="cantitate"]').value,
                    pret: row.querySelector('input[name="pret"]').value
                };
                facturaData.produse.push(produs);
            }
        });

        // Trimite la server
        fetch('/api/save_factura', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(facturaData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Factura a fost salvată cu succes!');
                window.location.href = '/dashboard';
            } else {
                alert('Eroare la salvarea facturii!');
            }
        })
        .catch(error => {
            console.error('Eroare:', error);
            alert('Eroare la salvarea facturii!');
        });
    }
});'''

        with open(f"{base_path}/static/js/main.js", 'w', encoding='utf-8') as f:
            f.write(main_js)

        with open(f"{base_path}/static/js/factura.js", 'w', encoding='utf-8') as f:
            f.write(factura_js)

    def run(self):
        """Pornește aplicația"""
        print("Creez structura de fișiere...")
        self.create_folder_structure()

        print("Creez baza de date...")
        self.create_database()

        print("Creez fișierele HTML...")
        self.create_html_files()
        self.create_additional_pages()

        print("Creez fișierele CSS și JS...")
        self.create_css_files()
        self.create_js_files()

        print("Aplicația SmartBill este gata!")
        print("Pornesc serverul Flask...")

        # Deschide browserul automat
        threading.Timer(2, lambda: webbrowser.open('http://localhost:5000')).start()

        # Pornește serverul
        self.app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == "__main__":
    # Schimbă directorul de lucru
    os.chdir("d:/SmartBillLikeApp")

    # Creează și pornește aplicația
    app = SmartBillApp()
    app.run()