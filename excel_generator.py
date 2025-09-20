import xlsxwriter
from datetime import datetime, timedelta
import calendar

def create_excel_template(filename='Karşılaştırmalı_Analiz_Excel.xlsx', santral1='Santral_1', santral2='Santral_2'):
    workbook = xlsxwriter.Workbook(filename)
    
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#D7E4BC',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
    })
    
    date_format = workbook.add_format({
        'num_format': 'dd/mm/yyyy',
        'border': 1,
        'align': 'center'
    })
    
    number_format = workbook.add_format({
        'border': 1,
        'align': 'center'
    })
    
    # Santral_1 sheet'i oluştur
    ws1 = workbook.add_worksheet(santral1)
    
    headers1 = [
        'Tarih', 'Ay', 'Saat', 'PTF', 'SMF',
        'Pozitif Den. Fiyatı', 'Negatif Den. Fiyatı',
        'Gün Öncesi Üretim Tahmini (KGUP)', 'Gerçekleşen Üretim',
        'Dengesizlik Miktarı', 'GÖP Geliri (TL)',
        'Dengesizlik Tutarı (TL)', 'Toplam (Net) Gelir (TL)',
        'Dengesizlik Maliyeti (TL)', 'Birim Dengesizlik Maliyeti (TL/MWh)'
    ]
    
    # Başlıkları yaz
    for col, header in enumerate(headers1):
        ws1.write(0, col, header, header_format)
    
    # Sütun genişlikleri
    ws1.set_column('A:A', 12)  # Tarih
    ws1.set_column('B:B', 6)   # Ay  
    ws1.set_column('C:C', 6)   # Saat
    ws1.set_column('D:O', 15)  # Diğer sütunlar
    
    # 2024 yılı için tarih ve saat verilerini doldur
    row = 1
    for month in range(1, 13):
        last_day = calendar.monthrange(2024, month)[1]
        for day in range(1, last_day + 1):
            for hour in range(24):
                date = datetime(2024, month, day)
                ws1.write(row, 0, date, date_format)  # Tarih
                ws1.write(row, 1, month, number_format)  # Ay
                ws1.write(row, 2, hour, number_format)  # Saat
                # Diğer sütunları boş bırak
                for col in range(3, len(headers1)):
                    ws1.write(row, col, '', number_format)
                row += 1
    
    print(f"{santral1} toplam satır sayısı: {row-1}")
    
    # Santral_2 sheet'i oluştur
    ws2 = workbook.add_worksheet(santral2)
    
    # Aynı başlıkları kullan
    for col, header in enumerate(headers1):
        ws2.write(0, col, header, header_format)
    
    # Sütun genişlikleri
    ws2.set_column('A:A', 12)
    ws2.set_column('B:B', 6) 
    ws2.set_column('C:C', 6)
    ws2.set_column('D:O', 15)
    
    # 2024 yılı için tarih ve saat verilerini doldur
    row = 1
    for month in range(1, 13):
        last_day = calendar.monthrange(2024, month)[1]
        for day in range(1, last_day + 1):
            for hour in range(24):
                date = datetime(2024, month, day)
                ws2.write(row, 0, date, date_format)
                ws2.write(row, 1, month, number_format)
                ws2.write(row, 2, hour, number_format)
                for col in range(3, len(headers1)):
                    ws2.write(row, col, '', number_format)
                row += 1
    
    print(f"{santral2} toplam satır sayısı: {row-1}")
    
    # Karşılaştırma sheet'i oluştur
    ws3 = workbook.add_worksheet('Karşılaştırma')
    
    
    workbook.close()
    print(f"Excel dosyası oluşturuldu: {filename}")
    print(f"2024 yılı toplam saat: {366 * 24} (leap year)")

