import pandas as pd
import os
import numpy as np

#(3) Función para limpiar y convertir a float las columnas
def clean_and_convert(value):
    
    value = str(value)
    value = value.replace('$', '').replace(',', '').replace('%', '').replace(' de 5 estrellas', '')
    try:
        value = float(value)
        return float(value)
    except ValueError:
        print(f"Error al convertir el valor '{value}' a float.")
        return None  # Manejar valores no numéricos


# Ruta a la carpeta donde se encuentran los archivos CSV
ruta_carpeta = r"C:\Users\Angel\Desktop\Amazon\data_cleaning_process\Prueba"  # Reemplaza con la ruta correcta

# Columnas a modificar (índices comienzan desde 0)

# Recorremos todos los archivos CSV en la carpeta
for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(".csv"):
        ruta_archivo = os.path.join(ruta_carpeta, archivo)

        # Leemos 1  el archivo CSV en un DataFrame
        #df = pd.read_csv(ruta_archivo, encoding='utf-8-sig')

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
        #1 Agregamos la nueva columna DESC BUEN FIN en la posición 8
        # Nueva columna y valor a agregar (puedes modificarlo)
        nueva_columna = "buen_fin_discount"
        valor_a_agregar = "No"
        try:
            df.insert(7, nueva_columna, valor_a_agregar)
            print(f"1. Se agregó la columna: '{nueva_columna}' ")
        except ValueError:
            print(f"1. El archivo ya tiene la columna: '{nueva_columna}' ")


        #1.2 Agregamos la nueva columna DESC BLACK FRIDAY en la posición 8
            # Nueva columna y valor a agregar (puedes modificarlo)
        nueva_columna = "black_friday_discount"
        valor_a_agregar = "No"
        try:
            df.insert(8, nueva_columna, valor_a_agregar)
            print(f"1.2. Se agregó la columna: '{nueva_columna}' ")
        except ValueError:
            print(f"1.2. El archivo ya tiene la columna: '{nueva_columna}' ")

        #2 Aplica la función para limpiar y convertir las columnas especificadas a numericas
        for col in ['price', 'original_price', 'discount_amount', 'discount_percentage', 'reviews_count', 'rating']:
            df[col] = df[col].apply(clean_and_convert)
        print("2. Columnas convertidas a float")

        #3 Corregir error de discount_amount y discount_percentage -> 0
        # Condición: si price == original_price, entonces discount_amount y discount_percentage son 0
        df.loc[df['price'] == df['original_price'], ['discount_amount', 'discount_percentage']] = 0
        print("3. Posibles errores: discount_amount y discount_percentage corregidos -> 0")

        #4 Agregamos otra columna en la pocision 7 DESCUENTO GENERAL
        # Convertir los valores booleanos a 'Yes' o 'No'
        try:
            # Crea una nueva columna con la condición y la coloca en la posición 8
            df.insert(7, 'has_discount', df['discount_amount'] > 0)
            df['has_discount'] = df['has_discount'].map({True: 'Yes', False: 'No'})
            print("4 Se ha agregado la columna 'has_discount'")
        except ValueError:
            print("4 El archivo ya tiene la columna 'has_discount'")

        #4.2 Convertir Columnas buen_fin_discount y black_friday_discount a BOOLEANO
        df['buen_fin_discount'] = df['buen_fin_discount'].apply(lambda x: bool(x == 'Yes'))
        df['black_friday_discount'] = df['black_friday_discount'].apply(lambda x: bool(x == 'Yes'))
        print("4.2 Columnas buen_fin_discount y black_friday_discount Convertidas a BOOLEANO")

        #5 Llena los valores NaN en las columnas 'discount_amount' y 'discount_percentage' con 0
        df['discount_amount'].fillna(0.0, inplace=True)
        df['discount_percentage'].fillna(0.0, inplace=True)
        df['reviews_count'].fillna(0.0, inplace=True)
        print(f"5. Se reemplazaron los 'N/A' por 0 en discount_amount y discount_percentage")

        #6 Si no hay "rating" -> reviews_count = 0
        df.loc[df['rating'] == "No Rating", 'reviews_count'] = 0
        print("6. Se corrigieron errores en 'reviews_count' -> 0")

        #7 Replace original_price with price where original_price is less than price
        #df.loc[df['original_price'] < df['price'], 'original_price'] = df['price']     #Version Compacta
        # Identificar los valores que necesitan ser actualizados
        mask = df['original_price'] < df['price']

        # Realizar la actualización solo donde sea necesario
        changes_made = mask.any()  # Verificar si hay al menos un cambio necesario
        df.loc[mask, 'original_price'] = df.loc[mask, 'price']

        # Mostrar un mensaje indicando si se hicieron cambios
        if changes_made:
            print("7. Se realizaron cambios en los valores de 'original_price'.")
        else:
            print("7. No fue necesario realizar cambios en 'original_price'.")


        # Guardamos los cambios en el mismo archivo
        df.to_csv(ruta_archivo, encoding='utf-8-sig', index=False)
        print(f"Se guardaron los cambios en el archivo: {archivo}")