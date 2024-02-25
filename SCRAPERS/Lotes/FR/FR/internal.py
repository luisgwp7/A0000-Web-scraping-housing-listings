
import pandas as pd 
import re 
import time

from datetime import datetime, timedelta

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

def selectdfQ(df, Q, operacion): # operacion puede ser Venta o Arriendo
    # Excluir proyectos y dejar solo lo que tiene que ver con inmuebles 
    df_inmobiliaria = df[df.Tipo.isin([f'Apartamento en {operacion}', 
                                            f'Casa en {operacion}', 
                                            f'Apartaestudio en {operacion}',])].reset_index(drop=True)

    total_filas = len(df_inmobiliaria)
    tamaño_cuarto = total_filas // 4

    dfQ1 = df_inmobiliaria.iloc[:tamaño_cuarto]
    dfQ2 = df_inmobiliaria.iloc[tamaño_cuarto:tamaño_cuarto*2]
    dfQ3 = df_inmobiliaria.iloc[tamaño_cuarto*2:tamaño_cuarto*3]
    dfQ4 = df_inmobiliaria.iloc[tamaño_cuarto*3:]

    # Devolver el DataFrame correspondiente a Q
    if Q == 1:
        return dfQ1, print(f'Usted seleccionó dfQ1 con: {len(dfQ1)} obs')
    elif Q == 2:
        return dfQ2, print(f'Usted seleccionó dfQ2 con: {len(dfQ2)} obs')
    elif Q == 3:
        return dfQ3, print(f'Usted seleccionó dfQ3 con: {len(dfQ3)} obs')
    elif Q == 4:
        return dfQ4, print(f'Usted seleccionó dfQ4 con: {len(dfQ4)} obs')
    else:
        print("Error: Q debe ser un valor entre 1 y 4.")



'''
div_elements: Is used in the scraper for storage the data.

'''

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


'''
obtener_palabras: Is used in function which clean the data.

'''

def obtener_palabras(row):
    palabras = row['inmu_op'].split()
    tipo_inmueble = palabras[0] if palabras else None
    operation = palabras[-1] if palabras else None
    return pd.Series([tipo_inmueble, operation], index=['tipo_inmueble', 'operation'])


'''
regexdata: This function uses the regular expressions for convert the 
html text in real data.

'''

