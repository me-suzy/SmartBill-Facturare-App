
# Script pentru crearea automată a structurii SmartBill

import os
import subprocess
import sys

def create_smartbill_structure():
    """Creează toată structura SmartBill automat"""

    base_path = "d:/SmartBillLikeApp"

    # Creează toate folderele
    folders = [
        base_path,
        f"{base_path}/templates",
        f"{base_path}/static",
        f"{base_path}/static/css",
        f"{base_path}/static/js",
        f"{base_path}/static/images",
        f"{base_path}/database",
        f"{base_path}/reports",
        f"{base_path}/node_modules"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Creat folder: {folder}")

    # Creează toate paginile HTML
    create_all_html_pages(base_path)

    # Creează fișierele CSS
    create_complete_css(base_path)

    # Creează fișierele JavaScript
    create_complete_js(base_path)

    # Creează fișierele de configurare
    create_config_files(base_path)

    # Creează App.jsx (pentru compatibilitate)
    create_react_files(base_path)

    print(f"\n✅ Toată structura SmartBill a fost creată în: {base_path}")
    print("📁 Fișierele principale create:")
    print("   - START.py (aplicația principală)")
    print("   - templates/ (toate paginile HTML)")
    print("   - static/ (CSS, JS, imagini)")
    print("   - database/ (Excel database)")
    print("   - App.jsx, main.jsx, index.css")

def create_all_html_pages(base_path):
    """Creează toate paginile HTML necesare"""
    templates_path = f"{base_path}/templates"

    # Template de bază pentru sidebar
    sidebar_template = '''
        <div class="sidebar">
            <div class="logo">
                <h2>💰 SmartBill</h2>
                <span>FACTURARE</span>
            </div>
            <nav class="nav-menu">
                <a href="/dashboard" class="nav-item {dashboard_active}">
                    <span>📊</span> Dashboard
                </a>
                <div class="nav-group">
                    <span class="nav-title">📄 Emitere</span>
                    <a href="/factura" class="nav-subitem {factura_active}">Factură</a>
                    <a href="/bon-fiscal" class="nav-subitem {bon_fiscal_active}">Bon Fiscal</a>
                    <a href="/factura-storno" class="nav-subitem {factura_storno_active}">Factură Storno</a>
                    <a href="/factura-proforma" class="nav-subitem {factura_proforma_active}">Factură Proforma</a>
                    <a href="/aviz" class="nav-subitem {aviz_active}">Aviz</a>
                    <a href="/voucher" class="nav-subitem {voucher_active}">Voucher</a>
                </div>
                <a href="/preluare-efacturi" class="nav-item {preluare_active}">
                    <span>📥</span> Preluare e-Facturi
                </a>
                <div class="nav-group">
                    <span class="nav-title">📈 Rapoarte</span>
                    <a href="/rapoarte-facturi" class="nav-subitem {rapoarte_facturi_active}">Facturi</a>
                    <a href="/rapoarte-incasari" class="nav-subitem {rapoarte_incasari_active}">Încasări</a>
                    <a href="/rapoarte-proforma" class="nav-subitem {rapoarte_proforma_active}">Proforma</a>
                    <a href="/rapoarte-avize" class="nav-subitem {rapoarte_avize_active}">Avize</a>
                    <a href="/rapoarte-vouchere" class="nav-subitem {rapoarte_vouchere_active}">Vouchere</a>
                    <a href="/rapoarte-vanzari-produse" class="nav-subitem">Vânzări produse</a>
                    <a href="/rapoarte-sume-incasat" class="nav-subitem">Sume de încasat pe client</a>
                    <a href="/rapoarte-fisa-client" class="nav-subitem">Fișa client</a>
                    <a href="/rapoarte-vanzari-agent" class="nav-subitem">Vânzări pe agent</a>
                    <a href="/rapoarte-registru-casa" class="nav-subitem">Registru casa</a>
                    <a href="/rapoarte-tranzactii-bancare" class="nav-subitem">Tranzacții bancare</a>
                    <a href="/rapoarte-preluari-importuri" class="nav-subitem">Preluări și importuri tranzacții</a>
                </div>
                <div class="nav-group">
                    <span class="nav-title">⚙️ Configurare</span>
                    <a href="/configurare-generale" class="nav-subitem {config_generale_active}">Generale</a>
                    <a href="/configurare-sedii" class="nav-subitem {config_sedii_active}">Sedii</a>
                    <a href="/configurare-conturi-bancare" class="nav-subitem {config_bancare_active}">Conturi bancare</a>
                    <a href="/configurare-seriii" class="nav-subitem {config_serii_active}">Serii</a>
                    <a href="/configurare-personalizare" class="nav-subitem {config_personalizare_active}">Personalizare</a>
                    <a href="/configurare-efactura" class="nav-subitem {config_efactura_active}">e-Factura</a>
                    <a href="/configurare-case-marcat" class="nav-subitem {config_case_active}">Case de marcat</a>
                    <a href="/configurare-limbi" class="nav-subitem {config_limbi_active}">Limbi</a>
                    <a href="/configurare-preferinte" class="nav-subitem {config_preferinte_active}">Preferințe personale</a>
                    <a href="/configurare-generale-pref" class="nav-subitem {config_generale_pref_active}">Preferințe generale</a>
                    <a href="/configurare-notificari" class="nav-subitem {config_notificari_active}">Notificări clienți</a>
                    <a href="/configurare-email" class="nav-subitem {config_email_active}">Email</a>
                </div>
                <div class="nav-group">
                    <span class="nav-title">📝 Nomenclatoare</span>
                    <a href="/produse" class="nav-subitem {produse_active}">Produse</a>
                    <a href="/categorii-cheltuieli" class="nav-subitem {categorii_active}">Categorii cheltuieli</a>
                    <a href="/grupari-produse" class="nav-subitem {grupari_active}">Grupări produse</a>
                    <a href="/clienti" class="nav-subitem {clienti_active}">Clienți</a>
                    <a href="/furnizori" class="nav-subitem {furnizori_active}">Furnizori</a>
                </div>
                <a href="/utilizatori" class="nav-item {utilizatori_active}">
                    <span>👥</span> Utilizatori
                </a>
                <a href="/contul-meu" class="nav-item {contul_meu_active}">
                    <span>👤</span> Contul Meu
                </a>
            </nav>
        </div>
    '''

    # Funcție pentru generarea headerului
    def create_header(title, breadcrumb=""):
        return f'''
            <header>
                <h1>{title}</h1>
                {f'<nav class="breadcrumb">{breadcrumb}</nav>' if breadcrumb else ''}
                <div class="user-info">
                    <span>TIP B. SRL</span>
                    <div class="user-menu">
                        <button class="user-dropdown">Neculai Fantanaru ▼</button>
                    </div>
                </div>
            </header>
        '''

    # 1. INDEX.HTML cu loader
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
            <div class="logo-loader">
                <h2>💰 SmartBill</h2>
                <span>FACTURARE</span>
            </div>
            <p>Se încarcă aplicația...</p>
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
        </div>
    </div>

    <script>
        let progress = 0;
        const progressFill = document.querySelector('.progress-fill');

        const interval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress > 100) progress = 100;

            progressFill.style.width = progress + '%';

            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 500);
            }
        }, 200);
    </script>
