import requests

API_KEY = "858b260f277796a0419c374182976be83ebbe0e5569d73d13ea9621470236ac64bbeab67ee66ca37"


def check_ip(ip):

    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        print("========== AbuseIPDB Response ==========")
        print("Status Code:", response.status_code)

        data = response.json()
        print(data)
        print("========================================")

        # API error
        if response.status_code != 200:
            return {
                "error": True,
                "message": data
            }

        return data

    except requests.exceptions.Timeout:
        return {
            "error": True,
            "message": "Connection timed out."
        }

    except requests.exceptions.ConnectionError:
        return {
            "error": True,
            "message": "Unable to connect to AbuseIPDB."
        }

    except Exception as e:
        return {
            "error": True,
            "message": str(e)
        }