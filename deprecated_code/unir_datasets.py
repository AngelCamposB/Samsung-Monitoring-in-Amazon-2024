import pandas as pd
import os
from datetime import datetime

def process_csv_files(folder_path, output_file, current_year=2025):
    all_data = []

    # Iterar sobre todos los archivos CSV en la carpeta
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            # Leer archivo CSV
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, encoding="utf-8-sig")
            
            # Extraer metadatos del nombre del archivo
            # Suponemos nombres como "Amazon_Samsung_Products - Nov14 - 10pm.csv"
            parts = file_name.replace(".csv", "").split(" - ")
            search_type = parts[0].replace("Amazon_", "").replace("_Products", "").strip()
            date_str = parts[1].strip()  # Ejemplo: "Nov14"
            time_str = parts[2].strip()  # Ejemplo: "10pm"
            
            # Convertir fecha a un formato estándar con el año actual
            date_obj = datetime.strptime(date_str, "%b%d")
            date_standard = f"{current_year}-{date_obj.month:02d}-{date_obj.day:02d}"  # Año manualmente
            
            # Añadir columnas de contexto
            df["search_type"] = search_type
            df["date"] = date_standard
            #df["time"] = time_str
            
            # Añadir al conjunto general
            all_data.append(df)
    
    # Combinar todos los DataFrames
    combined_data = pd.concat(all_data, ignore_index=True)
    
    # Guardar en un archivo CSV unificado
    combined_data.to_csv(output_file, encoding="utf-8-sig", index=False)
    print(f"Datos combinados guardados en {output_file}")
    return combined_data

# Uso
folder_path = r"C:\Users\Angel\Desktop\Amazon\data_cleaning_process\data_cleaned_unique - copia"
output_file = "data_unificada.csv"
combined_data = process_csv_files(folder_path, output_file, current_year=2024)
