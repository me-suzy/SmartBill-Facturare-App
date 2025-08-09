#!/usr/bin/env python3
"""
Script simplu pentru a porni SmartBill App din Cursor
"""

import os
import sys
import time
import webbrowser
import threading

def main():
    print("🚀 Pornesc SmartBill App...")
    
    # Verifică dacă app.py există
    if not os.path.exists('app.py'):
        print("❌ Fișierul app.py nu a fost găsit!")
        return
    
    # Importă și pornește aplicația
    try:
        from app import SmartBillApp
        
        print("✅ Aplicația importată cu succes!")
        
        # Creează instanța aplicației
        app = SmartBillApp()
        
        # Deschide browserul după 3 secunde
        def open_browser():
            try:
                webbrowser.open('http://localhost:5000')
                print("✅ Browser deschis automat!")
            except Exception as e:
                print(f"⚠️ Nu s-a putut deschide browserul automat: {e}")
                print("🌐 Deschide manual: http://localhost:5000")
        
        threading.Timer(3, open_browser).start()
        
        # Pornește aplicația
        print("🌐 Aplicația pornește pe http://localhost:5000")
        app.run()
        
    except ImportError as e:
        print(f"❌ Eroare la importul aplicației: {e}")
        print("Asigură-te că toate dependențele sunt instalate!")
    except Exception as e:
        print(f"❌ Eroare la pornirea aplicației: {e}")

if __name__ == "__main__":
    main() 