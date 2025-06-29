#!/usr/bin/env python3
import requests
import sys
import time

def healthcheck():
    """Healthcheck usando Python requests"""
    try:
        # Tenta conectar ao endpoint de health
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend healthy")
            sys.exit(0)
        else:
            print(f"❌ Backend unhealthy - Status: {response.status_code}")
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend not responding - Connection refused")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("❌ Backend timeout")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Backend error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    healthcheck() 