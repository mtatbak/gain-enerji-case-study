import streamlit as st
import pandas as pd
from config import power_plants  
import requests
from fetch_data import fetch_data 
from data_procces import process_plant_data
from excel_generator import save_to_excel


def main():
    st.title("")
    col1,col2 = st.columns(2)

    IMAGE_PATH = "gainweb.png"
    st.sidebar.image(IMAGE_PATH,width=225)
    st.sidebar.title("Gain Enerji — Intern Analyst Case Study")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Geliştirici:** Mehmet TATBAK")
    
    plant_names = [plant["powerPlantName"] for plant in power_plants]
    
    with col1:
        plant1_name = st.selectbox("1. Santral Seçimi", plant_names, index=0)
    with col2:
        plant2_name = st.selectbox("2. Santral Seçimi", plant_names, index=0)            
    
    
    run_analysis = st.button("Çalıştır")
    
    if run_analysis:
        plant1 = next(p for p in power_plants if p["powerPlantName"] == plant1_name)
        plant2 = next(p for p in power_plants if p["powerPlantName"] == plant2_name)
        
        tgt = ""
    
        dfs_plant1 = process_plant_data(plant1, tgt)
        dfs_plant2 = process_plant_data(plant2, tgt)
        file_name = save_to_excel(plant1_name, plant2_name, dfs_plant1, dfs_plant2)
        st.success(f"Excel dosyası oluşturuldu: {file_name}")
    
if __name__ == "__main__":
    main()