def regexdata(df):
    def apply_regex(regex, name_row, list_empty, row):
        row_dict = row[name_row]

        if isinstance(row_dict, dict):
            general = row_dict.values()
            general = list(general)[0]  # Convert the dictionary value to a string
            match = re.search(regex, general)
            text = match.group(1) if match else ''
            list_empty.append(text)
        else:
            list_empty.append('')

    def extract_names(value):
        # Utilizar una expresión regular para extraer lo que está después de "name":
        matches = re.findall('"name":"([^"]+)"', value)

        # Unir los resultados con el operador '|'
        result = " | ".join(matches)

        return result

    # Definir la expresión regular para "name" dentro de "interior"

    public_regex = ',"published":"([^"]+)",'
    updated_regex = ',"updated":"([^"]+)"},'    
    description_regex = ',"description":"([^"]+)",'
    stratum_regex = '"stratum":{"name":"([^"]+)",'
    pricem2_regex = '"priceM2":"([^"]+)",'
    newflat_regex = '"isNew":([^"]+),' 
    livingarea_regex = '"livingArea":"([^"]+)"' 
    minLivingArea_regex = '"minLivingArea":([^"]+),' 
    maxLivingArea_regex = '"minLivingArea":([^"]+),' 
    address_regex = '"address":"([^"]+)"'  
    contact_regex = '"contact":{"emails":\["([^"]+)"\],'
    call_regex = '"phones":{"call":\["([^"]+)"\],'
    whatsapp_regex = '"whatsapp":\["([^"]+)"\],'
    title_regex = '"title":"([^"]+)"'  
    price_regex = '"price":([^"]+),' 
    rooms_regex = '"rooms":{"name":"([^"]+)"' 
    baths_regex = '"baths":{"name":"([^"]+)"' 
    area_regex = '"area":([^"]+),' 
    name_regex = '"name":"([^"]+)","firstName"' 
    maps_regex = '"maps":\["([^"]+)"\],'
    lat_regex = '{"lat":([^"]+),'
    lng_regex = ',"lng":([^"]+),'
    garages_regex = '"garages":{"name":"([^"]+)",'
    floor_regex = '"floor":{"name":"([^"]+)",'
    seo_regex = '"seo":{"description":"([^"]+)",'
    propertyType_regex = '"propertyType":{"name":"([^"]+)"}'
    transaction_regex = '"transaction":"([^"]+)"'
    location1_regex = '"location1":"([^"]+)"'
    location2_regex = '"location2":"([^"]+)"'
    condition_regex = '"condition":{"name":"([^"]+)",'
    age_regex = '"age":{"name":"([^"]+)",'
    interior_regex = '"interior":\s*\[([^\]]+)\]'
    exterior_regex = '"exterior":\s*\[([^\]]+)\]'
    sector_regex = '"sector":\s*\[([^\]]+)\]'


    published = []
    updated = [] 
    description = []
    stratum = []
    pricem2 = []
    newflat = [] 
    livingarea = []
    minLivingArea = []
    maxLivingArea = []
    address = []
    contact= []
    call = []
    whatsapp = [] 
    title = []
    price = []
    rooms = []
    baths = []
    area = []
    name = []
    maps = []
    lat = []
    lng = []
    garages = []
    floor = []
    seo = []
    propertyType = []
    transaction = []
    location1 = []
    location2 = []
    condition = []
    age = []
    categories_interior = []
    categories_exterior = []
    categories_sector = []

    links = []

    # Assuming scraped_data is a DataFrame with a column 'Url'
    for index, row in df.iterrows():
        link = row['Url']
        links.append(link)
        apply_regex(public_regex, 'general', published, row)
        apply_regex(updated_regex, 'general', updated, row)
        apply_regex(description_regex, 'general', description, row)
        apply_regex(stratum_regex, 'general', stratum, row)
        apply_regex(pricem2_regex, 'general', pricem2, row)
        apply_regex(newflat_regex, 'general', newflat, row)
        apply_regex(livingarea_regex, 'general', livingarea, row)
        apply_regex(minLivingArea_regex, 'general', minLivingArea, row)
        apply_regex(maxLivingArea_regex, 'general', maxLivingArea, row)
        apply_regex(address_regex, 'general', address, row)
        apply_regex(contact_regex, 'general', contact, row)
        apply_regex(call_regex, 'general', call, row)
        apply_regex(whatsapp_regex, 'general', whatsapp, row)   
        apply_regex(title_regex, 'general', title, row)
        apply_regex(price_regex, 'general', price, row)
        apply_regex(rooms_regex, 'general', rooms, row)
        apply_regex(baths_regex, 'general', baths, row)
        apply_regex(area_regex, 'general', area, row)
        apply_regex(name_regex, 'general', name, row)
        apply_regex(maps_regex, 'general', maps, row)
        apply_regex(lat_regex, 'general', lat, row)
        apply_regex(lng_regex, 'general', lng, row)
        apply_regex(garages_regex, 'general', garages, row)
        apply_regex(floor_regex, 'general', floor, row)
        apply_regex(seo_regex, 'general', seo, row) 
        apply_regex(propertyType_regex, 'general', propertyType, row)
        apply_regex(transaction_regex, 'general', transaction, row) 
        apply_regex(location1_regex, 'general', location1, row) 
        apply_regex(location2_regex, 'general', location2, row) 
        apply_regex(condition_regex, 'general', condition, row) 
        apply_regex(age_regex, 'general', age, row) 
        apply_regex(interior_regex, 'general', categories_interior, row) 
        apply_regex(exterior_regex, 'general', categories_exterior, row) 
        apply_regex(sector_regex, 'general', categories_sector, row) 




    # Create a new DataFrame or column with the results
    new_df = pd.DataFrame({'diaPublicado': published, 
                           'diaActualizado':updated,
                           'descripcion':description,
                           'estrato':stratum,
                           'preciom2':pricem2,
                           'inmuebleNuevo':newflat,
                           'livingArea':livingarea,
                           'minLivingArea':minLivingArea,
                           'maxLivingArea':maxLivingArea, 
                           'ubicacion':address,
                           'contact':contact,
                           'call':call,
                           'whatsapp':whatsapp,
                           'inmu_op': title,
                           'price':price,
                           'rooms':rooms,
                           'baths':baths,
                           'area':area,
                           'publicado_por':name,
                           'maps':maps,
                           'latitud':lat,
                           'longitud':lng,
                           'garages':garages,
                           'floor':floor,
                           'seo':seo,
                           'propertyType':propertyType,
                           'operation':transaction,
                           'location1':location1,
                           'location2':location2,
                           'condition':condition,
                           'age':age,
                           'interior':categories_interior,
                           'exterior':categories_exterior,
                           'sector':categories_sector,
                           'Url': links})
    new2_df = new_df.copy()

    # Aplicar la función a la columna 'interior'
    new2_df['interior'] = new2_df['interior'].apply(extract_names)
    new2_df['exterior'] = new2_df['exterior'].apply(extract_names)
    new2_df['sector'] = new2_df['sector'].apply(extract_names)

    new2_df['estrato'] = new2_df['estrato'].str.replace('Estrato ', '')
    new2_df['Codigo'] = new2_df['Url'].str.extract(r'(\d+)$')

    new2_df['latitud'] = new2_df['latitud'].apply(lambda x: str(x).replace('.', ','))
    new2_df['longitud'] = new2_df['longitud'].apply(lambda x: str(x).replace('.', ','))
    new2_df['preciom2'] = new2_df['preciom2'].apply(lambda x: str(x).replace('.', ','))
    
    new2_df['Consulta'] = pd.Timestamp.now()
    new2_df[['tipo_inmueble', 'operation']] = new2_df.apply(obtener_palabras, axis=1)
    return new2_df

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

