
import pandas as pd 
import re 
import time

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By    #En nuevas versiones de Python es requerido
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, SessionNotCreatedException
from webdriver_manager.chrome import ChromeDriverManager

from .tools import randomtime

#Paquetes interacción a usuario
from IPython.display import clear_output, display, HTML
import ipywidgets as widgets

def selectdfQ(df, Q, operacion):   # Operacion puede ser venta o arriendo
    # Excluir proyectos y dejar solo lo que tiene que ver con inmuebles 
    df_inmobiliaria = df[df.Tipo.isin([f'Apartamento en {operacion}', f'Casa en {operacion}'])].reset_index(drop=True)

    total_filas = len(df_inmobiliaria)
    print(total_filas)
    tamaño_medio = total_filas // 2

    # Divide el DataFrame en cuartos
    dfQ1 = df_inmobiliaria.iloc[:tamaño_medio]
    dfQ2 = df_inmobiliaria.iloc[tamaño_medio:]

    # Devolver el DataFrame correspondiente a Q
    if Q == 1:
        return dfQ1, print(f'Usted seleccionó dfQ1 con: {len(dfQ1)} obs')
    elif Q == 2:
        return dfQ2, print(f'Usted seleccionó dfQ2 con: {len(dfQ2)} obs')
    else:
        print("Error: Q debe ser un valor entre 1 y 2.")


'''
regexdata: This function uses the regular expressions for convert the 
html text in real data.

'''

