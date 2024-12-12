import pandas as pd
import os
from datetime import datetime

def process_csv_files(folder_path, output_folder):
    all_data = []
    current_date = datetime.now().strftime("%b%d")  # Ej: "Dec11"
    current_year = datetime.now().year               # Año actual

    # Iterar sobre todos los archivos CSV en la carpeta
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv") and current_date in file_name:
            # Leer archivo CSV
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, encoding="utf-8-sig")

            # Extraer metadatos del nombre del archivo
            # Suponemos nombres como "Amazon_Samsung_Products - Nov14 - 10pm.csv"
            parts = file_name.replace(".csv", "").split(" - ")
            
            # parts[0] = "Amazon_Samsung_Products"
            # parts[1] = "Nov14"
            # parts[2] = "10pm" (ejemplo)
            search_type = parts[0].replace("Amazon_", "").replace("_Products", "").strip()
            date_str = parts[1].strip()  # Ejemplo: "Nov14"
            time_str = parts[2].strip()  # Ejemplo: "10pm"
            
            # Convertir fecha a un formato estándar con el año actual
            date_obj = datetime.strptime(date_str, "%b%d")
            date_standard = f"{current_year}-{date_obj.month:02d}-{date_obj.day:02d}"
            
            # Añadir columnas de contexto
            df["search_type"] = search_type
            df["date"] = date_standard
            #df["time"] = time_str  # Descomenta si deseas agregar también la columna time

            # Añadir al conjunto general
            all_data.append(df)

    # Si no se encontraron datos para el día actual, no hacer nada
    if not all_data:
        print("No se encontraron archivos del día actual para unir.")
        return None

    # Combinar todos los DataFrames
    combined_data = pd.concat(all_data, ignore_index=True)

    # Crear el timestamp para el nombre del archivo
    timestamp = datetime.now().strftime("%b%d - %I%p")

    # Nombre del archivo de salida con fecha y hora
    output_file_name = f"data_unificada - {timestamp}.csv"
    output_file_path = os.path.join(output_folder, output_file_name)

    # Guardar en un archivo CSV unificado
    combined_data.to_csv(output_file_path, encoding="utf-8-sig", index=False)
    print(f"Datos combinados guardados en {output_file_path}")
    return combined_data

# Uso
folder_path = r"C:\Users\Angel\Documents\Programacion\Amazon\cleaned_data"
output_folder = r"C:\Users\Angel\Documents\Programacion\Amazon\dataset"

combined_data = process_csv_files(folder_path, output_folder)
