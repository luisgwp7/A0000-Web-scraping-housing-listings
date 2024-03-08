import pandas as pd 
import re 
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By    #En nuevas versiones de Python es requerido
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, SessionNotCreatedException
from webdriver_manager.chrome import ChromeDriverManager

from .tools import randomtime
from itertools import product

def frontpage(link):
    #Driver directory:
    DRIVER = 'C:/Users/luisG/GIT/SCRAPING/DRIVER/chromedriver.exe'
    tiempo = randomtime()
    pages = 499
    dataX = []
    options = webdriver.ChromeOptions()
    service = Service(DRIVER)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Desactivar sandboxing
    driver = webdriver.Chrome(service=service, options=options)
    def apply_filters(stratum, rooms, bathrooms):
        try:
            next_button = driver.find_element(By.XPATH, '//ciencuadras-button/button[contains(@data-qa-id, "cc-rs-rs-btn_open_modal_more_filters")]')
            driver.execute_script("arguments[0].click();", next_button)
            #time.sleep(tiempo)
        except:
            print("No se encontró el botón para filtrar")
            pass

        try:
            next_button = driver.find_element(By.XPATH, f'//div/label[contains(@data-qa-id, "cc-rs-rs-option_stratum{stratum}")]')
            driver.execute_script("arguments[0].click();", next_button)
        except:
            print("No se encontró el botón de filtro de estrato")
            pass 

        try:
            next_button = driver.find_element(By.XPATH, f'//div/label[contains(@data-qa-id, "cc-rs-rs-option_rooms{rooms}")]')
            driver.execute_script("arguments[0].click();", next_button)
            #time.sleep(tiempo)
        except:
            print("No se encontró el botón de filtro de rooms")
            pass
        
        try:
            next_button = driver.find_element(By.XPATH, f'//div/label[contains(@data-qa-id, "cc-rs-rs-option_bathrooms{bathrooms}")]')
            driver.execute_script("arguments[0].click();", next_button)
            #time.sleep(tiempo)
        except:
            print("No se encontró el botón de filtro de bathrooms")
            pass
        
        try:
            next_button = driver.find_element(By.XPATH,  '//ciencuadras-button/button[contains(@data-qa-id, "cc-rs-rs-btn_apply_filters")]')
            driver.execute_script("arguments[0].click();", next_button)
        except:
            print("No se encontró el botón para aplicar filtros")
            pass

    def parse_html(html_content):
        return {'HTML_Content': html_content}

    for stratum, rooms, bathrooms in product(range(1, 7), range(1, 7), range(1, 7)):
        driver = webdriver.Chrome(service=service, options=options)  # Abre el driver para cada combinación de filtros
        driver.get(link)
        apply_filters(stratum, rooms, bathrooms)
        time.sleep(tiempo)

        for i in range(pages):
            try:
                tiempo = randomtime()
                div_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "container-list-card grid")]/div[contains(@class, "grid-12 grid-sm-3 grid-md-3 grid-lg-3 grid-xl-2 ng-star-inserted")]')
                df_rows = []

                for element in div_elements:
                    html_content = element.get_attribute('outerHTML')
                    data = parse_html(html_content)
                    df_rows.append(data)

                dataX.extend(df_rows)
                time.sleep(tiempo)

                try:
                    next_button = driver.find_element(By.XPATH, '//li[contains(@class, "following show") and contains(@data-qa-id, "cc-rs-rs_paginator_results_next")]')
                    driver.execute_script("arguments[0].click();", next_button)
                except:
                    print("No se encontró el botón 'Siguiente página'")
                    break

            except Exception as e:
                print(f"Error al procesar la página {i+1}: {str(e)}")
                break

        driver.quit()  # Cierra el driver después de iterar por todas las páginas con la combinación actual de filtros

    time.sleep(tiempo)
    df = pd.DataFrame(dataX)
    df_final = df.drop_duplicates(subset=['HTML_Content'])
    return df_final

