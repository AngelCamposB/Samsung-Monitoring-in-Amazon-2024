# Monitoreo de Descuentos de Productos Samsung en Amazon 2024

## Descripción General

Este proyecto busca monitorear productos de la marca Samsung disponibles en Amazon México durante eventos promocionales clave como el Buen Fin, Black Friday y el periodo posterior hasta mediados de diciembre de 2024. El objetivo es analizar tendencias de descuentos y evaluar el impacto de estas promociones en los productos de la marca.

El sistema implementa un pipeline ETL (Extracción, Transformación y Carga) para gestionar datos de manera eficiente: recopila información desde Amazon, la limpia, la transforma y la almacena en una base de datos PostgreSQL alojada en la nube mediante Supabase. Además, incluye un dashboard interactivo creado con Streamlit para visualizar métricas clave, tendencias y comparaciones.

---

## Tabla de Contenidos

1. [Instalación](#instalación)
2. [Uso del Proyecto](#uso-del-proyecto)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Requerimientos](#requerimientos)
5. [Tecnologías Utilizadas](#tecnologías-utilizadas)
6. [Contribución](#contribución)
7. [Licencia](#licencia)

---

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/AngelCamposB/Samsung-Monitoring-in-Amazon-2024.git
   ```

2. **Instalar dependencias:**

   Utiliza el archivo `requirements.txt` para instalar las bibliotecas necesarias:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar credenciales:**

   Crea un archivo `secrets.toml` para almacenar las credenciales de tu base de datos alojada en Supabase.

---

## Uso del Proyecto

### Paso 1: Ejecutar el Pipeline ETL

Inicia el pipeline ETL con el archivo `pipeline.py`, el cual ejecuta las etapas de extracción, limpieza, transformación y carga de datos:

```bash
python pipeline.py
```

### Paso 2: Visualización de Resultados

Para explorar los datos y obtener análisis visuales, ejecuta el dashboard interactivo con Streamlit:

```bash
streamlit run deployment.py
```

Si deseas compartir el dashboard con otras personas, utiliza [nGrok](https://dashboard.ngrok.com/get-started/setup/windows) para exponer el servidor local de forma segura.

---

## Estructura del Proyecto

```plaintext
Samsung Monitoring in Amazon 2024/
|— Scraping_Amazon.py           # Obtiene datos de Amazon y los guarda en CSV.
|— cleaning_data.py            # Limpia y transforma los datos extraídos.
|— merge_data.py               # Une los archivos CSV y agrega metadatos.
|— crear_database_table.py     # Crea la base de datos y la tabla en PostgreSQL.
|— load_to_database.py         # Carga los datos transformados a la base de datos.
|— deployment.py              # Despliega el dashboard interactivo con Streamlit.
|— pipeline.py                # Automatiza el proceso ETL completo.
|— requirements.txt           # Lista de dependencias.
|— .gitignore                 # Archivos y carpetas ignorados en el repositorio.
|— dataset/                   # Almacena los datos unificados.
|— raw_data/                  # Contiene los datos crudos obtenidos del scraping.
|— cleaned_data/              # Contiene los datos procesados y limpios.
```

---

## Requerimientos

- Python 3.9 o superior
- Dependencias incluidas en `requirements.txt`. Para instalarlas, ejecuta:

  ```bash
  pip install -r requirements.txt
  ```

---

## Tecnologías Utilizadas

- **Lenguajes**: Python
- **Librerías**: Selenium, BeautifulSoup, Pandas, SQLAlchemy, Streamlit, Plotly
- **Base de Datos**: PostgreSQL (Supabase como servicio en la nube)
- **Herramientas Adicionales**: [nGrok](https://dashboard.ngrok.com/get-started/setup/windows) para compartir el dashboard local

---

## Contribución

1. Haz un fork de este repositorio.
2. Crea una rama para tu contribución (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Haz push a tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request en este repositorio.

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