</body>
</html>'''

    # 2. DASHBOARD.HTML
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
        ''' + sidebar_template.format(
            dashboard_active="active", factura_active="", bon_fiscal_active="",
            factura_storno_active="", factura_proforma_active="", aviz_active="",
            voucher_active="", preluare_active="", rapoarte_facturi_active="",
            rapoarte_incasari_active="", rapoarte_proforma_active="", rapoarte_avize_active="",
            rapoarte_vouchere_active="", config_generale_active="", config_sedii_active="",
            config_bancare_active="", config_serii_active="", config_personalizare_active="",
            config_efactura_active="", config_case_active="", config_limbi_active="",
            config_preferinte_active="", config_generale_pref_active="", config_notificari_active="",
            config_email_active="", produse_active="", categorii_active="", grupari_active="",
            clienti_active="", furnizori_active="", utilizatori_active="", contul_meu_active=""
        ) + '''

        <div class="main-content">
            ''' + create_header("Dashboard") + '''

            <div class="alert-banner">
                <div class="alert-content">
                    <span class="alert-icon">⚠️</span>
                    <div class="alert-text">
                        <strong>Securizează-ți contul de SmartBill</strong>
                        <p>Activează autentificarea în 2 pași pentru a reduce riscul de accesare neautorizată a contului tău.</p>
                        <a href="#" class="alert-link">Vreau un cont mai sigur</a>
                    </div>
                </div>
            </div>

            <div class="dashboard-progress">
                <div class="progress-section">
                    <span class="progress-label">Primele operațiuni</span>
                    <div class="progress-circle">
                        <span class="progress-value">2/7</span>
                        <span class="progress-text">completați</span>
                    </div>
                </div>
                <div class="progress-section">
                    <span class="progress-label">e-Factura</span>
                    <div class="progress-circle">
                        <span class="progress-value">2/5</span>
                        <span class="progress-text">completați</span>
                    </div>
                </div>
            </div>

            <div class="dashboard-grid">
                <div class="stat-card vanzari" data-stat="vanzari">
                    <h3>VÂNZĂRI</h3>
                    <div class="stat-value">{{ stats.vanzari or 7618 }}</div>
                    <div class="stat-currency">RON</div>
                    <button class="btn-primary" onclick="window.location.href='/factura'">Emite factură</button>
                </div>

                <div class="stat-card sold-clienti" data-stat="sold_clienti">
                    <h3>SOLD CLIENȚI</h3>
                    <div class="stat-value">{{ stats.sold_clienti or 0 }}</div>
                    <div class="stat-currency">RON</div>
                    <p class="stat-description">Obține lista primilor 10 clienți în ordinea sumelor pe care le-ți datorează.</p>
                    <button class="btn-primary" onclick="window.location.href='/factura'">Emite factură</button>
                </div>

                <div class="stat-card facturi-neincasate" data-stat="facturi_neincasate">
                    <h3>FACTURI NEÎNCASATE</h3>
                    <div class="stat-value">{{ stats.facturi_neincasate or 0 }}</div>
                    <p class="stat-description">Obține lista facturilor neîncasate în funcție de vechimea lor.</p>
                    <button class="btn-primary" onclick="window.location.href='/factura'">Emite factură</button>
                </div>

                <div class="stat-card cheltuieli" data-stat="cheltuieli">
                    <h3>CHELTUIELI</h3>
                    <div class="stat-value">{{ stats.cheltuieli or 4704 }}</div>
                    <div class="stat-currency">RON</div>
                    <p class="stat-description">Află care sunt cheltuielile firmei și cum se împart ele pe categorii.</p>
                    <button class="btn-primary">Adaugă cheltuială</button>
                </div>

                <div class="stat-card sume-platit">
                    <h3>SUME DE PLĂTIT</h3>
                    <div class="stat-value">1467</div>
                    <div class="stat-currency">RON</div>
                    <p class="stat-description">Află care sume trebuie să plătești, când anume și către cine.</p>
                    <button class="btn-primary">Adaugă cheltuială</button>
                </div>

                <div class="activity-card">
                    <h3>ACTIVITATE</h3>
                    <div class="activity-list">
                        <div class="activity-item">
                            <div class="activity-avatar">👤</div>
                            <div class="activity-content">
                                <span class="activity-action">Adăugare utilizator Făntănaru Neculai</span>
                                <small class="activity-time">Ioan.fantanaru@gmail.com</small>
                                <small class="activity-date">Făntănaru Neculai - ieri, 29 iul, ora 23:59</small>
                            </div>
                        </div>
                        <div class="activity-item">
                            <div class="activity-avatar">🏢</div>
                            <div class="activity-content">
                                <span class="activity-action">Creare companie TIP B. SRL</span>
                                <small class="activity-date">Făntănaru Neculai - ieri, 29 iul, ora 23:59</small>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="stat-card sold-casa">
                    <h3>SOLD CASA</h3>
                    <p class="stat-description">Setează soldul inițial, astfel încât soldul de casă să poată fi calculat.</p>
                    <button class="btn-primary">Setează soldul inițial</button>
                </div>

                <div class="stat-card total-scadent">
                    <h3>TOTAL SCADENT</h3>
                    <p class="stat-description">A doua partea are următorul sold și, în final, calculat.</p>
                </div>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>'''

    # 3. FACTURA.HTML - Formularul de factură complet
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
        ''' + sidebar_template.format(
            dashboard_active="", factura_active="active", bon_fiscal_active="",
            factura_storno_active="", factura_proforma_active="", aviz_active="",
            voucher_active="", preluare_active="", rapoarte_facturi_active="",
            rapoarte_incasari_active="", rapoarte_proforma_active="", rapoarte_avize_active="",
            rapoarte_vouchere_active="", config_generale_active="", config_sedii_active="",
            config_bancare_active="", config_serii_active="", config_personalizare_active="",
            config_efactura_active="", config_case_active="", config_limbi_active="",
            config_preferinte_active="", config_generale_pref_active="", config_notificari_active="",
            config_email_active="", produse_active="", categorii_active="", grupari_active="",
            clienti_active="", furnizori_active="", utilizatori_active="", contul_meu_active=""
        ) + '''

        <div class="main-content">
            ''' + create_header("Emitere › Factură") + '''

            <div class="form-container">
                <div class="form-alerts">
                    <div class="alert alert-warning">
                        <span class="alert-icon">⚠️</span>
                        <div>
                            <strong>Pentru firme: completează CIF valid și preiau datele firmei din ANAF.</strong><br>
                            Pentru persoane fizice: adaugă CNP sau folosește semnul minus între caractere.
                        </div>
                    </div>
                </div>

                <form id="facturaForm" class="factura-form">
                    <div class="form-header">
                        <div class="form-options">
                            <button type="button" class="btn-option active" data-tab="optiuni">⚙️ Opțiuni factură</button>
                            <button type="button" class="btn-option" data-tab="help">❓</button>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group large">
                            <label for="clientCIF">Nume sau CIF/CNP</label>
                            <div class="input-group">
                                <input type="text" id="clientCIF" name="clientCIF"
                                       placeholder="Cif pt. firme/CNP dacă sunt semnul minus între caractere" required>
                                <button type="button" id="addClient" class="btn-add">+ Adaugă Client</button>
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="dataEmitere">Data emiterii</label>
                            <input type="date" id="dataEmitere" name="dataEmitere" value="{{ moment().format('YYYY-MM-DD') }}" required>
                        </div>

                        <div class="form-group">
                            <label for="termenPlata">Termen de plată</label>
                            <select id="termenPlata" name="termenPlata">
                                <option value="">Selectează</option>
                                <option value="0">La prezentare</option>
                                <option value="15">15 zile</option>
                                <option value="30">30 zile</option>
                                <option value="45">45 zile</option>
                                <option value="60">60 zile</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="serieNumar">Serie și număr</label>
                            <select id="serieNumar" name="serieNumar">
                                <option value="re.nr.0001">re.nr.0001</option>
                                <option value="fact.nr.0001">fact.nr.0001</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="moneda">Moneda facturii</label>
                            <select id="moneda" name="moneda">
                                <option value="RON">RON - Leu</option>
                                <option value="EUR">EUR - Euro</option>
                                <option value="USD">USD - Dolar</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="limba">Limba</label>
                            <select id="limba" name="limba">
                                <option value="ro">Română</option>
                                <option value="en">English</option>
                                <option value="hu">Magyar</option>
                                <option value="de">Deutsch</option>
                            </select>
                        </div>
                    </div>

                    <div class="products-section">
                        <h3>Produse/Servicii</h3>
                        <div class="products-toolbar">
                            <input type="text" id="productSearch" placeholder="Denumire produs/serviciu">
                            <input type="text" id="productCode" placeholder="Cod">
                            <select id="productUM">
                                <option value="">U.M.</option>
                                <option value="buc">buc</option>
                                <option value="kg">kg</option>
                                <option value="ore">ore</option>
                                <option value="mp">mp</option>
                            </select>
                            <input type="number" id="productQuantity" placeholder="Cantitate" min="1" step="0.01">
                            <input type="number" id="productPrice" placeholder="Preț (RON)" min="0" step="0.01">
                            <button type="button" id="addProduct" class="btn-add">+ Detalii produs</button>
                            <button type="button" id="addDescription" class="btn-add">+ Adaugă descriere</button>
                        </div>

                        <table id="productsTable" class="products-table">
                            <thead>
                                <tr>
                                    <th>Nr. crt.</th>
                                    <th>Denumire produs/serviciu</th>
                                    <th>U.M.</th>
                                    <th>Cant.</th>
                                    <th>Preț (RON)</th>
                                    <th>Valoare</th>
                                    <th>Acțiuni</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr id="addProductRow">
                                    <td colspan="7" class="add-product-prompt">
                                        <div class="add-product-content">
                                            <span class="info-icon">ℹ️</span>
                                            <span>Adaugă produse/servicii pe factură completând datele de mai sus</span>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>

                        <div class="form-checkbox">
                            <input type="checkbox" id="incaseazaAcum" name="incaseazaAcum">
                            <label for="incaseazaAcum">Încasează acum (total sau parțial)</label>
                        </div>
                    </div>

                    <div class="additional-data">
                        <h3>Date adiționale</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="intocmitDe">Întocmit de</label>
                                <input type="text" id="intocmitDe" name="intocmitDe" value="Neculai Fantanaru" readonly>
                            </div>

                            <div class="form-group">
                                <label for="cnpIntocmitor">CNP</label>
                                <input type="text" id="cnpIntocmitor" name="cnpIntocmitor">
                            </div>

                            <div class="form-group">
                                <label for="delegat">Delegat</label>
                                <input type="text" id="delegat" name="delegat">
                            </div>

                            <div class="form-group">
                                <label for="buletin">Buletin</label>
                                <input type="text" id="buletin" name="buletin">
                            </div>

                            <div class="form-group">
                                <label for="auto">Auto</label>
                                <input type="text" id="auto" name="auto">
                            </div>
                        </div>

                        <div class="form-group full-width">
                            <label for="mentiuni">Mențiuni</label>
                            <textarea id="mentiuni" name="mentiuni" rows="4"
                                     placeholder="Adaugă mențiuni suplimentare pentru această factură..."></textarea>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn-success">
                            <span>💾</span> Salvează și Emite Factură
                        </button>
                        <button type="button" class="btn-secondary" id="saveWithoutPrint">
                            <span>💾</span> Salvează fără tipărire
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/factura.js') }}"></script>
</body>
</html>'''

    # Salvează toate paginile HTML
    html_files = {
        'index.html': index_html,
        'dashboard.html': dashboard_html,
        'factura.html': factura_html,
    }

    # Continuă cu toate celelalte pagini...
    create_remaining_pages(templates_path, sidebar_template, create_header)

    for filename, content in html_files.items():
        with open(f"{templates_path}/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Creat: {filename}")

def create_remaining_pages(templates_path, sidebar_template, create_header):
    """Creează toate paginile HTML rămase"""

    # BON FISCAL
    bon_fiscal_html = '''<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartBill - Bon Fiscal</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        ''' + sidebar_template.format(
            dashboard_active="", factura_active="", bon_fiscal_active="active",
            factura_storno_active="", factura_proforma_active="", aviz_active="",
            voucher_active="", preluare_active="", rapoarte_facturi_active="",
            rapoarte_incasari_active="", rapoarte_proforma_active="", rapoarte_avize_active="",
            rapoarte_vouchere_active="", config_generale_active="", config_sedii_active="",
            config_bancare_active="", config_serii_active="", config_personalizare_active="",
            config_efactura_active="", config_case_active="", config_limbi_active="",
            config_preferinte_active="", config_generale_pref_active="", config_notificari_active="",
            config_email_active="", produse_active="", categorii_active="", grupari_active="",
            clienti_active="", furnizori_active="", utilizatori_active="", contul_meu_active=""
        ) + '''

        <div class="main-content">
            ''' + create_header("Emitere › Bon Fiscal") + '''

            <div class="alert-banner">
                <div class="alert-content">
                    <span class="alert-icon">⚠️</span>
                    <div class="alert-text">
                        <strong>Pentru a putea tipări bonuri fiscale trebuie să instalezi și să configurezi</strong>
                        <p>plugin-ul desktop SmartBill pentru case de marcat. Te rugăm să accesezi <a href="#">plugin-ul de aici</a>.</p>
                    </div>
                </div>
            </div>

            <div class="form-container">
                <form id="bonFiscalForm" class="bon-fiscal-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="dataBon">Data</label>
                            <input type="date" id="dataBon" name="dataBon" value="{{ moment().format('YYYY-MM-DD') }}" required>
                        </div>

                        <div class="form-group">
                            <label for="casaMarcat">Casa de marcat</label>
                            <select id="casaMarcat" name="casaMarcat">
                                <option value="">---</option>
                                <option value="casa1">Casa de marcat 1</option>
                                <option value="casa2">Casa de marcat 2</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="numarBon">Nr. bon</label>
                            <input type="text" id="numarBon" name="numarBon" readonly>
                        </div>
                    </div>

                    <div class="total-section">
                        <h3>Total de încasat</h3>
                        <div class="total-display">
                            <span class="total-label">Încasat de la client</span>
                            <div class="total-actions">
                                <button type="button" class="btn-option">Adaugă o casă de marcat și setează metodele de plată pentru casa respectivă - aici</button>
                                <select id="cifClient">
                                    <option value="">CIF client</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="products-section">
                        <div class="products-toolbar">
                            <input type="text" id="productSearch" placeholder="Denumire produs/serviciu">
                            <input type="text" id="productCode" placeholder="Cod">
                            <select id="productUM">
                                <option value="">U.M.</option>
                                <option value="buc">buc</option>
                                <option value="kg">kg</option>
                                <option value="ore">ore</option>
                                <option value="mp">mp</option>
                            </select>
                            <input type="number" id="productQuantity" placeholder="Cantitate" min="1" step="0.01">
                            <input type="number" id="productPrice" placeholder="Preț" min="0" step="0.01">
                            <button type="button" id="addProduct" class="btn-primary">Adaugă</button>
                        </div>

                        <table id="productsTable" class="products-table">
                            <thead>
                                <tr>
                                    <th>Nr. crt.</th>
                                    <th>Denumire produs/serviciu</th>
                                    <th>U.M.</th>
                                    <th>Cant.</th>
                                    <th>Preț</th>
                                    <th>Valoare</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr id="addProductRow">
                                    <td colspan="6" class="add-product-prompt">
                                        <div class="add-product-content">
                                            <span class="info-icon">ℹ️</span>
                                            <span>Adaugă produse/servicii pe bon completând datele de mai sus</span>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn-success">Tipărește bon fiscal</button>
                        <button type="button" class="btn-secondary">Salvează fără tipărire</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/bon-fiscal.js') }}"></script>
