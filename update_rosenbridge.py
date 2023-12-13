from requests.auth import HTTPBasicAuth
import requests
import json
import os

base_url = "http://127.0.0.1:3030"
username = os.getenv('rosen_username')
password = os.getenv('rosen_password')

def get_info():
    url = f"{base_url}/api/info"
    auth = HTTPBasicAuth(username, password) if username and password else None
    response = requests.get(url, auth=auth)
    data = response.json()

    info_object = {
        "erg_amount": data["currentBalance"]/10**9,
        "permits_per_event": data["permitsPerEvent"],
        "active_permits": int(data["permitCount"]["active"]/data["permitsPerEvent"]),
        "total_permits": int(data["permitCount"]["total"]/data["permitsPerEvent"]),
        "health": data["health"],
        "erg_collateral": data["collateral"]["erg"]/10**9,
        "rsn_collateral": data["collateral"]["rsn"]/10**3
    }
    return info_object

def get_assets():
    url = f"{base_url}/api/address/assets"
    auth = HTTPBasicAuth(username, password) if username and password else None
    response = requests.get(url, auth=auth)
    data = response.json()

    item_names = {item["name"]: item["amount"] for item in data["items"]}
    assets_object = {
        "erg_amount": item_names.get("ERG")/10**9,
        "rsn_amount": item_names.get("RSN")/10**3,
        "collateral_nft_amount": next((item["amount"] for item in data["items"] if item["name"].startswith("WID")), None)
    }
    return assets_object

def get_health():
    url = f"{base_url}/api/health/status"
    auth = HTTPBasicAuth(username, password) if username and password else None
    response = requests.get(url, auth=auth)
    data = response.json()

    health_object = {
        "logs_status": next((item["status"] for item in data if item["id"] == "Error in Logs"), None),
        "logs_last_check": next((item["lastCheck"] for item in data if item["id"] == "Error in Logs"), None),
        "WID_status": next((item["status"] for item in data if item["id"] == "WID Token"), None),
        "WID_last_check": next((item["lastCheck"] for item in data if item["id"] == "WID Token"), None),
        "erg_status": next((item["status"] for item in data if item["id"] == "Native Asset ERG"), None),
        "erg_last_check": next((item["lastCheck"] for item in data if item["id"] == "Native Asset ERG"), None),
        "erg_scan_status": next((item["status"] for item in data if item["id"] == "Ergo Scanner Sync (Explorer)"), None),
        "erg_scan_last_check": next((item["lastCheck"] for item in data if item["id"] == "Ergo Scanner Sync (Explorer)"), None),
        "cardano_scan_status": next((item["status"] for item in data if item["id"] == "Cardano Scanner Sync (Koios)"), None),
        "cardano_scan_last_check": next((item["lastCheck"] for item in data if item["id"] == "Cardano Scanner Sync (Koios)"), None),
        "permits_status": next((item["status"] for item in data if item["id"] == "Available Reporting Permits"), None),
        "permits_last_check": next((item["lastCheck"] for item in data if item["id"] == "Available Reporting Permits"), None)
    }
    return health_object

def get_observations():
    url = f"{base_url}/api/observation"
    auth = HTTPBasicAuth(username, password) if username and password else None
    response = requests.get(url, auth=auth)
    data = response.json()

def get_events():
    url = f"{base_url}/api/events"
    auth = HTTPBasicAuth(username, password) if username and password else None
    response = requests.get(url, auth=auth)
    data = response.json()

def get_revenue():
    url = f"{base_url}/api/revenue" # also check /revenue/chart
    auth = HTTPBasicAuth(username, password) if username and password else None
    response = requests.get(url, auth=auth)
    data = response.json()

def get_statistics():
    url = f"{base_url}/api/statistics" 
    auth = HTTPBasicAuth(username, password) if username and password else None
    response = requests.get(url, auth=auth)
    data = response.json()

if __name__ == "__main__":
    try:
        data_to_write = {
            "info": get_info(),
            "assets": get_assets(),
            "health": get_health()
        }

    except Exception as e:
        print(e)

    with open('rosenbridge.json', 'w') as f:
        json.dump(data_to_write, f, indent=4)
