import random
import requests
import pandas as pd
import time
import config
import streamlit as st 

# Geliştirilmiş POST fonksiyonu

def safe_post(url, headers=None, json=None, data=None, max_retries=5, timeout=60):
    for attempt in range(max_retries):
        try:
            # Exponential backoff + jitter
            if attempt > 0:
                wait_time = (2 ** attempt) + random.uniform(0, 2)
                print(f"Bekleniyor: {wait_time:.1f} saniye...")
                time.sleep(wait_time)
            
            # Session kullanarak connection pooling
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Connection': 'keep-alive'
            })
            
            response = session.post(url, headers=headers, json=json, data=data, timeout=timeout)
            response.raise_for_status()
            session.close()
            return response
            
        except (requests.exceptions.RequestException, ConnectionResetError, ConnectionError) as e:
            print(f"{attempt+1}. deneme başarısız: {e}")
            if attempt == max_retries - 1:
                print(f"Tüm denemeler başarısız oldu! URL: {url}")
                raise
            
    return None


def get_tgt():
    url = config.AUTH_URL
    headers = {
        "Accept": "text/plain",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {
        "username":f"{config.EPIAS_USER}",
        "password":f"{config.EPIAS_PASS}",
    }
    r = safe_post(url, data=body, headers=headers)
    return r.text

# Veri çekme fonksiyonları

def fetch_ptf(tgt, start_date, end_date):
    url = f"{config.BASE_URL}/markets/dam/data/mcp"
    headers = {
        "TGT": tgt,
        "Accept-Language": "en",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    body = {"startDate": start_date, "endDate": end_date}
    response = safe_post(url, headers=headers, json=body)
    data_ptf = response.json()
    df_ptf = pd.DataFrame(data_ptf["items"])
    return df_ptf[["date", "hour", "price"]]

def fetch_smf(tgt, start_date, end_date):
    url = f"{config.BASE_URL}/markets/bpm/data/system-marginal-price"
    headers = {
        "TGT": tgt,
        "Accept-Language": "en",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    body = {"startDate": start_date, "endDate": end_date}
    response = safe_post(url, headers=headers, json=body)
    data_smf = pd.DataFrame(response.json()["items"])
    data_smf['hour'] = pd.to_datetime(data_smf['hour']).dt.strftime('%H:%M')
    return data_smf

def fetch_kgup(tgt, organizationId, uevcbId, start_date, end_date, region="TR1"):
    url = f"{config.BASE_URL}/generation/data/dpp-first-version"
    headers = {
        "TGT": tgt,
        "Accept-Language": "en",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "organizationId": str(organizationId),
        "uevcbId": str(uevcbId),
        "region": region
    }
    response = safe_post(url, headers=headers, json=body)
    df = pd.DataFrame(response.json()["items"])
    df.rename(columns={"time": "hour"}, inplace=True)
    return df[["date", "hour", "toplam"]]

def fetch_uretim(tgt, powerPlantId, start_date, end_date):
    url = f"{config.BASE_URL}/generation/data/realtime-generation"
    headers = {
        "TGT": tgt,
        "Accept-Language": "en",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    body = {"startDate": start_date, "endDate": end_date, "powerPlantId": str(powerPlantId)}
    response = safe_post(url, headers=headers, json=body)
    df = pd.DataFrame(response.json()["items"])
    return df[["date", "hour", "total"]]

def fetch_monthly_data(tgt, organizationId, uevcbId, powerPlantId, start_date, end_date, region="TR1"):
    df_ptf = fetch_ptf(tgt, start_date, end_date)
    df_smf = fetch_smf(tgt, start_date, end_date)
    df_kgup = fetch_kgup(tgt, organizationId, uevcbId, start_date, end_date, region)
    df_uretim = fetch_uretim(tgt, powerPlantId, start_date, end_date)

    df_merged = df_ptf.merge(df_smf[["date","hour","systemMarginalPrice"]], on=["date","hour"], how="outer")
    df_merged = df_merged.merge(df_kgup, on=["date","hour"], how="outer")
    df_merged = df_merged.merge(df_uretim, on=["date","hour"], how="outer")
    return df_merged

def fetch_all_data_yearly(organizationId, uevcbId, powerPlantId, region="TR1"):
    tgt = get_tgt()  
    df_final = pd.DataFrame()
    import calendar

    for month in range(1, 13):
        last_day = calendar.monthrange(2024, month)[1]
        start_date = f"2024-{month:02d}-01T00:00:00+03:00"
        end_date = f"2024-{month:02d}-{last_day:02d}T23:00:00+03:00"
        try:
            df_monthly = fetch_monthly_data(tgt, organizationId, uevcbId, powerPlantId, start_date, end_date, region)
            df_final = pd.concat([df_final, df_monthly], ignore_index=True) if not df_final.empty else df_monthly.copy()
        except Exception as e:
            print(f"{month}. ay için hata oluştu: {e}")
            continue

    df_final = df_final.sort_values(by=["date","hour"]).reset_index(drop=True)
    return df_final