</body>
</html>'''

    # RAPOARTE - Pagina principală de rapoarte
    rapoarte_html = '''<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartBill - Rapoarte</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        ''' + sidebar_template.format(
            dashboard_active="", factura_active="", bon_fiscal_active="",
            factura_storno_active="", factura_proforma_active="", aviz_active="",
            voucher_active="", preluare_active="", rapoarte_facturi_active="active",
            rapoarte_incasari_active="", rapoarte_proforma_active="", rapoarte_avize_active="",
            rapoarte_vouchere_active="", config_generale_active="", config_sedii_active="",
            config_bancare_active="", config_serii_active="", config_personalizare_active="",
            config_efactura_active="", config_case_active="", config_limbi_active="",
            config_preferinte_active="", config_generale_pref_active="", config_notificari_active="",
            config_email_active="", produse_active="", categorii_active="", grupari_active="",
            clienti_active="", furnizori_active="", utilizatori_active="", contul_meu_active=""
        ) + '''

        <div class="main-content">
            ''' + create_header("Rapoarte") + '''

            <div class="rapoarte-grid">
                <div class="raport-category">
                    <h3>📄 Documente emise</h3>
                    <div class="raport-links">
                        <a href="/rapoarte-facturi" class="raport-link">
                            <span class="raport-icon">📊</span>
                            <div>
                                <strong>Facturi</strong>
                                <p>Vizualizează toate facturile emise</p>
                            </div>
                        </a>
                        <a href="/rapoarte-incasari" class="raport-link">
                            <span class="raport-icon">💰</span>
                            <div>
                                <strong>Încasări</strong>
                                <p>Raport încasări și plăți</p>
                            </div>
                        </a>
                        <a href="/rapoarte-proforma" class="raport-link">
                            <span class="raport-icon">📋</span>
                            <div>
                                <strong>Proforma</strong>
                                <p>Facturi proforma emise</p>
                            </div>
                        </a>
                        <a href="/rapoarte-avize" class="raport-link">
                            <span class="raport-icon">📦</span>
                            <div>
                                <strong>Avize</strong>
                                <p>Avize de livrare</p>
                            </div>
                        </a>
                        <a href="/rapoarte-vouchere" class="raport-link">
                            <span class="raport-icon">🎫</span>
                            <div>
                                <strong>Vouchere</strong>
                                <p>Vouchere emise</p>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="raport-category">
                    <h3>📈 Rapoarte avansate</h3>
                    <div class="raport-links">
                        <a href="/rapoarte-vanzari-produse" class="raport-link">
                            <span class="raport-icon">📊</span>
                            <div>
                                <strong>Vânzări produse</strong>
                                <p>Analiză vânzări pe produse</p>
                            </div>
                        </a>
                        <a href="/rapoarte-sume-incasat" class="raport-link">
                            <span class="raport-icon">💳</span>
                            <div>
                                <strong>Sume de încasat pe client</strong>
                                <p>Solduri clienți</p>
                            </div>
                        </a>
                        <a href="/rapoarte-fisa-client" class="raport-link">
                            <span class="raport-icon">👤</span>
                            <div>
                                <strong>Fișa client</strong>
                                <p>Detalii complete client</p>
                            </div>
                        </a>
                        <a href="/rapoarte-vanzari-agent" class="raport-link">
                            <span class="raport-icon">👨‍💼</span>
                            <div>
                                <strong>Vânzări pe agent</strong>
                                <p>Performance agenți vânzări</p>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="raport-category">
                    <h3>🏦 Bănci, curieri și procesatori</h3>
                    <div class="raport-links">
                        <a href="/rapoarte-tranzactii-bancare" class="raport-link">
                            <span class="raport-icon">🏦</span>
                            <div>
                                <strong>Tranzacții bancare</strong>
                                <p>Toate tranzacțiile bancare</p>
                            </div>
                        </a>
                        <a href="/rapoarte-incasari-curieri" class="raport-link">
                            <span class="raport-icon">🚚</span>
                            <div>
                                <strong>Încasări curieri și procesatori</strong>
                                <p>Situația încasărilor externe</p>
                            </div>
                        </a>
                        <a href="/rapoarte-preluari-importuri" class="raport-link">
                            <span class="raport-icon">📥</span>
                            <div>
                                <strong>Preluări și importuri tranzacții</strong>
                                <p>Importuri automate de tranzacții</p>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="raport-category">
                    <h3>🏠 Registru casa</h3>
                    <div class="raport-links">
                        <a href="/rapoarte-registru-casa" class="raport-link">
                            <span class="raport-icon">📖</span>
                            <div>
                                <strong>Vizualizare registru casa</strong>
                                <p>Registrul de casă complet</p>
                            </div>
                        </a>
                        <a href="/rapoarte-operatiuni-casa" class="raport-link">
                            <span class="raport-icon">💰</span>
                            <div>
                                <strong>Operațiuni casa</strong>
                                <p>Toate operațiunile de casă</p>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="raport-category">
                    <h3>📊 Grafice</h3>
                    <div class="raport-links">
                        <a href="/rapoarte-grafice-facturi" class="raport-link">
                            <span class="raport-icon">📊</span>
                            <div>
                                <strong>Facturi</strong>
                                <p>Grafice și statistici facturi</p>
                            </div>
                        </a>
                        <a href="/rapoarte-grafice-clienti" class="raport-link">
                            <span class="raport-icon">👥</span>
                            <div>
                                <strong>Clienți</strong>
                                <p>Analize grafice clienți</p>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/rapoarte.js') }}"></script>
