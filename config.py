power_plants = [
    {
        "powerPlantName" : "MASLAKTEPE RES",
        "organizationId" : 12717,
        "powerPlantId" : 2468,
        "uevcbId" : 3207214
    },
    {
        "powerPlantName" : "EBER RES",
        "organizationId" : 12517,
        "powerPlantId" : 2316,
        "uevcbId" : 3217197
    },
    {
        "powerPlantName" : "YANBOLU HES",
        "organizationId" : 8801,
        "powerPlantId" : 1884,
        "uevcbId" : 2813560
    },
    {
        "powerPlantName" : "MELİKOM HES",
        "organizationId" : 9709,
        "powerPlantId" : 2142,
        "uevcbId" : 3196990
    }
]

IMAGE_PATH = "media\gainweb.png"

AUTH_URL = "https://giris.epias.com.tr/cas/v1/tickets"

BASE_URL = "https://seffaflik.epias.com.tr/electricity-service/v1"

EPIAS_USER="USERNAME"
EPIAS_PASS="PASSWORD"

mapping = {
        "price": "PTF",
        "systemMarginalPrice": "SMF", 
        "toplam": "Gün Öncesi Üretim Tahmini (KGÜP)",
        "total": "Gerçekleşen Üretim",
        "Pozitif Den. Fiyatı": "Pozitif Den. Fiyatı",
        "Negatif Den. Fiyatı" : "Negatif Den. Fiyatı",
        "Dengesizlik Miktarı" : "Dengesizlik Miktarı",
        "GÖP Geliri (TL)" : "GÖP Geliri (TL)",
        "Dengesizlik Tutarı (TL)" : "Dengesizlik Tutarı  (TL)",
        "Toplam (Net) Gelir (TL)" : "Toplam (Net) Gelir (TL)",
        "Dengesizlik Maliyeti (TL)" :"Dengesizlik Maliyeti (TL)",
        "Birim Dengesizlik Maliyeti (TL/MWh)" : "Birim Dengesizlik Maliyeti (TL/MWh)"
        }
