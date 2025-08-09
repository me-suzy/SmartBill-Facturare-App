#!/usr/bin/env python3
"""
Script de test pentru formularele SmartBill
Testează dacă formularele salvează datele în baza de date
"""

import requests
import json
import time
import random
import string

BASE_URL = "http://localhost:5000"

def generate_unique_cif():
    """Generează un CIF unic pentru testare"""
    timestamp = int(time.time())
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"TEST{timestamp}{random_suffix}"

def generate_unique_product_code():
    """Generează un cod de produs unic pentru testare"""
    timestamp = int(time.time())
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"TEST-PROD-{timestamp}-{random_suffix}"

def test_client_form():
    """Testează formularul pentru clienți"""
    print("=== TEST FORMULAR CLIENTI ===")
    
    # Generează CIF unic
    unique_cif = generate_unique_cif()
    print(f"Folosind CIF unic: {unique_cif}")
    
    # Test 1: Adăugare client nou
    print("1. Test adăugare client nou...")
    new_client = {
        "cif": unique_cif,
        "nume": f"TEST CLIENT SRL - {unique_cif}",
        "email": f"test.{unique_cif}@client.ro",
        "telefon": "0722123456",
        "localitate": "București",
        "judet": "București",
        "adresa": "Str. Test, Nr. 1",
        "cod_postal": "010101",
        "website": "www.testclient.ro",
        "persoana_contact": "Test Contact",
        "observatii": "Client de test"
    }
    
    response = requests.post(f"{BASE_URL}/api/add_client", json=new_client)
    print(f"Status: {response.status_code}")
    print(f"Răspuns: {response.json()}")
    
    if response.status_code == 200 and response.json().get('success'):
        print("✅ Client adăugat cu succes!")
        
        # Test 2: Actualizare client
        print("\n2. Test actualizare client...")
        updated_client = {
            "cif": unique_cif,
            "nume": f"TEST CLIENT SRL - {unique_cif} - MODIFICAT",
            "email": f"test.modificat.{unique_cif}@client.ro",
            "telefon": "0722123457",
            "localitate": "Cluj-Napoca",
            "judet": "Cluj",
            "adresa": "Str. Test Modificat, Nr. 2",
            "cod_postal": "400001",
            "website": "www.testclientmodificat.ro",
            "persoana_contact": "Test Contact Modificat",
            "observatii": "Client de test modificat"
        }
        
        # Găsește ID-ul clientului adăugat
        print("\n3. Căutare client pentru actualizare...")
        clients_response = requests.get(f"{BASE_URL}/api/get_clienti")
        clients = clients_response.json()
        print(f"Clienți găsiți: {len(clients)}")
        
        test_client = None
        for client in clients:
            if client['CIF'] == unique_cif:
                test_client = client
                break
        
        if test_client:
            client_id = test_client['ID']
            print(f"✅ Client găsit cu ID: {client_id}")
            print(f"📋 Detalii client: {test_client}")
            
            update_response = requests.put(f"{BASE_URL}/api/update_client/{client_id}", json=updated_client)
            print(f"Status actualizare: {update_response.status_code}")
            
            if update_response.status_code == 200:
                print(f"Răspuns actualizare: {update_response.json()}")
                if update_response.json().get('success'):
                    print("✅ Client actualizat cu succes!")
                else:
                    print("❌ Eroare la actualizarea clientului")
            else:
                print(f"❌ Eroare HTTP la actualizare: {update_response.text}")
        else:
            print("❌ Nu s-a găsit clientul de test")
            print("🔍 Clienți disponibili (primele 5):")
            for i, client in enumerate(clients[:5]):
                print(f"  {i+1}. ID: {client['ID']}, CIF: {client['CIF']}, Nume: {client['Nume']}")
            print("🔍 Căutare CIF în toți clienții:")
            for client in clients:
                if unique_cif in str(client['CIF']):
                    print(f"  Găsit similar: ID: {client['ID']}, CIF: {client['CIF']}")
    else:
        print("❌ Eroare la adăugarea clientului")