</body>
</html>'''

    # CONFIGURARE - Pagina principală
    configurare_html = '''<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartBill - Configurare</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        ''' + sidebar_template.format(
            dashboard_active="", factura_active="", bon_fiscal_active="",
            factura_storno_active="", factura_proforma_active="", aviz_active="",
            voucher_active="", preluare_active="", rapoarte_facturi_active="",
            rapoarte_incasari_active="", rapoarte_proforma_active="", rapoarte_avize_active="",
            rapoarte_vouchere_active="", config_generale_active="active", config_sedii_active="",
            config_bancare_active="", config_serii_active="", config_personalizare_active="",
            config_efactura_active="", config_case_active="", config_limbi_active="",
            config_preferinte_active="", config_generale_pref_active="", config_notificari_active="",
            config_email_active="", produse_active="", categorii_active="", grupari_active="",
            clienti_active="", furnizori_active="", utilizatori_active="", contul_meu_active=""
        ) + '''

        <div class="main-content">
            ''' + create_header("Configurare") + '''

            <div class="config-grid">
                <div class="config-category">
                    <h3>🏢 Datele firmei</h3>
                    <div class="config-links">
                        <a href="/configurare-generale" class="config-link">
                            <span class="config-icon">⚙️</span>
                            <div>
                                <strong>Generale</strong>
                                <p>Date generale ale firmei</p>
                            </div>
                        </a>
                        <a href="/configurare-sedii" class="config-link">
                            <span class="config-icon">🏢</span>
                            <div>
                                <strong>Sedii</strong>
                                <p>Gestionează sediile firmei</p>
                            </div>
                        </a>
                        <a href="/configurare-conturi-bancare" class="config-link">
                            <span class="config-icon">🏦</span>
                            <div>
                                <strong>Conturi bancare</strong>
                                <p>Configurează conturile bancare</p>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="config-category">
                    <h3>📄 Emitere documente</h3>
                    <div class="config-links">
                        <a href="/configurare-serii" class="config-link">
                            <span class="config-icon">🔢</span>
                            <div>
                                <strong>Serii</strong>
                                <p>Configurează seriile documentelor</p>
                            </div>
                        </a>
                        <a href="/configurare-personalizare" class="config-link">
                            <span class="config-icon">🎨</span>
                            <div>
                                <strong>Personalizare</strong>
                                <p>Personalizează aspectul documentelor</p>
                            </div>
                        </a>
                        <a href="/configurare-efactura" class="config-link">
                            <span class="config-icon">📧</span>
                            <div>
                                <strong>e-Factura</strong>
                                <p>Configurare e-Factura ANAF</p>
                            </div>
                        </a>
                        <a href="/configurare-case-marcat" class="config-link">
                            <span class="config-icon">🖨️</span>
                            <div>
                                <strong>Case de marcat</strong>
                                <p>Configurare case de marcat</p>
                            </div>
                        </a>
                        <a href="/configurare-limbi" class="config-link">
                            <span class="config-icon">🌐</span>
                            <div>
                                <strong>Limbi</strong>
                                <p>Limbile pentru documente</p>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="config-category">
                    <h3>👤 Configurări program</h3>
                    <div class="config-links">
                        <a href="/configurare-preferinte" class="config-link">
                            <span class="config-icon">⚙️</span>
                            <div>
                                <strong>Preferințe personale</strong>
                                <p>Setările tale personale</p>
                            </div>
                        </a>
                        <a href="/configurare-generale-pref" class="config-link">
                            <span class="config-icon">🔧</span>
                            <div>
                                <strong>Preferințe generale</strong>
                                <p>Setări generale aplicație</p>
                            </div>
                        </a>
                        <a href="/configurare-notificari" class="config-link">
                            <span class="config-icon">🔔</span>
                            <div>
                                <strong>Notificări clienți</strong>
                                <p>Configurează notificările</p>
                            </div>
                        </a>
                        <a href="/configurare-email" class="config-link">
                            <span class="config-icon">📧</span>
                            <div>
                                <strong>Email</strong>
                                <p>Configurare server email</p>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/configurare.js') }}"></script>