def internal(df):
    #Driver directory:
    DRIVER = 'C:/Users/luisG/GIT/SCRAPING/DRIVER/chromedriver.exe'
    minutes = 5


    service = Service(f'{DRIVER}')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Desactivar sandboxing
    
    driver = webdriver.Chrome(service=service, options=options)

    enlaces_list = []
    general = []
    total_enlaces = len(df)
    enlaces_procesados = 0
    enlaces_procesados_desde_ultima_cierre = 0
    last_reset_time = get_current_time()

    try:
        start_time = datetime.now()
        print(f"El proceso de scraping ha comenzado a las {start_time.strftime('%H:%M')} del {start_time.strftime('%d/%m/%Y')}")
        
        index = 0
        continue_scraping = True

        while continue_scraping and index < len(df):
            tiempo = randomtime()
            row = df.iloc[index]
            enlaces_procesados += 1
            enlaces_procesados_desde_ultima_cierre += 1
            link = row['Link']

            current_time = get_current_time()
            elapsed_time = current_time - last_reset_time

            if elapsed_time >= timedelta(minutes=minutes):
                try:
                    driver.quit()
                    print("Han pasado 5 minutos. Reiniciando el driver...")

                    driver = webdriver.Chrome(service=service, options=options)
                    last_reset_time = get_current_time()
                    enlaces_procesados_desde_ultima_cierre = 0
                except Exception as quit_exception:
                    print(f"Error al cerrar o abrir el driver: {quit_exception}")

            if enlaces_procesados % 50 == 0:
                print(f"Enlaces procesados: {enlaces_procesados} de {total_enlaces}")

            try:
                driver.get(link)
                time.sleep(tiempo)

                div_general = driver.find_elements(By.XPATH, '//script[contains(@id, "__NEXT_DATA__")]')
                gen = div_elements(div_general, general)
                enlaces_list.append(link)

            except Exception as e:
                print(f"Se produjo un error al cargar el enlace: {link}")
                print(f"Excepción: {str(e)}")
                print("Reiniciando el driver y continuando con el próximo enlace...")
                driver.quit()
                driver = webdriver.Chrome(service=service, options=options)

            else:
                index += 1

    except Exception as e:
        print(f"Se produjo un error en el scraping: {e}")

    finally:
        try:
            driver.quit()
        except Exception as quit_exception:
            print(f"Error al cerrar el driver en finally: {quit_exception}")

    data_list = []

    for gen_v, link in zip(gen, enlaces_list):
        row_data = {
            'general': gen_v,
            'Url': link
        }
        data_list.append(row_data)
    df = pd.DataFrame(data_list)

    aviso = f"¡El DataFrame de tamaño {df.shape} df_inmobiliarias de FINCA RAIZ está disponible para su análisis!"
    display(HTML(f"<div style='background-color: #b8daba; padding: 10px; border: 1px solid #007723; border-radius: 5px;'><strong>IMBUEBLES DISPONIBLE:</strong> {aviso}</div>"))

    return df