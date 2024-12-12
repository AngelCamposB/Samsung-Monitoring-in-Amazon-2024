import pandas as pd
import os
import numpy as np
from datetime import datetime

# (3) Función para limpiar y convertir a float las columnas
def clean_and_convert(value):
    value = str(value)
    value = value.replace('$', '').replace(',', '').replace('%', '').replace(' de 5 estrellas', '')
    try:
        value = float(value)
        return float(value)
    except ValueError:
        print(f"Error al convertir el valor '{value}' a float.")
        return None  # Manejar valores no numéricos

# Rutas de las carpetas
ruta_carpeta = r"C:\Users\Angel\Documents\Programacion\Amazon\raw_data"
ruta_carpeta_cleaned = r"C:\Users\Angel\Documents\Programacion\Amazon\cleaned_data"

# Crear carpeta cleaned_data si no existe
if not os.path.exists(ruta_carpeta_cleaned):
    os.makedirs(ruta_carpeta_cleaned)

# Obtener la fecha actual en el mismo formato usado en los nombres de archivo (ej: "Dec10")
current_date = datetime.now().strftime("%b%d")

# Recorremos todos los archivos CSV en la carpeta raw_data
for archivo in os.listdir(ruta_carpeta):
    # Procesar sólo si el archivo del día actual está en el nombre
    # Ejemplo: "Amazon_Samsung_Products - Dec10 - 07PM.csv" contiene "Dec10"
    if archivo.endswith(".csv") and current_date in archivo:
        ruta_archivo = os.path.join(ruta_carpeta, archivo)
        
        # Intentar leer el archivo con diferentes codificaciones
        try:
            df = pd.read_csv(ruta_archivo, encoding='utf-8-sig')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(ruta_archivo, encoding='latin-1')
                print("Latin-1")
            except UnicodeDecodeError:
                df = pd.read_csv(ruta_archivo, errors='ignore')
                print("Warning: Some characters may have been ignored due to encoding issues.")

        print(f"\n------- ARCHIVO: {archivo} -------")
        
        # 1. Agregar la columna 'buen_fin_discount' en posición 8
        nueva_columna = "buen_fin_discount"
        valor_a_agregar = "No"
        try:
            df.insert(7, nueva_columna, valor_a_agregar)
            print(f"1. Se agregó la columna: '{nueva_columna}' ")
        except ValueError:
            print(f"1. El archivo ya tiene la columna: '{nueva_columna}' ")

        # 1.2 Agregar la columna 'black_friday_discount' en posición 9
        nueva_columna = "black_friday_discount"
        valor_a_agregar = "No"
        try:
            df.insert(8, nueva_columna, valor_a_agregar)
            print(f"1.2. Se agregó la columna: '{nueva_columna}' ")
        except ValueError:
            print(f"1.2. El archivo ya tiene la columna: '{nueva_columna}' ")

        # 2. Aplica la función para limpiar y convertir las columnas a numéricas
        for col in ['price', 'original_price', 'discount_amount', 'discount_percentage', 'reviews_count', 'rating']:
            df[col] = df[col].apply(clean_and_convert)
        print("2. Columnas convertidas a float")

        # 3. Si price == original_price, discount_amount y discount_percentage = 0
        df.loc[df['price'] == df['original_price'], ['discount_amount', 'discount_percentage']] = 0
        print("3. discount_amount y discount_percentage corregidos -> 0 donde price == original_price")

        # 4. Agregar columna 'has_discount'
        try:
            df.insert(7, 'has_discount', df['discount_amount'] > 0)
            df['has_discount'] = df['has_discount'].map({True: 'Yes', False: 'No'})
            print("4. Se ha agregado la columna 'has_discount'")
        except ValueError:
            print("4. El archivo ya tiene la columna 'has_discount'")

        # 4.2 Convertir columnas buen_fin_discount y black_friday_discount a booleano
        df['buen_fin_discount'] = df['buen_fin_discount'].apply(lambda x: bool(x == 'Yes'))
        df['black_friday_discount'] = df['black_friday_discount'].apply(lambda x: bool(x == 'Yes'))
        print("4.2 Columnas buen_fin_discount y black_friday_discount convertidas a BOOLEANO")

        # 5. Llenar valores NaN en discount_amount, discount_percentage y reviews_count con 0
        df['discount_amount'].fillna(0.0, inplace=True)
        df['discount_percentage'].fillna(0.0, inplace=True)
        df['reviews_count'].fillna(0.0, inplace=True)
        print("5. Se reemplazaron los 'N/A' por 0 en discount_amount, discount_percentage y reviews_count")

        # 6. Si no hay "rating" -> reviews_count = 0
        df.loc[df['rating'] == "No Rating", 'reviews_count'] = 0
        print("6. Se corrigieron errores en 'reviews_count' -> 0")

        # 7. Reemplazar original_price con price donde original_price < price
        mask = df['original_price'] < df['price']
        changes_made = mask.any()
        df.loc[mask, 'original_price'] = df.loc[mask, 'price']
        if changes_made:
            print("7. Se realizaron cambios en los valores de 'original_price'.")
        else:
            print("7. No fue necesario realizar cambios en 'original_price'.")

        # Guardar los cambios en la carpeta cleaned_data con el mismo nombre del archivo
        ruta_archivo_cleaned = os.path.join(ruta_carpeta_cleaned, archivo)
        df.to_csv(ruta_archivo_cleaned, encoding='utf-8-sig', index=False)
        print(f"Se guardaron los cambios en el archivo: {ruta_archivo_cleaned}")
    else:
        # Archivos que no coincidan con la fecha actual se omiten
        pass