</body>
</html>'''

    # PRODUSE - Nomenclator produse
    produse_html = '''<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartBill - Produse</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        ''' + sidebar_template.format(
            dashboard_active="", factura_active="", bon_fiscal_active="",
            factura_storno_active="", factura_proforma_active="", aviz_active="",
            voucher_active="", preluare_active="", rapoarte_facturi_active="",
            rapoarte_incasari_active="", rapoarte_proforma_active="", rapoarte_avize_active="",
            rapoarte_vouchere_active="", config_generale_active="", config_sedii_active="",
            config_bancare_active="", config_serii_active="", config_personalizare_active="",
            config_efactura_active="", config_case_active="", config_limbi_active="",
            config_preferinte_active="", config_generale_pref_active="", config_notificari_active="",
            config_email_active="", produse_active="active", categorii_active="", grupari_active="",
            clienti_active="", furnizori_active="", utilizatori_active="", contul_meu_active=""
        ) + '''

        <div class="main-content">
            ''' + create_header("Nomenclatoare › Produse") + '''

            <div class="content-toolbar">
                <div class="toolbar-left">
                    <button class="btn-primary" id="addProduct">
                        <span>➕</span> Adaugă produs
                    </button>
                    <button class="btn-secondary" id="importProducts">
                        <span>📤</span> Import produse
                    </button>
                    <button class="btn-secondary" id="exportProducts">
                        <span>📥</span> Export
                    </button>
                </div>
                <div class="toolbar-right">
                    <input type="text" id="searchProducts" placeholder="Caută produse..." class="search-input">
                    <select id="categoryFilter" class="filter-select">
                        <option value="">Toate categoriile</option>
                        <option value="servicii">Servicii</option>
                        <option value="materiale">Materiale</option>
                        <option value="produse_finite">Produse finite</option>
                    </select>
                </div>
            </div>

            <div class="table-container">
                <table id="productsTable" class="data-table">
                    <thead>
                        <tr>
                            <th>
                                <input type="checkbox" id="selectAll">
                            </th>
                            <th>Cod</th>
                            <th>Denumire</th>
                            <th>U.M.</th>
                            <th>Preț vânzare</th>
                            <th>TVA %</th>
                            <th>Categorie</th>
                            <th>Stoc</th>
                            <th>Acțiuni</th>
                        </tr>
                    </thead>
                    <tbody id="productsTableBody">
                        <!-- Produsele vor fi încărcate dinamic -->
                    </tbody>
                </table>
            </div>

            <div class="pagination">
                <button class="btn-page" id="prevPage" disabled>‹ Anterior</button>
                <span class="page-info">Pagina 1 din 1</span>
                <button class="btn-page" id="nextPage" disabled>Următorul ›</button>
            </div>
        </div>
    </div>

    <!-- Modal pentru adăugare/editare produs -->
    <div id="productModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modalTitle">Adaugă produs nou</h3>
                <button class="modal-close" id="closeModal">&times;</button>
            </div>
            <form id="productForm" class="modal-form">
                <div class="form-row">
                    <div class="form-group">
                        <label for="productCode">Cod produs</label>
                        <input type="text" id="productCode" name="cod" required>
                    </div>
                    <div class="form-group">
                        <label for="productName">Denumire</label>
                        <input type="text" id="productName" name="denumire" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="productUM">Unitate de măsură</label>
                        <select id="productUM" name="um" required>
                            <option value="">Selectează</option>
                            <option value="buc">buc</option>
                            <option value="kg">kg</option>
                            <option value="ore">ore</option>
                            <option value="mp">mp</option>
                            <option value="ml">ml</option>
                            <option value="cm">cm</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="productPrice">Preț vânzare (RON)</label>
                        <input type="number" id="productPrice" name="pret" step="0.01" min="0" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="productTVA">TVA (%)</label>
                        <select id="productTVA" name="tva" required>
                            <option value="19">19%</option>
                            <option value="9">9%</option>
                            <option value="5">5%</option>
                            <option value="0">0%</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="productCategory">Categorie</label>
                        <select id="productCategory" name="categorie">
                            <option value="">Fără categorie</option>
                            <option value="servicii">Servicii</option>
                            <option value="materiale">Materiale</option>
                            <option value="produse_finite">Produse finite</option>
                        </select>
                    </div>
                </div>
                <div class="form-group full-width">
                    <label for="productDescription">Descriere</label>
                    <textarea id="productDescription" name="descriere" rows="3"></textarea>
                </div>
                <div class="modal-actions">
                    <button type="submit" class="btn-success">Salvează</button>
                    <button type="button" class="btn-secondary" id="cancelModal">Anulează</button>
                </div>
            </form>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/produse.js') }}"></script>
