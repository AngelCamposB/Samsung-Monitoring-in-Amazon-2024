import subprocess

def ejecutar_script(nombre_archivo):
    """Ejecuta un script Python.

    Args:
        nombre_archivo (str): Nombre del archivo Python a ejecutar.
    """
    try:
        subprocess.call(["python", nombre_archivo])
        print(f"Script {nombre_archivo} ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {nombre_archivo}: {e}")

# Lista de archivos en el orden de ejecución
archivos = [
    "Scraping_Amazon.py",
    "cleaning_data.py",
    "merge_data.py",
    "load_to_database.py",
    "deployment.py"
]

# Ejecutar cada script
for archivo in archivos:
    ejecutar_script(archivo)