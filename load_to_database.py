import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import streamlit as st
import os

def load_csv_to_postgresql():
    # Definir credenciales Supabase
    user = st.secrets["postgres"]["user"]
    password = st.secrets["postgres"]["password"]
    host = st.secrets["postgres"]["host"] 
    port = st.secrets["postgres"]["port"]
    database = st.secrets["postgres"]["database"]

    # Generar el nombre del archivo en función del timestamp requerido
    # Ejemplo: data_unificada - Nov14 - 10PM.csv
    timestamp = datetime.now().strftime("%b%d - %I%p")
    csv_file = f"data_unificada - {timestamp}.csv"

    # Ubicación del archivo dentro de la carpeta 'dataset'
    csv_path = os.path.join("dataset", csv_file)

    # Leer el archivo CSV
    df = pd.read_csv(csv_path)
    
    # Convertir columnas específicas a tipos adecuados si es necesario
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    # Crear conexión a la base de datos PostgreSQL en Supabase
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url)
    
    # Subir datos a la tabla
    table_name = "productos_amazon"
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Datos de '{csv_file}' cargados con éxito en la tabla '{table_name}'.")

# Llamar a la función
load_csv_to_postgresql()