</body>
</html>'''

    # CLIENTI - Nomenclator clienți
    clienti_html = '''<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartBill - Clienți</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        ''' + sidebar_template.format(
            dashboard_active="", factura_active="", bon_fiscal_active="",
            factura_storno_active="", factura_proforma_active="", aviz_active="",
            voucher_active="", preluare_active="", rapoarte_facturi_active="",
            rapoarte_incasari_active="", rapoarte_proforma_active="", rapoarte_avize_active="",
            rapoarte_vouchere_active="", config_generale_active="", config_sedii_active="",
            config_bancare_active="", config_serii_active="", config_personalizare_active="",
            config_efactura_active="", config_case_active="", config_limbi_active="",
            config_preferinte_active="", config_generale_pref_active="", config_notificari_active="",
            config_email_active="", produse_active="", categorii_active="", grupari_active="",
            clienti_active="active", furnizori_active="", utilizatori_active="", contul_meu_active=""
        ) + '''

        <div class="main-content">
            ''' + create_header("Nomenclatoare › Clienți") + '''

            <div class="content-toolbar">
                <div class="toolbar-left">
                    <button class="btn-primary" id="addClient">
                        <span>➕</span> Adaugă client
                    </button>
                    <button class="btn-secondary" id="importClients">
                        <span>📤</span> Import clienți
                    </button>
                    <button class="btn-secondary" id="exportClients">
                        <span>📥</span> Export
                    </button>
                </div>
                <div class="toolbar-right">
                    <input type="text" id="searchClients" placeholder="Caută clienți..." class="search-input">
                    <select id="typeFilter" class="filter-select">
                        <option value="">Toți clienții</option>
                        <option value="firma">Firme</option>
                        <option value="persoana_fizica">Persoane fizice</option>
                    </select>
                </div>
            </div>

            <div class="table-container">
                <table id="clientsTable" class="data-table">
                    <thead>
                        <tr>
                            <th>
                                <input type="checkbox" id="selectAll">
                            </th>
                            <th>CIF/CNP</th>
                            <th>Nume/Denumire</th>
                            <th>Email</th>
                            <th>Telefon</th>
                            <th>Localitate</th>
                            <th>Sold curent</th>
                            <th>Acțiuni</th>
                        </tr>
                    </thead>
                    <tbody id="clientsTableBody">
                        <!-- Clienții vor fi încărcați dinamic -->
                    </tbody>
                </table>
            </div>

            <div class="pagination">
                <button class="btn-page" id="prevPage" disabled>‹ Anterior</button>
                <span class="page-info">Pagina 1 din 1</span>
                <button class="btn-page" id="nextPage" disabled>Următorul ›</button>
            </div>
        </div>
    </div>

    <!-- Modal pentru adăugare/editare client -->
    <div id="clientModal" class="modal">
        <div class="modal-content large">
            <div class="modal-header">
                <h3 id="modalTitle">Adaugă client nou</h3>
                <button class="modal-close" id="closeModal">&times;</button>
            </div>
            <form id="clientForm" class="modal-form">
                <div class="form-tabs">
                    <button type="button" class="tab-btn active" data-tab="general">General</button>
                    <button type="button" class="tab-btn" data-tab="contact">Date de contact</button>
                    <button type="button" class="tab-btn" data-tab="financiar">Date financiare</button>
                </div>

                <div id="general" class="tab-content active">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientType">Tip client</label>
                            <select id="clientType" name="tip_client" required>
                                <option value="firma">Firmă</option>
                                <option value="persoana_fizica">Persoană fizică</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="clientCIF">CIF/CNP</label>
                            <input type="text" id="clientCIF" name="cif" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientName">Nume/Denumire</label>
                            <input type="text" id="clientName" name="nume" required>
                        </div>
                        <div class="form-group">
                            <label for="clientRegCom">Reg. Com.</label>
                            <input type="text" id="clientRegCom" name="reg_com">
                        </div>
                    </div>
                </div>

                <div id="contact" class="tab-content">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientEmail">Email</label>
                            <input type="email" id="clientEmail" name="email">
                        </div>
                        <div class="form-group">
                            <label for="clientPhone">Telefon</label>
                            <input type="tel" id="clientPhone" name="telefon">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientAddress">Adresă</label>
                            <input type="text" id="clientAddress" name="adresa">
                        </div>
                        <div class="form-group">
                            <label for="clientCity">Localitate</label>
                            <input type="text" id="clientCity" name="localitate">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientCounty">Județ</label>
                            <input type="text" id="clientCounty" name="judet">
                        </div>
                        <div class="form-group">
                            <label for="clientCountry">Țară</label>
                            <input type="text" id="clientCountry" name="tara" value="România">
                        </div>
                    </div>
                </div>

                <div id="financiar" class="tab-content">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientIBAN">IBAN</label>
                            <input type="text" id="clientIBAN" name="iban">
                        </div>
                        <div class="form-group">
                            <label for="clientBank">Banca</label>
                            <input type="text" id="clientBank" name="banca">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientPaymentTerm">Termen de plată (zile)</label>
                            <input type="number" id="clientPaymentTerm" name="termen_plata" min="0" value="30">
                        </div>
                        <div class="form-group">
                            <label for="clientCreditLimit">Limită de credit</label>
                            <input type="number" id="clientCreditLimit" name="limita_credit" min="0" step="0.01">
                        </div>
                    </div>
                </div>

                <div class="modal-actions">
                    <button type="submit" class="btn-success">Salvează</button>
                    <button type="button" class="btn-secondary" id="cancelModal">Anulează</button>
                </div>
            </form>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/clienti.js') }}"></script>
</body>
</html>'''

    # Salvează toate paginile
    pages = {
        'bon_fiscal.html': bon_fiscal_html,
        'rapoarte.html': rapoarte_html,
        'configurare.html': configurare_html,
        'produse.html': produse_html,
        'clienti.html': clienti_html,
    }

    for filename, content in pages.items():
        with open(f"{templates_path}/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Creat: {filename}")

def create_complete_css(base_path):
    """Creează fișierul CSS complet"""
    css_content = '''/* ==========================================================================
   SmartBill CSS Framework
   ========================================================================== */

/* Reset și setup de bază */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #3498db;
    --primary-dark: #2980b9;
    --success-color: #27ae60;
    --warning-color: #f39c12;
    --danger-color: #e74c3c;
    --secondary-color: #95a5a6;
    --dark-color: #2c3e50;
    --light-color: #ecf0f1;
    --border-color: #ddd;
    --shadow: 0 2px 10px rgba(0,0,0,0.1);
    --border-radius: 4px;
    --transition: all 0.3s ease;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f8f9fa;
    color: #333;
    line-height: 1.6;
}

/* ==========================================================================
   Loader Styles
   ========================================================================== */
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
    animation: fadeIn 0.5s ease-in;
}

.loader-content {
    text-align: center;
    color: white;
}

.logo-loader {
    margin: 20px 0;
}

.logo-loader h2 {
    font-size: 32px;
    margin-bottom: 5px;
    font-weight: 300;
}

.logo-loader span {
    font-size: 14px;
    opacity: 0.8;
    letter-spacing: 2px;
}

.loader-spinner {
    width: 60px;
    height: 60px;
    border: 3px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s ease-in-out infinite;
    margin: 0 auto 20px;
}

