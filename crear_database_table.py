import psycopg2
import streamlit as st

def create_database_and_table():
    # Cambia 'tu_usuario' y 'tu_contraseña' por tus credenciales correctas
        # Supabase credentials (adjust with your actual password)
    user = st.secrets["postgres"]["user"]
    password = st.secrets["postgres"]["password"]
    host = st.secrets["postgres"]["host"] 
    port = st.secrets["postgres"]["port"]
    #database = st.secrets["postgres"]["database"]
    
    # Conectar al servidor PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Crear la base de datos si no existe
        database_name = "amazon_data"
        cursor.execute(f"CREATE DATABASE {database_name};")
        print(f"Base de datos '{database_name}' creada con éxito.")
        cursor.close()
        conn.close()
    except psycopg2.errors.DuplicateDatabase:
        print(f"La base de datos '{database_name}' ya existe. Continuando...")
        cursor.close()
        conn.close()
    
    # Conectar a la nueva base de datos para crear la tabla
    try:
        conn = psycopg2.connect(
            dbname=database_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()

        # Crear la tabla
        create_table_query = """
        CREATE TABLE IF NOT EXISTS productos_amazon (
            name TEXT,
            product_type TEXT,
            availability TEXT,
            price NUMERIC,
            original_price NUMERIC,
            discount_amount NUMERIC,
            discount_percentage NUMERIC,
            has_discount BOOLEAN,
            buen_fin_discount BOOLEAN,
            black_friday_discount BOOLEAN,
            image TEXT,
            reviews_count INT,
            rating NUMERIC,
            search_type TEXT,
            date DATE
            
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Tabla 'productos_amazon' creada con éxito.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al crear la tabla: {e}")
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Llama a la función
create_database_and_table()
