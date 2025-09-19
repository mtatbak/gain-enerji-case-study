import requests
import pandas as pd

url = "https://giris.epias.com.tr/cas/v1/tickets"
headers = {
    "Accept": "text/plain", 
    "Content-Type": "application/x-www-form-urlencoded"
}
body = {
    "username":"mtatbak54@gmail.com", # Şeffaflık Platformuna kayıt olurken belirlediğiniz kullanıcı adınız.
    "password":"Qazwsx!123",      # Şeffaflık Platformuna kayıt olurken belirlediğiniz şifreniz.
}
r = requests.post(url, data=body, headers=headers)

tgt = r.text

#print(tgt) TGT-14754978-P8tHEskER7afnAH-satv7PlsK0dT2kRbYBvm6hwHQsMqFOi-UM2-1vJ2oX-5wYCNmuk-cas-7dc76c888-d9cdw

import requests
import pandas as pd

def fetch_data(plant, tgt, data_type):
    """
    plant: santral sözlüğü
    tgt: Ticket Granting Ticket
    data_type: "PTF", "SMF", "KGÜP", "Üretim"
    """

    url_dict = {
        "PTF": "https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/mcp",
        "SMF": "https://seffaflik.epias.com.tr/electricity-service/v1/markets/bpm/data/system-marginal-price",
        "KGÜP": "https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/dpp-first-version",
        "Üretim": "https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/realtime-generation"
    }

    headers = {
        "TGT": tgt,
        "Accept-Language": "en",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    if data_type in ["PTF", "SMF"]:
        body = {"startDate": "2024-01-01T00:00:00+03:00",
                "endDate": "2024-12-31T23:00:00+03:00"}
    elif data_type == "KGÜP":
        body = {
            "startDate": "2024-01-01T00:00:00+03:00",
            "endDate": "2024-12-31T23:00:00+03:00",
            "organizationId": plant["organizationId"],
            "uevcbId": plant["uevcbId"],
            "region": "TR1"
        }
    elif data_type == "Üretim":
        body = {
            "startDate": "2024-01-01T00:00:00+03:00",
            "endDate": "2024-12-31T23:00:00+03:00",
            "powerPlantId": plant["powerPlantId"]
        }

    response = requests.post(url_dict[data_type], headers=headers, json=body)
    data = response.json()

    # JSON yapısını güvenli hale getir
    if isinstance(data, dict):
        # Eğer dict içinde 'result' veya 'data' varsa
        if "result" in data:
            data = data["result"]
        elif "data" in data:
            data = data["data"]
        else:
            data = [data]  # tek dict'i listeye çevir

    elif not isinstance(data, list):
        data = [data]  # list değilse listeye çevir

    df = pd.DataFrame(data)
    return df