def regexdata(df):
    
    def applyregex(row, regex, column_name, emptylist):
        column_content = str(row[column_name])
        operation_match = re.search(regex, column_content)
        operation_text = operation_match.group(1) if operation_match else ''
        emptylist.append(operation_text)


    #regex
    url_regex = r'"url":"([^<]+)","name"'
    operation_regex = r'data-qa-id="_route_1">([^<]+)</a>'
    city_regex = r'data-qa-id="_route_2">([^<]+)</a>'
    zone_regex = 'data-qa-id="_route_3">([^<]+)</a>'
    neighbour_regex = 'data-qa-id="_route_4">([^<]+)</a>'
    property_regex = 'data-qa-id="_route_5">([^<]+)</a>'
    price_regex = r'class="price">([^<]+)<'
    area_regex = r'class="contact__area-value">([^<]+)<'
    codigo_regex = r'Código: </strong>([^<]+)<'
    habs_regex = r'Habitaciones<\/p><p [^>]*>(\d+)<\/p>'
    baths_regex = r'Baños<\/p><p [^>]*>(\d+)<\/p>'
    park_regex = r'Parqueaderos<\/p><p [^>]*>(\d+)<\/p>'
    admin_regex = r'Administración: </strong>([^<]+)<'
    stratum_regex = r'Estrato: </strong>([^<]+)<'
    floor_regex = r'Piso: </strong>([^<]+)<'
    description_regex = r'class="expansion-panel__description">([^<]+)<'
    features_regex = r'<h3\s+class="ng-star-inserted">Características del inmueble<\/h3>(.*?)<h3\s+class="ng-star-inserted">Zonas comunes<\/h3>'
    zonasc_regex = r'<h3\s+class="ng-star-inserted">Zonas comunes<\/h3>(.*?)<ciencuadras-expansion-panel\s+.*?title="Sitios de interés".*?>'
    sitiosi_regex = r'<ciencuadras-expansion-panel\s+.*?title="Sitios de interés".*?>(.*?)¿Aún tienes dudas\? <br> ¡Hablemos!</p></div>'

    lat_regex = r'"latitude":"([^<]+)","longitude":"'
    lon_regex = r'"longitude":"([^<]+)"}'

    #listas
    url = []
    operation = []
    city = []
    zone = []
    neighbour = []
    propertyt = []
    price = []
    area = []
    codigo = []
    habs = []
    baths = []
    park = []
    admin = []
    stratum = []
    floor = []
    description = []
    features = []
    zonas = []
    sitios = []

    latitude = []
    longitude = []


    for index, row in df.iterrows():
        applyregex(row, url_regex,'maps', url)

        applyregex(row, operation_regex,'general', operation)
        applyregex(row, city_regex,'general', city)
        applyregex(row, zone_regex,'general', zone)
        applyregex(row, neighbour_regex,'general', neighbour)
        applyregex(row, property_regex,'general', propertyt)
        applyregex(row, price_regex,'general', price)
        applyregex(row, area_regex,'general', area)
        applyregex(row, codigo_regex,'general', codigo)
        applyregex(row, habs_regex,'general', habs)
        applyregex(row, baths_regex,'general', baths)
        applyregex(row, park_regex,'general', park)
        applyregex(row, admin_regex,'general', admin)
        applyregex(row, stratum_regex,'general', stratum)
        applyregex(row, floor_regex,'general', floor)
        applyregex(row, description_regex,'general', description)
        applyregex(row, features_regex,'general', features)
        applyregex(row, zonasc_regex,'general', zonas)
        applyregex(row, sitiosi_regex,'general', sitios)

        applyregex(row, lat_regex,'maps', latitude)
        applyregex(row, lon_regex,'maps', longitude)





    new_df = pd.DataFrame({'url': url,
                           'operation': operation, 
                           'city':city,
                           'zone':zone, 
                           'neighbour':neighbour,
                           'propertytype':propertyt,
                           'price':price,
                           'area':area,
                           'codigo':codigo,
                           'bedrooms':habs,
                           'baths':baths,
                           'park':park,
                           'admin':admin,
                           'stratum':stratum,
                           'floor':floor,
                           'description':description,
                           'features':features,
                           'zonas':zonas,
                           'sitios':sitios,

                           'latitude':latitude, 
                           'longitude':longitude,
                          })

    new_df['features'] = new_df['features'].str.replace(r'<[^>]*>', '|')
    # Eliminar los múltiples '|' consecutivos
    new_df['features'] = new_df['features'].str.replace(r'\|+', '|')

    # Eliminar '|' al principio y al final de la cadena
    new_df['features'] = new_df['features'].str.strip('|')

    new_df['zonas'] = new_df['zonas'].str.replace(r'<[^>]*>', '|')
    # Eliminar los múltiples '|' consecutivos
    new_df['zonas'] = new_df['zonas'].str.replace(r'\|+', '|')

    # Eliminar '|' al principio y al final de la cadena
    new_df['zonas'] = new_df['zonas'].str.strip('|')

    new_df['sitios'] = new_df['sitios'].str.replace(r'<[^>]*>', '|')
    # Eliminar los múltiples '|' consecutivos
    new_df['sitios'] = new_df['sitios'].str.replace(r'\|+', '|')

    # Eliminar '|' al principio y al final de la cadena
    new_df['sitios'] = new_df['sitios'].str.strip('|')

    return new_df


'''
get_current_time: just get the real time for the scraper

'''
def get_current_time():
    return datetime.now()

'''
internal: This is the most important function, 
the scraper use just one xpath that contains all the information of the page. 
Aditionaly, the scraper only takes five minutes open, after five minutes, the driver closes itself,
and start again with the other links storaged in the main df

'''