.progress-bar {
    width: 200px;
    height: 4px;
    background: rgba(255,255,255,0.3);
    border-radius: 2px;
    margin: 20px auto 10px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: white;
    width: 0%;
    transition: width 0.3s ease;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* ==========================================================================
   Layout Principal
   ========================================================================== */
.container {
    display: flex;
    min-height: 100vh;
}

/* ==========================================================================
   Sidebar
   ========================================================================== */
.sidebar {
    width: 250px;
    background: var(--dark-color);
    color: white;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    z-index: 1000;
    transition: var(--transition);
}

.logo {
    padding: 20px;
    background: #34495e;
    text-align: center;
    border-bottom: 1px solid #34495e;
}

.logo h2 {
    font-size: 24px;
    margin-bottom: 5px;
    font-weight: 300;
}

.logo span {
    font-size: 12px;
    opacity: 0.8;
    letter-spacing: 1px;
}

.nav-menu {
    padding: 0;
}

.nav-item, .nav-subitem {
    display: block;
    padding: 12px 20px;
    color: white;
    text-decoration: none;
    transition: var(--transition);
    border-left: 3px solid transparent;
}

.nav-item:hover, .nav-subitem:hover {
    background: #34495e;
    border-left-color: var(--primary-color);
}

.nav-item.active {
    background: var(--primary-color);
    border-left-color: var(--primary-dark);
}

.nav-subitem.active {
    background: var(--primary-dark);
    border-left-color: white;
    padding-left: 40px;
}

.nav-item span {
    margin-right: 10px;
    font-size: 16px;
}

.nav-title {
    display: block;
    padding: 20px 20px 8px;
    font-size: 13px;
    font-weight: 600;
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.nav-subitem {
    padding-left: 40px;
    font-size: 14px;
    opacity: 0.9;
}

.nav-group {
    border-bottom: 1px solid #34495e;
    margin-bottom: 5px;
}

/* ==========================================================================
   Main Content
   ========================================================================== */
.main-content {
    flex: 1;
    margin-left: 250px;
    background: #f8f9fa;
    min-height: 100vh;
}

header {
    background: white;
    padding: 20px 30px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--shadow);
    position: sticky;
    top: 0;
    z-index: 100;
}

header h1 {
    font-size: 28px;
    color: var(--dark-color);
    font-weight: 300;
}

.breadcrumb {
    font-size: 14px;
    color: #666;
    margin-top: 5px;
}

.breadcrumb a {
    color: var(--primary-color);
    text-decoration: none;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 15px;
}

.user-info span {
    background: var(--primary-color);
    color: white;
    padding: 8px 16px;
    border-radius: var(--border-radius);
    font-size: 14px;
    font-weight: 500;
}

.user-dropdown {
    background: none;
    border: 1px solid var(--border-color);
    padding: 8px 12px;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 14px;
}

/* ==========================================================================
   Alert Banner
   ========================================================================== */
.alert-banner {
    background: linear-gradient(90deg, #f39c12, #e67e22);
    color: white;
    padding: 15px 30px;
    position: relative;
}

.alert-content {
    display: flex;
    align-items: flex-start;
    gap: 15px;
}

.alert-icon {
    font-size: 20px;
    margin-top: 2px;
}

.alert-text strong {
    display: block;
    margin-bottom: 5px;
    font-size: 16px;
}

.alert-text p {
    margin-bottom: 8px;
    opacity: 0.9;
}

.alert-link {
    color: white;
    text-decoration: underline;
    font-weight: 500;
}

.alert-link:hover {
    text-decoration: none;
}

/* ==========================================================================
   Dashboard
   ========================================================================== */
.dashboard-progress {
    display: flex;
    gap: 30px;
    padding: 20px 30px;
    background: white;
    border-bottom: 1px solid var(--border-color);
}

.progress-section {
    display: flex;
    align-items: center;
    gap: 15px;
}

.progress-label {
    font-size: 14px;
    color: #666;
    font-weight: 500;
}

.progress-circle {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: conic-gradient(var(--primary-color) 0deg 102deg, #e9ecef 102deg 360deg);
    position: relative;
}

.progress-circle::before {
    content: '';
    position: absolute;
    width: 60px;
    height: 60px;
    background: white;
    border-radius: 50%;
}

.progress-value {
    font-size: 18px;
    font-weight: bold;
    color: var(--dark-color);
    z-index: 1;
}

.progress-text {
    font-size: 11px;
    color: #666;
    z-index: 1;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
    padding: 30px;
}

/* ==========================================================================
   Stat Cards
   ========================================================================== */
.stat-card {
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: var(--shadow);
    text-align: center;
    transition: var(--transition);
    border-top: 4px solid var(--primary-color);
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

.stat-card.vanzari {
    border-top-color: var(--success-color);
}

.stat-card.cheltuieli {
    border-top-color: var(--danger-color);
}

.stat-card.sold-clienti {
    border-top-color: var(--warning-color);
}

.stat-card.facturi-neincasate {
    border-top-color: var(--secondary-color);
}

.stat-card h3 {
    font-size: 14px;
    color: #666;
    margin-bottom: 15px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stat-value {
    font-size: 36px;
    font-weight: 300;
    color: var(--dark-color);
    margin-bottom: 5px;
    line-height: 1;
}

.stat-currency {
    font-size: 14px;
    color: #666;
    margin-bottom: 15px;
    font-weight: 500;
}

.stat-description {
    font-size: 13px;
    color: #666;
    margin-bottom: 20px;
    line-height: 1.4;
}

/* ==========================================================================
   Activity Card
   ========================================================================== */
.activity-card {
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: var(--shadow);
    grid-column: 1 / -1;
    border-top: 4px solid var(--primary-color);
}

.activity-card h3 {
    font-size: 14px;
    color: #666;
    margin-bottom: 20px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.activity-list {
    space-y: 15px;
}

.activity-item {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    padding: 15px 0;
    border-bottom: 1px solid #f8f9fa;
}

.activity-item:last-child {
    border-bottom: none;
}

.activity-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--primary-color);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: white;
    flex-shrink: 0;
}

.activity-content {
    flex: 1;
}

.activity-action {
    display: block;
    font-weight: 500;
    color: var(--dark-color);
    margin-bottom: 5px;
}

.activity-time, .activity-date {
    display: block;
    color: #666;
    font-size: 12px;
    line-height: 1.3;
}

/* ==========================================================================
   Buttons
   ========================================================================== */
.btn-primary {
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: var(--transition);
    display: inline-flex;
    align-items: center;
    gap: 8px;
    text-decoration: none;
}

.btn-primary:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
}

.btn-success {
    background: var(--success-color);
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
    margin-right: 10px;
    transition: var(--transition);
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.btn-success:hover {
    background: #219a52;
    transform: translateY(-1px);
}

.btn-secondary {
    background: var(--secondary-color);
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
    transition: var(--transition);
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.btn-secondary:hover {
    background: #7f8c8d;
    transform: translateY(-1px);
}

.btn-add {
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 14px;
    white-space: nowrap;
}

.btn-option {
    background: #f8f9fa;
    border: 1px solid var(--border-color);
    padding: 8px 15px;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 14px;
    color: #666;
    transition: var(--transition);
}

.btn-option.active {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}

.btn-page {
    background: white;
    border: 1px solid var(--border-color);
    padding: 8px 12px;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 14px;
    margin: 0 5px;
}

.btn-page:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* ==========================================================================
   Forms
   ========================================================================== */
.form-container {
    padding: 30px;
    background: white;
    margin: 20px;
    border-radius: 8px;
    box-shadow: var(--shadow);
}

.form-alerts {
    margin-bottom: 25px;
}

.alert {
    padding: 15px;
    border-radius: var(--border-radius);
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 15px;
}

.alert-warning {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
}

.form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--border-color);
}

.form-options {
    display: flex;
    gap: 10px;
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

.form-group.large {
    grid-column: 1 / -1;
}

.form-group.full-width {
    grid-column: 1 / -1;
}

.form-group label {
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--dark-color);
    font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
    padding: 10px;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: 14px;
    transition: var(--transition);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.input-group {
    display: flex;
    gap: 10px;
    align-items: flex-end;
}

.input-group input {
    flex: 1;
}

.form-checkbox {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 20px 0;
}

.form-checkbox input[type="checkbox"] {
    width: 18px;
    height: 18px;
}

/* ==========================================================================
   Products Section
   ========================================================================== */
.products-section {
    margin: 30px 0;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    overflow: hidden;
}

.products-section h3 {
    padding: 15px 20px;
    margin: 0;
    background: #f8f9fa;
    border-bottom: 1px solid var(--border-color);
    color: var(--dark-color);
    font-size: 16px;
}

.products-toolbar {
    display: grid;
    grid-template-columns: 2fr 1fr 100px 120px 140px 1fr 1fr;
    gap: 10px;
    padding: 15px 20px;
    background: #fafbfc;
    border-bottom: 1px solid var(--border-color);
    align-items: end;
}

.products-toolbar input,
.products-toolbar select {
    padding: 8px 10px;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: 14px;
}

.products-table {
    width: 100%;
    border-collapse: collapse;
}

.products-table th,
.products-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #f8f9fa;
}

.products-table th {
    background: #f8f9fa;
    font-weight: 600;
    color: var(--dark-color);
    font-size: 14px;
}

.products-table tbody tr:hover {
    background: #f8f9fa;
}

.add-product-prompt {
    text-align: center;
    padding: 40px 20px;
    color: #666;
}

.add-product-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.info-icon {
    font-size: 18px;
    color: var(--primary-color);
}

/* ==========================================================================
   Additional Data Section
   ========================================================================== */
.additional-data {
    margin: 30px 0;
    padding: 20px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: #fafbfc;
}

.additional-data h3 {
    margin-bottom: 20px;
    color: var(--dark-color);
    font-size: 16px;
}

/* ==========================================================================
   Form Actions
   ========================================================================== */
.form-actions {
    text-align: right;
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}

/* ==========================================================================
   Content Areas
   ========================================================================== */
.content-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 30px;
    background: white;
    border-bottom: 1px solid var(--border-color);
}

.toolbar-left,
.toolbar-right {
    display: flex;
    gap: 10px;
    align-items: center;
}

.search-input {
    padding: 8px 12px;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: 14px;
    min-width: 200px;
}

.filter-select {
    padding: 8px 12px;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: 14px;
    min-width: 150px;
    background: white;
}

/* ==========================================================================
   Tables
   ========================================================================== */
.table-container {
    background: white;
    margin: 0 20px;
    border-radius: 8px;
    box-shadow: var(--shadow);
    overflow: hidden;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #f8f9fa;
}

.data-table th {
    background: #f8f9fa;
    font-weight: 600;
    color: var(--dark-color);
    font-size: 14px;
    position: sticky;
    top: 0;
}

.data-table tbody tr:hover {
    background: #f8f9fa;
}

.data-table tbody tr {
    transition: var(--transition);
}

/* ==========================================================================
   Pagination
   ========================================================================== */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    gap: 10px;
}

.page-info {
    margin: 0 15px;
    font-size: 14px;
    color: #666;
}

/* ==========================================================================
   Modals
   ========================================================================== */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 2000;
    animation: fadeIn 0.3s ease;
}

