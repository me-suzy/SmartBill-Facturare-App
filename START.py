#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartBill Launcher Script
========================
"""

import os
import sys
from pathlib import Path

def main():
    print("🚀 Pornire SmartBill...")

    # Schimbă directorul de lucru
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    try:
        # Importă și pornește aplicația
        from app import SmartBillApp

        print("✅ SmartBill se încarcă...")
        app = SmartBillApp()
        app.run()

    except ImportError as e:
        print(f"❌ Eroare import: {e}")
        print("💡 Instalează dependințele: pip install Flask pandas openpyxl")
        input("Apasă ENTER...")
    except Exception as e:
        print(f"❌ Eroare: {e}")
        input("Apasă ENTER...")

if __name__ == "__main__":
    main()
