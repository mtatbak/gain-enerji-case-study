import streamlit as st
import config 
from api_client import get_tgt, fetch_all_data_yearly
from excel_generator import create_excel_template,load_data_excel
import time 
from data_process import eda 


def main():
    st.set_page_config(page_title="Gain Enerji", layout="wide")
   
    try:
        st.sidebar.image(config.IMAGE_PATH, width=225)
    except:
        pass  
   
    st.sidebar.title("Intern Analyst Case Study")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Geliştirici:** Mehmet TATBAK")

   
    st.title("Gain Enerji - Santral Karşılaştırma")
   
    col1, col2 = st.columns(2)
    plant_names = [p["powerPlantName"] for p in config.power_plants]
   
    with col1:
        plant1_name = st.selectbox("1. Santral Seçimi", plant_names)
    with col2:
        plant2_name = st.selectbox("2. Santral Seçimi", plant_names, index=1)
   
    st.markdown("---")
   
    if st.button("Çalıştır", type="primary", use_container_width=True):
        if plant1_name == plant2_name:
            st.warning("Lütfen farklı santraller seçiniz!")
            return
       
        plant1 = next(p for p in config.power_plants if p["powerPlantName"] == plant1_name)
        plant2 = next(p for p in config.power_plants if p["powerPlantName"] == plant2_name)
        
        st.sidebar.info("EPİAŞ Şeffaflık Platformuna bağlanılıyor...")
        tgt = get_tgt()          
        if not tgt:
            st.error("Bağlantı sağlanamadı!")
            return
        st.sidebar.success("Bağlantı başarılı!")

        # 1. Santral verileri
        
        st.subheader(f"{plant1_name} verileri çekiliyor...")
        progress1 = st.progress(0)
        with st.spinner(f"{plant1_name} verileri çekiliyor, lütfen bekleyiniz..."):
            data1 = fetch_all_data_yearly(plant1["organizationId"], plant1["uevcbId"], plant1["powerPlantId"], region="TR1")
            for i in range(100):
                time.sleep(0.01)  
                progress1.progress(i + 1)
        st.success(f"{plant1_name} tamamlandı! ({len(data1)} kayıt)")
        
        data1 = eda(data1)
        
        # 2. Santral verileri
        
        st.subheader(f"{plant2_name} verileri çekiliyor...")
        progress2 = st.progress(0)
        with st.spinner(f"{plant2_name} verileri çekiliyor, lütfen bekleyiniz..."):
            data2 = fetch_all_data_yearly(plant2["organizationId"], plant2["uevcbId"], plant2["powerPlantId"], region="TR1")
            for i in range(100):
                time.sleep(0.01)
                progress2.progress(i + 1)
        st.success(f"{plant2_name} tamamlandı! ({len(data2)} kayıt)")

        st.success("Tüm veriler çekildi!")
        
        data2 = eda(data2)

        
        
        # 3. Excel
        filename = f"{plant1_name}_vs_{plant2_name}.xlsx"
        
        create_excel_template(filename=filename,
                              santral1=plant1_name,
                              santral2=plant2_name)
        
        st.success("Excel Dosyası Oluşturuldu.")
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
        
        load_data_excel(data1, filename, plant1_name, mapping)
        
        load_data_excel(data2, filename, plant2_name, mapping)

        with open(filename, "rb") as f:
            data = f.read()

        st.download_button(
            label="Excel İndir (.xlsx)",
            data=data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    
if __name__ == "__main__":
    main()
