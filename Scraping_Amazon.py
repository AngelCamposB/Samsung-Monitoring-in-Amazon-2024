from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime
import os


def scrape_amazon_products(url, csv_filename="productos_amazon.csv"):
    # Inicializa el navegador Microsoft Edge
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

    # Carga la página del producto
    driver.get(url)

    # Espera a que cargue la página
    try:
        time.sleep(5)  # Puedes ajustar el tiempo de espera según sea necesario

        # Recopila la información de los productos
        products = []

        # Usa BeautifulSoup para extraer información de la página
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in items:
            try:
                # Nombre del producto
                name = item.h2.get_text(strip=True)

                # Clasificación del tipo de producto
                if ("case" in name.lower() or "funda" in name.lower()) and not ("incluye funda" in name.lower() or "incluye case" in name.lower() or "incluye folio" in name.lower() or "con funda" in name.lower() or "con case" in name.lower()):
                    product_type = "case"
                elif "tablet" in name.lower() or "tab" in name.lower():
                    product_type = "tablet"
                elif "flip" in name.lower() or "s1" in name.lower() or "s2" in name.lower() or "a0" in name.lower() or "a1" in name.lower() or "a2" in name.lower() or "a3" in name.lower() or "a5" in name.lower() or "phone" in name.lower() or "celular" in name.lower() or "telefono" in name.lower():
                    product_type = "smartphone"
                elif "pen" in name.lower():
                    product_type = "pencil"
                elif "watch" in name.lower() or "reloj" in name.lower() or "fit" in name.lower():
                    product_type = "watch"
                elif "tv" in name.lower():
                    product_type = "tv"
                elif "cargador" in name.lower():
                    product_type = "charger"
                else:
                    product_type = "another"

                # Precio del producto (descuento)
                price_whole = item.find("span", class_="a-price-whole")
                price_fraction = item.find("span", class_="a-price-fraction")
                price = None
                if price_whole and price_fraction:
                    price = float(price_whole.get_text(strip=True).replace(".", "").replace(',', '') + "." + price_fraction.get_text(strip=True))
                elif price_whole:
                    price = float(price_whole.get_text(strip=True).replace("..", "."))

                # Precio original (sin descuento)
                original_price_elem = item.find("span", class_="a-price a-text-price")
                original_price = float(original_price_elem.find("span", class_="a-offscreen").get_text(strip=True).replace("$", "").replace(",", "")) if original_price_elem else price

                # Calcular el descuento (cantidad y porcentaje), si original < actual -> original = actual
                if original_price and price and original_price > price:
                    discount_amount = original_price - price
                    discount_percentage = (discount_amount / original_price) * 100
                elif original_price and price and original_price < price:
                    original_price = price

                # Verificar si el descuento es del Buen Fin
                black_friday_discount = "Black Friday" in item.get_text()                

                # Imagen del producto
                image = item.find("img", class_="s-image")["src"]

                # Cantidad de reseñas y puntuación
                reviews_count = item.find("span", class_="a-size-base")
                reviews_count = reviews_count.get_text(strip=True) if reviews_count else "No Reviews"
                rating = item.find("span", class_="a-icon-alt")
                rating = rating.get_text(strip=True) if rating else "No Rating"

                # Disponibilidad
                availability = "Available" if price else "Out of Stock"

                # Agrega los datos del producto a la lista
                products.append({
                    "name": name,
                    "product_type": product_type,
                    "availability": availability,
                    "price": f"${price:,.2f}" if price else "N/A",
                    "original_price": f"${original_price:,.2f}" if original_price else 0,
                    "discount_amount": f"${discount_amount:,.2f}" if discount_amount else 0,
                    "discount_percentage": f"{discount_percentage:.2f}%" if discount_percentage else 0,
                    "black_friday_discount": "Yes" if black_friday_discount else "No",
                    "image": image,
                    "reviews_count": reviews_count,
                    "rating": rating
                })

            except Exception as e:
                print("Error extrayendo datos de un PRODUCTO:", e)

        # Guarda los datos en un archivo CSV
        with open(csv_filename, mode="w", newline='', encoding="utf-8-sig") as file:
            fieldnames = ["name", "product_type", "availability", "price", "original_price", "discount_amount", "discount_percentage", "black_friday_discount", "image", "reviews_count", "rating"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)

        print(f"Datos guardados en {csv_filename} correctamente.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        driver.quit()

# Define la URL del producto de Amazon
#Sangung S23
Amazon_Samsung_S23_url = "https://www.amazon.com.mx/s?k=samsung+galaxy+s23&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=4JIMJY0R3H8A&sprefix=%2Caps%2C676&ref=nb_sb_noss_2"
#Samsung Productos
Amazon_Samsung_Products = "https://www.amazon.com.mx/s?k=samsung&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3C8G7TS1MTQ3E&sprefix=samsung%2Caps%2C166&ref=nb_sb_noss_1"
#Galaxy tab
Amazon_Samsung_Tablets = "https://www.amazon.com.mx/s?k=samsung+tab&crid=3HMZW7SW28WSB&sprefix=samsung+t%2Caps%2C113&ref=nb_sb_ss_ts-doa-p_2_9"



# Generar la fecha/hora en el formato deseado
# Ejemplo de formato: "Dec10 - 7pm"
# %b: nombre corto del mes (Ej: Dec)
# %d: día del mes (Ej: 10)
# %I: hora en formato 12 horas (Ej: 07)
# %p: AM/PM (Ej: PM)
# Nota: Puede que obtengas un cero a la izquierda en la hora (07pm), 
# si quieres evitarlo depende del sistema operativo, pero muchas veces se acepta el 0 inicial.

# Crear la carpeta raw_data si no existe
if not os.path.exists("raw_data"):
    os.makedirs("raw_data")

timestamp = datetime.now().strftime("%b%d - %I%p")

# Guardado de archivos
scrape_amazon_products(Amazon_Samsung_Products, f"raw_data/Amazon_Samsung_Products - {timestamp}.csv")
scrape_amazon_products(Amazon_Samsung_S23_url, f"raw_data/Amazon_Samsung_S23 - {timestamp}.csv")
scrape_amazon_products(Amazon_Samsung_Tablets, f"raw_data/Amazon_Samsung_Tabs - {timestamp}.csv")

