import requests

API_KEY = "04bb7c27afd3af200eb67bc36758cd92b209cab90270d96142965d5ee459221a"

def check_ip(ip):

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    headers = {
        "x-apikey": API_KEY
    }

    response = requests.get(url, headers=headers)

    print("========== VirusTotal Response ==========")
    print(response.status_code)
    print(response.json())
    print("=========================================")

    return response.json()