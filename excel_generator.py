import xlsxwriter
from datetime import datetime, timedelta
import calendar
import pandas as pd
from openpyxl import load_workbook

def create_excel_template(filename, santral1='Santral_1', santral2='Santral_2'):
    workbook = xlsxwriter.Workbook(filename)
    
    # Excel formatlarını tanımla
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
    
    # Başlık sütunlarını tanımla
    headers = [
        'Tarih', 'Ay', 'Saat','PTF', 'SMF','Pozitif Den. Fiyatı', 'Negatif Den. Fiyatı',
        'Gün Öncesi Üretim Tahmini (KGÜP)', 'Gerçekleşen Üretim',
        'Dengesizlik Miktarı', 'GÖP Geliri (TL)',
        'Dengesizlik Tutarı  (TL)', 'Toplam (Net) Gelir (TL)',
        'Dengesizlik Maliyeti (TL)', 'Birim Dengesizlik Maliyeti (TL/MWh)']
    
    # İLK SANTRAL SHEET'İ OLUŞTUR
    ws1 = workbook.add_worksheet(santral1)
    
    # Başlıkları 0. satıra (ilk satır) yaz
    for col, header in enumerate(headers):
        ws1.write(0, col, header, header_format)
    
    # Sütun genişliklerini ayarla
    ws1.set_column('A:A', 12)  # Tarih sütunu
    ws1.set_column('B:B', 6)   # Ay sütunu
    ws1.set_column('C:C', 6)   # Saat sütunu
    ws1.set_column(3, len(headers)-1, 15)  # Diğer tüm sütunlar
    
    # 1. satırı tamamen boş bırak (hiçbir şey yazmıyoruz)
    
    # 2024 yılının tüm tarih ve saat verilerini oluştur
    # 2. satırdan başla (0: başlık, 1: boş, 2: ilk veri)
    current_row = 2
    total_hours = 0
    
    for month in range(1, 13):  # 12 ay
        last_day = calendar.monthrange(2024, month)[1]  # Ayın son günü
        for day in range(1, last_day + 1):  # Ayın tüm günleri
            for hour in range(24):  # Günün 24 saati
                date = datetime(2024, month, day)
                
                # Veriyi Excel'e yaz
                ws1.write(current_row, 0, date, date_format)      # A sütunu: Tarih
                ws1.write(current_row, 1, month, number_format)   # B sütunu: Ay
                ws1.write(current_row, 2, hour, number_format)    # C sütunu: Saat

                # Diğer sütunları boş bırak (daha sonra veri ile doldurulacak)
                for col in range(3, len(headers)):
                    ws1.write(current_row, col, '', number_format)
                
                current_row += 1
                total_hours += 1
    
    print(f"{santral1} - Toplam oluşturulan saat: {total_hours}")
    print(f"{santral1} - Son veri satırı: {current_row-1}")
    
    # İKİNCİ SANTRAL SHEET'İ OLUŞTUR (Aynı işlemleri tekrarla)
    ws2 = workbook.add_worksheet(santral2)
    
    # Başlıkları yaz
    for col, header in enumerate(headers):
        ws2.write(0, col, header, header_format)
    
    # Sütun genişliklerini ayarla
    ws2.set_column('A:A', 12)
    ws2.set_column('B:B', 6)
    ws2.set_column('C:C', 6)
    ws2.set_column(3, len(headers)-1, 15)
    
    # 1. satırı tamamen boş bırak (hiçbir şey yazmıyoruz)
    
    # 2. santral için de aynı tarih/saat verilerini oluştur
    # 2. satırdan başla (0: başlık, 1: boş, 2: ilk veri)
    current_row = 2
    
    for month in range(1, 13):
        last_day = calendar.monthrange(2024, month)[1]
        for day in range(1, last_day + 1):
            for hour in range(24):
                date = datetime(2024, month, day)
                
                ws2.write(current_row, 0, date, date_format)
                ws2.write(current_row, 1, month, number_format)
                ws2.write(current_row, 2, hour, number_format)
                
                for col in range(3, len(headers)):
                    ws2.write(current_row, col, '', number_format)
                
                current_row += 1
    
    print(f"{santral2} - Son veri satırı: {current_row-1}")
    
    # KARŞILAŞTIRMA SHEET'İ (Boş olarak oluştur)
    ws3 = workbook.add_worksheet('Karşılaştırma')
    
    
    
    
    
    workbook.close()
    print(f"Excel dosyası başarıyla oluşturuldu: {filename}")

def load_data_excel(df, excel_path, sheet_name, mapping):
    """
    DataFrame'deki verileri Excel dosyasının belirtilen sheet'ine yazar
    """
    wb = load_workbook(excel_path)
    ws = wb[sheet_name]

    # Excel'in ilk satırındaki başlıkları oku
    headers = [cell.value for cell in ws[1]]  # 1. satır (index 0) başlık satırı
    
    # Debug: Hangi başlıklar var kontrol et
    print(f"Sheet '{sheet_name}' başlıkları: {headers}")

    # Mapping'deki her sütun için işlem yap
    for df_column, excel_header in mapping.items():
        if excel_header not in headers:
            print(f"UYARI: '{excel_header}' başlığı bulunamadı, atlanıyor...")
            continue
        
        # Excel'de bu başlığın hangi sütunda olduğunu bul
        col_index = headers.index(excel_header) + 1  # +1 çünkü Excel 1-based indexing
        print(f"'{df_column}' → '{excel_header}' (Sütun {col_index})")
        
        # DataFrame'deki veriyi Excel'e yaz
        # 2. satırdan başla (0: başlık, 1: boş satır, 2: ilk veri)
        start_row = 3
        
        for i, value in enumerate(df[df_column]):
            excel_row = start_row + i  # 2, 3, 4, 5...
            ws.cell(row=excel_row, column=col_index, value=value)
    
    wb.save(excel_path)
    wb.close()
