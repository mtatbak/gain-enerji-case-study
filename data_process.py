import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
  
def eda(data):
    data["Pozitif Den. Fiyatı"] = data[["price","systemMarginalPrice"]].min(axis=1)*0.97
    data["Negatif Den. Fiyatı"] = data[["price","systemMarginalPrice"]].max(axis=1)*1.03
    data["Dengesizlik Miktarı"] = data["total"]-data["toplam"]
    data["GÖP Geliri (TL)"] = data["price"]*data["toplam"]
    
    conditions = [
    data["Dengesizlik Miktarı"] > 0,
    data["Dengesizlik Miktarı"] < 0,
    data["Dengesizlik Miktarı"] == 0]

    choices = [
    data["Dengesizlik Miktarı"] * data["Pozitif Den. Fiyatı"],
    data["Dengesizlik Miktarı"] * data["Negatif Den. Fiyatı"],
    0]

    data["Dengesizlik Tutarı (TL)"] = np.select(conditions, choices, default=0)
    
    data["Toplam (Net) Gelir (TL)"] =  data["GÖP Geliri (TL)"] + data["Dengesizlik Tutarı (TL)"]
    
    data["Dengesizlik Maliyeti (TL)"] = (data["total"] * data["price"]) - data["Toplam (Net) Gelir (TL)"]
    
    data["Birim Dengesizlik Maliyeti (TL/MWh)"] = np.where(
                data["total"] != 0, 
                data["Dengesizlik Maliyeti (TL)"] / data["total"], 
                None
)    
    return data

