import streamlit as st
import config 
from api_client import get_cached_tgt, fetch_all_data_yearly
from excel_generator import create_excel_template
import time  


def main():
    st.set_page_config(page_title="Gain Enerji", layout="wide")
   
    try:
        st.sidebar.image(config.IMAGE_PATH, width=225)
    except:
        pass  
   
    st.sidebar.title("Gain Enerji — Intern Analyst Case Study")
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
        
        st.info("Şeffaflık Platformuna bağlanılıyor...")
        tgt = get_cached_tgt()  # artık cache kullanılıyor        
        if not tgt:
            st.error("Bağlantı sağlanamadı!")
            return
        st.success("Bağlantı başarılı!")

        # 1. Santral verileri
        
        st.subheader(f"{plant1_name} verileri çekiliyor...")
        progress1 = st.progress(0)
        with st.spinner(f"{plant1_name} verileri çekiliyor, lütfen bekleyiniz..."):
            data1 = fetch_all_data_yearly(plant1["organizationId"], plant1["uevcbId"], plant1["powerPlantId"], region="TR1")
            for i in range(100):
                time.sleep(0.01)  
                progress1.progress(i + 1)
        st.success(f"{plant1_name} tamamlandı! ({len(data1)} kayıt)")

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

        # Genel Durumu
        
        st.subheader("Veri Durumu")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{plant1_name}**")
            st.write(f"PTF: {data1['price'].notna().sum()} kayıt")
            st.write(f"SMF: {data1['systemMarginalPrice'].notna().sum()} kayıt")
            st.write(f"KGÜP: {data1['toplam'].notna().sum()} kayıt")
            st.write(f"Üretim: {data1['total'].notna().sum()} kayıt")
        with col2:
            st.write(f"**{plant2_name}**")
            st.write(f"PTF: {data2['price'].notna().sum()} kayıt")
            st.write(f"SMF: {data2['systemMarginalPrice'].notna().sum()} kayıt")
            st.write(f"KGÜP: {data2['toplam'].notna().sum()} kayıt")
            st.write(f"Üretim: {data2['total'].notna().sum()} kayıt")
        # 3. Excel
        create_excel_template(
                                filename=f'{plant1_name}_vs_{plant2_name}.xlsx',
                                santral1=plant1_name,
                                santral2=plant2_name
                                                                                        )
        st.success("Excel Dosyası Oluşturuldu.")
        
if __name__ == "__main__":
    main()