def internal(df, operation):

    tiempo = randomtime()
    #Driver directory:
    DRIVER = 'C:/Users/luisG/GIT/SCRAPING/DRIVER/chromedriver.exe'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar en modo sin cabeza
    options.add_argument("--no-sandbox")  
    service = Service(f'{DRIVER}')

    # Crear el driver fuera del loop
    driver = webdriver.Chrome(service=service, options=options)
    

    enlaces_list = []
    general = []
    maps = []


    # Contador de enlaces
    total_enlaces = len(df)
    enlaces_procesados = 0
    enlaces_procesados_desde_ultima_cierre = 0
    
    #Funcion para guardar el contenido html en listas vacias 
    def div_elements(div_element, Emptylist):

        def parse_html(html_content):
            return {f'{div_element}': html_content}

        df_rows = []

        for element in div_element:
            html_content = element.get_attribute('outerHTML')
            data = parse_html(html_content)
            df_rows.append(data)
        if not df_rows:
            df_rows = ['']  # Agrega una cadena vacía si no se encuentra información

        Emptylist.extend(df_rows)

        return Emptylist

    
    try:
        start_time = datetime.now()
        print(f"El proceso de scraping ha comenzado a las {start_time.strftime('%H:%M')} del {start_time.strftime('%d/%m/%Y')}")

        # Recorrer los enlaces del DataFrame
        index = 0
        continue_scraping = True  # Variable de control para continuar o detener el proceso

        while continue_scraping and index < len(df):
            row = df.iloc[index]
            enlaces_procesados += 1
            enlaces_procesados_desde_ultima_cierre += 1
            link = row['Link']
            
            # Verificar si se ha alcanzado el límite de enlaces procesados desde la última reinicialización del driver
            if enlaces_procesados_desde_ultima_cierre == 60:
                driver.quit()
                time.sleep(tiempo)
                driver = webdriver.Chrome(service=service, options=options)
                enlaces_procesados_desde_ultima_cierre = 0  
                
            if enlaces_procesados % 50 == 0:
                print(f"Enlaces procesados: {enlaces_procesados} de {total_enlaces}")

            try:
                if operation == 'venta':
                    try:
                        driver.get(link)
                        time.sleep(tiempo)
                        div_general = driver.find_elements(By.XPATH, '//div[contains(@class, "mt-huge")]')
                        gen = div_elements(div_general, general)
                        script_map = driver.find_elements(By.XPATH, '//script[@type="application/ld+json" and contains(., \'"@type":"GeoCoordinates"\')]')
                        maplt = div_elements(script_map, maps)

                    except: 
                        print('Error')

                elif operation == 'arriendo':
                    try:
                        driver.get(link)
                        time.sleep(tiempo)
                        div_general = driver.find_elements(By.XPATH, '//div[contains(@class, "mt-huge")]')
                        gen = div_elements(div_general, general)
                        script_map = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"][4]')
                        maplt = div_elements(script_map, maps)


                    except: 
                        print('Error')
                
                enlaces_list.append(link)
                    
            except Exception as e:
                print(f"Se produjo un error al cargar el enlace: {link}")
                print(f"Excepción: {str(e)}")
                print("Reiniciando el driver y continuando con el próximo enlace...")
                # Cerrar el controlador anterior
                driver.quit()

                # Iniciar un nuevo controlador
                driver = webdriver.Chrome(service=service, options=options)
            else:
                # El bloque "else" se ejecutará si no se produce una excepción, es decir, si se carga el enlace correctamente.
                index += 1  # Avanzar al próximo enlace solo si se procesa correctamente


                
    except Exception as e:
        print(f"Se produjo un error en el scraping: {e}")
    finally:
        # Cerrar el driver al final del proceso
        driver.quit()


    data_list = []

    for gen_v, maplt_v, link_v in zip(gen, maplt, enlaces_list):
        row_data = {
                'general': gen_v,
                'maps':maplt_v,
                'Url': link_v
            }
        data_list.append(row_data)
    df = pd.DataFrame(data_list)
    
    # Mensaje de aviso de que el scraping terminó
    aviso = f"¡El DataFrame de tamaño {df.shape} df_inmobiliarias de FINCA RAIZ está disponible para su análisis!"
    display(HTML(f"<div style='background-color: #b8daba; padding: 10px; border: 1px solid #007723; border-radius: 5px;'><strong>IMBUEBLES DISPONIBLE:</strong> {aviso}</div>"))
    
    return df