.modal.show {
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background: white;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    max-width: 500px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideIn 0.3s ease;
}

.modal-content.large {
    max-width: 800px;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
    margin: 0;
    color: var(--dark-color);
    font-size: 18px;
}

.modal-close {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-close:hover {
    color: var(--danger-color);
}

.modal-form {
    padding: 20px;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
    margin-top: 20px;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-50px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ==========================================================================
   Tabs
   ========================================================================== */
.form-tabs {
    display: flex;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 20px;
}

.tab-btn {
    background: none;
    border: none;
    padding: 12px 20px;
    cursor: pointer;
    font-size: 14px;
    color: #666;
    border-bottom: 2px solid transparent;
    transition: var(--transition);
}

.tab-btn.active {
    color: var(--primary-color);
    border-bottom-color: var(--primary-color);
}

.tab-btn:hover {
    color: var(--primary-color);
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

/* ==========================================================================
   Rapoarte Grid
   ========================================================================== */
.rapoarte-grid,
.config-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 30px;
    padding: 30px;
}

.raport-category,
.config-category {
    background: white;
    border-radius: 8px;
    box-shadow: var(--shadow);
    overflow: hidden;
}

.raport-category h3,
.config-category h3 {
    padding: 20px;
    margin: 0;
    background: #f8f9fa;
    border-bottom: 1px solid var(--border-color);
    color: var(--dark-color);
    font-size: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.raport-links,
.config-links {
    padding: 10px;
}

.raport-link,
.config-link {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    text-decoration: none;
    color: var(--dark-color);
    border-radius: var(--border-radius);
    transition: var(--transition);
    margin-bottom: 5px;
}

.raport-link:hover,
.config-link:hover {
    background: #f8f9fa;
    transform: translateX(5px);
}

.raport-icon,
.config-icon {
    font-size: 24px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8f9fa;
    border-radius: 50%;
    flex-shrink: 0;
}

.raport-link strong,
.config-link strong {
    display: block;
    margin-bottom: 5px;
    font-size: 15px;
}

.raport-link p,
.config-link p {
    margin: 0;
    font-size: 13px;
    color: #666;
    line-height: 1.3;
}

/* ==========================================================================
   Action Buttons in Tables
   ========================================================================== */
.action-buttons {
    display: flex;
    gap: 5px;
}

.btn-action {
    padding: 5px 8px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
    transition: var(--transition);
}

.btn-view {
    background: var(--primary-color);
    color: white;
}

.btn-edit {
    background: var(--warning-color);
    color: white;
}

.btn-delete {
    background: var(--danger-color);
    color: white;
}

.btn-action:hover {
    opacity: 0.8;
    transform: scale(1.05);
}

/* ==========================================================================
   Status Badges
   ========================================================================== */
.status-badge {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-active {
    background: #d4edda;
    color: #155724;
}

.status-inactive {
    background: #f8d7da;
    color: #721c24;
}

.status-pending {
    background: #fff3cd;
    color: #856404;
}

/* ==========================================================================
   Responsive Design
   ========================================================================== */
@media (max-width: 1200px) {
    .dashboard-grid {
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    }

    .products-toolbar {
        grid-template-columns: 1fr;
        gap: 10px;
    }
}

@media (max-width: 992px) {
    .sidebar {
        width: 200px;
    }

    .main-content {
        margin-left: 200px;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .rapoarte-grid,
    .config-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        height: auto;
        position: relative;
    }

    .main-content {
        margin-left: 0;
    }

    .dashboard-grid {
        grid-template-columns: 1fr;
        padding: 15px;
    }

    .content-toolbar {
        flex-direction: column;
        gap: 15px;
    }

    .toolbar-left,
    .toolbar-right {
        width: 100%;
        justify-content: center;
    }

    .search-input {
        min-width: auto;
        width: 100%;
    }

    header {
        padding: 15px 20px;
    }

    header h1 {
        font-size: 24px;
    }

    .form-container {
        margin: 10px;
        padding: 20px;
    }

    .table-container {
        margin: 0 10px;
        overflow-x: auto;
    }

    .modal-content {
        width: 95%;
        margin: 20px;
    }
}

@media (max-width: 480px) {
    .dashboard-progress {
        flex-direction: column;
        gap: 15px;
    }

    .stat-value {
        font-size: 28px;
    }

    .products-toolbar {
        padding: 10px;
    }

    .form-actions {
        text-align: center;
    }

    .btn-success,
    .btn-secondary {
        width: 100%;
        margin: 5px 0;
    }
}

/* ==========================================================================
   Utility Classes
   ========================================================================== */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.text-primary { color: var(--primary-color); }
.text-success { color: var(--success-color); }
.text-warning { color: var(--warning-color); }
.text-danger { color: var(--danger-color); }
.text-muted { color: #666; }

.bg-primary { background: var(--primary-color); }
.bg-success { background: var(--success-color); }
.bg-warning { background: var(--warning-color); }
.bg-danger { background: var(--danger-color); }
.bg-light { background: var(--light-color); }

.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 10px; }
.mb-2 { margin-bottom: 20px; }
.mb-3 { margin-bottom: 30px; }

.mt-0 { margin-top: 0; }
.mt-1 { margin-top: 10px; }
.mt-2 { margin-top: 20px; }
.mt-3 { margin-top: 30px; }

.p-0 { padding: 0; }
.p-1 { padding: 10px; }
.p-2 { padding: 20px; }
.p-3 { padding: 30px; }

.d-none { display: none; }
.d-block { display: block; }
.d-flex { display: flex; }
.d-grid { display: grid; }

.fade-in {
    animation: fadeIn 0.5s ease forwards;
}

.slide-up {
    animation: slideUp 0.3s ease forwards;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ==========================================================================
   Loading States
   ========================================================================== */
.loading {
    position: relative;
    pointer-events: none;
}

.loading::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255,255,255,0.8);
    display: flex;
    align-items: center;
    justify-content: center;
}

.loading::before {
    content: '';
    width: 20px;
    height: 20px;
    border: 2px solid var(--primary-color);
    border-top: 2px solid transparent;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    z-index: 1;
}

/* ==========================================================================
   Print Styles
   ========================================================================== */
@media print {
    .sidebar,
    .content-toolbar,
    .form-actions,
    .modal {
        display: none !important;
    }

    .main-content {
        margin-left: 0;
    }

    .form-container,
    .table-container {
        box-shadow: none;
        margin: 0;
    }
}'''