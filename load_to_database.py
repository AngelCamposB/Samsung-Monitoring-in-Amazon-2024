import pandas as pd
from sqlalchemy import create_engine

def load_csv_to_postgresql(csv_file, db_name):
    # Definir credenciales
    user = "postgres"  
    password = "5354"
    
    # Leer el archivo CSV
    df = pd.read_csv(csv_file)
    
    # Convertir columnas específicas a tipos adecuados si es necesario
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    #df["buen_fin_discount"] = df["buen_fin_discount"].astype(bool)
    
    # Crear conexión a la base de datos PostgreSQL
    engine = create_engine(f"postgresql://{user}:{password}@localhost:5432/{db_name}")
    
    # Subir datos a la tabla
    table_name = "productos_amazon"
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Datos de '{csv_file}' cargados con éxito en la tabla '{table_name}'.")

# Llama a la función
csv_file = "data_unificada.csv"  # Ruta completa al archivo CSV
db_name = "amazon_data"
load_csv_to_postgresql(csv_file, db_name)