def frontpage_new():
    #Driver irectory:
    DRIVER = 'C:/Users/luisG/GIT/SCRAPING/DRIVER/chromedriver.exe'
    tiempo = randomtime()
    link = 'https://www.ciencuadras.com/proyectos-vivienda-nueva'
    pages = 499
    dataX = []
    options = webdriver.ChromeOptions()
    service = Service(DRIVER)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Desactivar sandboxing
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(link)
    time.sleep(tiempo)
    
    def parse_html(html_content):
        return {'HTML_Content': html_content}
    
    for i in range(pages):
        try:
            tiempo = randomtime()
            div_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "container-list-card grid")]/div[contains(@class, "grid-12 grid-sm-3 grid-md-3 grid-lg-3 grid-xl-2 ng-star-inserted")]')
            df_rows = []

            for element in div_elements:
                html_content = element.get_attribute('outerHTML')
                data = parse_html(html_content)
                df_rows.append(data)

            dataX.extend(df_rows)
            time.sleep(tiempo)

            try:
                next_button = driver.find_element(By.XPATH, '//li[contains(@class, "following show") and contains(@data-qa-id, "cc-rs-rs_paginator_results_next")]')
                driver.execute_script("arguments[0].click();", next_button)
            except:
                print("No se encontró el botón 'Siguiente página'")
                break

        except Exception as e:
            print(f"Error al procesar la página {i+1}: {str(e)}")
            break

    driver.quit() 

    time.sleep(tiempo)
    df = pd.DataFrame(dataX)
    
    df = df.drop_duplicates(subset=['HTML_Content'])
    return df

def regexdata(df):
    enlaces_regex = r'href="([^"]+)"'
    destacados_regex = r'<p class="card__location ng-star-inserted"><!---->([^<]+)<!---->'
    precios_regex = r'<span class="card__price-big">([^"]+)<!----><!----><!---->'
    banos_regex = r'(\d+\s?Baño)'
    habs_regex = r'(\d+\s?Habit)' 
    areas_regex = r'(\d+\s?m2)'
    garaje_regex = r'(\d+\s?Garaje)'
    ubicacion_regex = r'<span class="city">([^<]+)</span>'
    ubicacion2_regex = '<span class="neighborhood">([^<]+)</span>'


    lista_enlaces = []
    destacado = []
    publicado = []
    prec = []
    baths = []
    habs = []
    area = []
    garaje = []
    ubicacion = []
    ubicacion2 = []


    for index, row in df.iterrows():
        html_content = row['HTML_Content']
        # Aplicar las expresiones regulares a los fragmentos de HTML
        enlaces_match = re.search(enlaces_regex, html_content)
        enlace = enlaces_match.group(1) if enlaces_match else ''
        lista_enlaces.append(enlace)

        destacados_match = re.search(destacados_regex, html_content)
        destacado_text = destacados_match.group(1) if destacados_match else ''
        destacado.append(destacado_text)

        precios_match = re.search(precios_regex, html_content)
        prec_text = precios_match.group(1) if precios_match else ''
        prec.append(prec_text)

        banos_match = re.search(banos_regex, html_content)
        banos_text = banos_match.group(1) if banos_match else ''
        baths.append(banos_text)

        habs_match = re.search(habs_regex, html_content)
        habs_text = habs_match.group(1) if habs_match else ''
        habs.append(habs_text)

        areas_match = re.search(areas_regex, html_content)
        areas_text = areas_match.group(1) if areas_match else ''
        area.append(areas_text)

        garaje_match = re.search(garaje_regex, html_content)
        garaje_text = garaje_match.group(1) if garaje_match else ''
        garaje.append(garaje_text)

        ubicacion_match = re.search(ubicacion_regex, html_content)
        ubicacion_text = ubicacion_match.group(1) if ubicacion_match else ''
        ubicacion.append(ubicacion_text)

        ubicacion2_match = re.search(ubicacion2_regex, html_content)
        ubicacion2_text = ubicacion2_match.group(1) if ubicacion2_match else ''
        ubicacion2.append(ubicacion2_text)
    
    link_regex = r'(\d+)$'       
    cod = []
    df['Link'] = lista_enlaces
    for index, row in df.iterrows():
        codigo_match = re.search(link_regex, row['Link'])
        codigo_text = codigo_match.group(1) if codigo_match else ''
        cod.append(codigo_text)
  
    df['Tipo'] = destacado
    df['Precio'] = prec
    df['Baños'] = baths
    df['Habitaciones'] = habs
    df['Area'] = area
    df['Garaje'] = garaje
    df['Ubicacion'] = ubicacion
    df['Destacado'] = ubicacion2
    df['Codigo'] = cod
    df = df.drop_duplicates(subset=['Link'])
    df["Baños"] = df["Baños"].str.replace('Baño', '')
    df["Habitaciones"] = df["Habitaciones"].str.replace('Habit', '')
    df["Area"] = df["Area"].str.replace('m2', '')
    df["Garaje"] = df["Garaje"].str.replace('Garaje', '')
    df["Precio"] = df["Precio"].str.replace('$', '').str.replace('.', '')
    df["Link"] =' https://www.ciencuadras.com'+ df['Link']
    df.drop(['HTML_Content'], axis=1, inplace=True)
    df = df.drop_duplicates(subset=['Codigo'])
    
    return df

