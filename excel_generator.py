import pandas as pd

def save_to_excel(plant1_name, plant2_name, dfs_plant1, dfs_plant2, file_name="Karsilastirmali_Analiz_2024.xlsx"):
    """
    dfs_plant1 / dfs_plant2: {
        "PTF": df,
        "SMF": df,
        "KGÜP": df,
        "Üretim": df
    }
    """
    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        # Plant 1 sheet'leri
        for key, df in dfs_plant1.items():
            sheet_name = f"{plant1_name}_{key}"[:31]  # Excel sheet adı max 31 karakter
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Plant 2 sheet'leri
        for key, df in dfs_plant2.items():
            sheet_name = f"{plant2_name}_{key}"[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return file_name