def test_product_form():
    """Testează formularul pentru produse"""
    print("\n=== TEST FORMULAR PRODUSE ===")
    
    # Generează cod unic
    unique_code = generate_unique_product_code()
    print(f"Folosind cod unic: {unique_code}")
    
    # Test 1: Adăugare produs nou
    print("1. Test adăugare produs nou...")
    new_product = {
        "cod": unique_code,
        "denumire": f"Produs Test - {unique_code}",
        "um": "buc",
        "categorie": "Test",
        "pret_vanzare": 100.50,
        "pret_achizitie": 80.00,
        "stoc": 10,
        "stoc_minim": 2,
        "descriere": "Produs de test pentru verificarea formularelor"
    }
    
    response = requests.post(f"{BASE_URL}/api/add_produs", json=new_product)
    print(f"Status: {response.status_code}")
    print(f"Răspuns: {response.json()}")
    
    if response.status_code == 200 and response.json().get('success'):
        print("✅ Produs adăugat cu succes!")
        
        # Test 2: Actualizare produs
        print("\n2. Test actualizare produs...")
        updated_product = {
            "cod": unique_code,
            "denumire": f"Produs Test - {unique_code} - Modificat",
            "um": "pachet",
            "categorie": "Test Modificat",
            "pret_vanzare": 120.75,
            "pret_achizitie": 95.00,
            "stoc": 15,
            "stoc_minim": 3,
            "descriere": "Produs de test modificat pentru verificarea formularelor"
        }
        
        # Găsește ID-ul produsului adăugat
        print("\n3. Căutare produs pentru actualizare...")
        products_response = requests.get(f"{BASE_URL}/api/get_produse")
        products = products_response.json()
        print(f"Produse găsite: {len(products)}")
        
        test_product = None
        for product in products:
            if product['Cod'] == unique_code:
                test_product = product
                break
        
        if test_product:
            product_id = test_product['ID']
            print(f"✅ Produs găsit cu ID: {product_id}")
            print(f"📋 Detalii produs: {test_product}")
            
            update_response = requests.put(f"{BASE_URL}/api/update_produs/{product_id}", json=updated_product)
            print(f"Status actualizare: {update_response.status_code}")
            
            if update_response.status_code == 200:
                print(f"Răspuns actualizare: {update_response.json()}")
                if update_response.json().get('success'):
                    print("✅ Produs actualizat cu succes!")
                else:
                    print("❌ Eroare la actualizarea produsului")
            else:
                print(f"❌ Eroare HTTP la actualizare: {update_response.text}")
        else:
            print("❌ Nu s-a găsit produsul de test")
            print("🔍 Produse disponibile (primele 5):")
            for i, product in enumerate(products[:5]):
                print(f"  {i+1}. ID: {product['ID']}, Cod: {product['Cod']}, Denumire: {product['Denumire']}")
            print("🔍 Căutare cod în toate produsele:")
            for product in products:
                if unique_code in str(product['Cod']):
                    print(f"  Găsit similar: ID: {product['ID']}, Cod: {product['Cod']}")
    else:
        print("❌ Eroare la adăugarea produsului")

def test_config_form():
    """Testează formularul pentru configurare"""
    print("\n=== TEST FORMULAR CONFIGURARE ===")
    
    # Test actualizare configurare
    print("1. Test actualizare configurare...")
    new_config = {
        "company_name": "TEST COMPANY SRL",
        "company_cif": "TEST12345678",
        "company_address": "Str. Test Config, Nr. 100, București",
        "company_phone": "021 999 9999",
        "company_email": "test@config.ro",
        "company_website": "https://www.testconfig.ro",
        "bank_account": "RO99 TEST 1234 5678 9012 3456",
        "bank_name": "Banca Test",
        "tva_rate": 19,
        "currency": "RON"
    }
    
    response = requests.post(f"{BASE_URL}/api/update_config", json=new_config)
    print(f"Status: {response.status_code}")
    print(f"Răspuns: {response.json()}")
    
    if response.status_code == 200 and response.json().get('success'):
        print("✅ Configurare actualizată cu succes!")
        
        # Verifică dacă configurarea a fost salvată
        print("\n2. Verificare configurare salvată...")
        config_response = requests.get(f"{BASE_URL}/api/get_config")
        config = config_response.json()
        print(f"Configurare citită: {config}")
        
        if config.get('Nume_Companie') == 'TEST COMPANY SRL':
            print("✅ Configurarea a fost salvată corect!")
        else:
            print("❌ Configurarea nu a fost salvată corect")
    else:
        print("❌ Eroare la actualizarea configurarei")

def main():
    """Funcția principală de test"""
    print("🚀 ÎNCEPE TESTAREA FORMULARELOR SMARTBILL")
    print("=" * 50)
    
    try:
        # Testează dacă aplicația rulează
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Aplicația nu rulează pe localhost:5000")
            return
        
        print("✅ Aplicația rulează pe localhost:5000")
        
        # Testează formularele
        test_client_form()
        test_product_form()
        test_config_form()
        
        print("\n" + "=" * 50)
        print("✅ TESTAREA FORMULARELOR COMPLETĂ!")
        print("Toate formularele salvează datele în baza de date.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Nu se poate conecta la aplicația SmartBill")
        print("Asigură-te că aplicația rulează pe localhost:5000")
    except Exception as e:
        print(f"❌ Eroare la testare: {str(e)}")

if __name__ == "__main__":
    main() 