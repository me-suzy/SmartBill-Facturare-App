import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    # Test API clienți
    print("=== TEST API CLIENTI ===")
    try:
        response = requests.get(f"{base_url}/api/get_clienti")
        print(f"Status: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Content: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Număr clienți: {len(data)}")
            if data:
                print(f"Primul client: {data[0]}")
        else:
            print(f"Eroare: {response.text}")
    except Exception as e:
        print(f"Eroare la testarea API clienți: {e}")
    
    print("\n=== TEST API PRODUSE ===")
    try:
        response = requests.get(f"{base_url}/api/get_produse")
        print(f"Status: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Content: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Număr produse: {len(data)}")
            if data:
                print(f"Primul produs: {data[0]}")
        else:
            print(f"Eroare: {response.text}")
    except Exception as e:
        print(f"Eroare la testarea API produse: {e}")

if __name__ == "__main__":
    test_api() 