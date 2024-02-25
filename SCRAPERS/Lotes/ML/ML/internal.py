
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
    #Funcion de regex de aquellos que no requieren union
    def apply_regex(regex, name_row, list_empty, row):
        row_dict = row[name_row]

        if isinstance(row_dict, dict):
            general = row_dict.values()
            general = list(general)[0]  # Convierte el valor del diccionario a una cadena de texto
            match = re.search(regex, general)
            text = match.group(1) if match else ''
            list_empty.append(text)
        else:
            list_empty.append('')

        return list_empty
    #Funcion de regex de aquellos que requieren union debido a la extrctura html
    def combined_regex(regex, name_row, list_empty, row):
        row_dict = row[name_row]

        if isinstance(row_dict, dict):
            general = row_dict.values()
            general = list(general)[0]  # Convierte el valor del diccionario a una cadena de texto
            match = re.search(regex, general)
            text1 = match.group(1) if match else ''
            text2 = match.group(2) if match else ''
            combined_text = f"{text1} {text2}"
            list_empty.append(combined_text)
        else:
            list_empty.append('')

        return list_empty
    
    
    features_1 = '<span class="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-label">'
    features_2 = '<div class="andes-table__header__container">'
    features_21 = '</div>.*?<span class="andes-table__column--value" style="line-clamp:none;-webkit-line-clamp:none">([^<]+)</span>'

    public_regex = '<p class="ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle">([^<]+)</p>'    
    subtitle_regex = r'<h1 class="ui-pdp-title">([^<]+)</h1>'
    tipo_regex = r'<span class="ui-pdp-subtitle">([^<]+)</span>'
    verfied_regex = r'<p class="ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-seller-validated__title">([^<]+)<a target="_self" href="#seller_profile">([^<]+)</a>'
    price_regex = r'<span class="andes-money-amount__fraction" aria-hidden="true">([^<]+)</span>'
    area_regex = fr'{features_1}([^<]+\s?m²[^<]+)</span>'
    habs_regex = fr'{features_1}([^<]+\s?hab[^<]+)</span>'
    baths_regex = fr'{features_1}([^<]+\s?ba[^<]+)</span>'
    
    location_regex = r'<p class="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title">([^<]+)</p>'
    located_regex = r'center=([^&]+)'
    
    area_total_regex = fr'{features_2}Área total{features_21}'
    area_contruida_regex = fr'{features_2}Área construida{features_21}'    
    habitaciones_regex = fr'{features_2}Habitaciones{features_21}'
    bahos_regex = fr'{features_2}Baños{features_21}'
    estacionamientos_regex = fr'{features_2}Estacionamientos{features_21}'
    antique_regex = fr'{features_2}Antigüedad{features_21}'
    gas_regex = fr'{features_2}Gas natural{features_21}'
    armarios_regex = fr'{features_2}Armarios{features_21}'
    lavanderia_regex = fr'{features_2}Lavandería{features_21}'
    estrato_regex = fr'{features_2}Estrato social{features_21}'
    amoblado_regex = fr'{features_2}Amoblado{features_21}'
    depositos_regex = fr'{features_2}Depósitos{features_21}'
    air_regex = fr'{features_2}Aire acondicionado{features_21}'
    admin_regex = fr'{features_2}Administración{features_21}'
    balcon_regex = fr'{features_2}Balcón{features_21}'
    pisos_regex = fr'{features_2}Cantidad de pisos{features_21}'

    seguridad_regex = fr'{features_2}Seguridad{features_21}'
    juegos_infantiles_regex = fr'{features_2}Área de juegos infantiles{features_21}'
    calefaccion_regex = fr'{features_2}Calefacción{features_21}'
    mascotas_regex = fr'{features_2}Admite mascotas{features_21}'



    
    description_regex = r'<p class="ui-pdp-description__content">(.*?)</p>'
    
    compania_regex = r'<h3 class="ui-pdp-color--BLACK ui-pdp-size--LARGE ui-pdp-family--REGULAR">(.*?)</h3>'
    codigoreal_regex = r'<h3 class="ui-seller-info__status-info__title ui-vip-seller-profile__title">([^<]+)</h3><p class="ui-seller-info__status-info__subtitle">([^<]+)</p>'

    # By regex
    tipo_operacion = []
    subtitle = []
    public_ago = []
    verified = []
    price = []
    area = []
    habs = []
    baths = []
    
    location = []
    located = []
    
    total_area = []
    contruc_area = []
    habitaciones = []
    bahnos = []
    estaciones = []
    antiguedad = []
    gas = []
    armarios = []
    lavanderia = []
    estrato = []
    amoblado = []
    depositos = [] #se refiere a áticos 
    air = []
    admin = []
    balcon = []
    pisos = []
    seguridad = []
    juegos_infantiles = [] 
    calefaccion = []
    mascotas = []

    description = []
    
    compania = []
    codigoreal = []

    
    links = []
    #By fixing information
    lon = []
    lat = []
    type = []
    op = []


    #created
    web = 'ML'

    for index, row in df.iterrows():
        link = row['Url']
        links.append(link)
        tipo_operacion = apply_regex(tipo_regex, 'general', tipo_operacion, row)
        subtitle = apply_regex(subtitle_regex, 'general', subtitle, row)
        public_ago = apply_regex(public_regex, 'general', public_ago, row)
        verified = combined_regex(verfied_regex, 'general', verified, row) #combinado
        price = apply_regex(price_regex, 'general', price, row)
        area = apply_regex(area_regex, 'general', area, row)
        habs = apply_regex(habs_regex, 'general', habs, row)
        baths = apply_regex(baths_regex, 'general', baths, row)
        
        location = apply_regex(location_regex, 'location', location, row)
        located = apply_regex(located_regex, 'location', located, row)
        
        total_area = apply_regex(area_total_regex, 'features', total_area, row)
        contruc_area = apply_regex(area_contruida_regex, 'features', contruc_area, row)
        
        habitaciones = apply_regex(habitaciones_regex, 'features', habitaciones, row)
        bahnos = apply_regex(bahos_regex, 'features', bahnos, row)
        estaciones = apply_regex(estacionamientos_regex, 'features', estaciones, row)
        antiguedad = apply_regex(antique_regex, 'features', antiguedad, row)
        gas = apply_regex(gas_regex, 'features', gas, row)
        armarios = apply_regex(armarios_regex, 'features', armarios, row)
        lavanderia = apply_regex(lavanderia_regex, 'features', lavanderia, row)
        estrato = apply_regex(estrato_regex, 'features', estrato, row)
        
        amoblado = apply_regex(amoblado_regex, 'features', amoblado, row)
        depositos = apply_regex(depositos_regex, 'features', depositos, row)
        air = apply_regex(air_regex, 'features', air, row)
        admin = apply_regex(admin_regex, 'features', admin, row)
        balcon = apply_regex(balcon_regex, 'features', balcon, row)
        pisos = apply_regex(pisos_regex, 'features', pisos, row)

        seguridad = apply_regex(seguridad_regex, 'features', seguridad, row)
        juegos_infantiles = apply_regex(juegos_infantiles_regex, 'features', juegos_infantiles, row)
        calefaccion = apply_regex(calefaccion_regex, 'features', calefaccion, row)
        mascotas = apply_regex(mascotas_regex, 'features', mascotas, row)

        
        description = apply_regex(description_regex, 'description', description, row)
        
        compania = apply_regex(compania_regex, 'publish', compania, row)
        codigoreal = combined_regex(codigoreal_regex, 'publish', codigoreal, row) # combinado

        lat = [x.split('%2C')[0] if isinstance(x, str) and '%2C' in x else None for x in located]
        lon = [x.split('%2C')[1] if isinstance(x, str) and '%2C' in x else None for x in located]

        type = [x.split(" ")[0] if isinstance(x, str) and len(x.split(" ")) > 1 else None for x in tipo_operacion]
        op = [x.split(" ")[2] if isinstance(x, str) and len(x.split(" ")) > 1 else None for x in tipo_operacion]

    # Luego, crea un nuevo DataFrame o columna con los resultados
    new_df = pd.DataFrame({'diaActualizado':'',
                          'diaPublicado':public_ago,
                          'Descripcion': description,
                          'estrato': estrato,
                          'preciom2':'', 
                          'inmuebleNuevo':'',
                          'livingArea':'',
                          'minLivingArea':'',
                          'maxLivingArea':'', 
                          'ubicacion': location,
                          'contact':'',
                          'call':'',
                          'whatsapp':'',
                          'inmu_op': tipo_operacion,
                          'price':price,
                          'rooms':habs,
                          'baths':baths,
                          'area': area,
                          'publicado_por': compania, 
                          'maps':located,
                          'latitud':lat,
                          'longitud':lon,
                          'garages':estaciones,
                          'floor': pisos, 
                          'seo':subtitle,
                          'verified':verified,
                          'propertyType':type,
                          'operation':op, 
                          'location1':'',
                          'location2':'',
                          'condition':'',
                          'age':antiguedad,
                          'interior':'',
                          'exterior':'',
                          'sector':'',
                          'Area_total':total_area,
                          'Area_construida':contruc_area,
                          'Habitaciones2':habitaciones,
                          'Banos2':bahnos,
                          'Gas_servicio':gas,
                          'Armarios':armarios,
                          'Lavanderia':lavanderia, 
                          'Amobladoi': amoblado,
                          'Deposito': depositos, 
                          'Aire_acondicionado': air,
                          'Administracion': admin,
                          'Balcon': balcon,
                          'Seguridad':seguridad,
                          'Juegos_infantiles':juegos_infantiles,
                          'Calefaccion':calefaccion,
                          'Mascotas':mascotas,
                          'Codigo_inmueble': codigoreal,
                          'Url': links,
                          'WEB': web
                          })
    
    
    #Arreglos del nuevo df
    new_df['diaPublicado'] = new_df['diaPublicado'].str.replace("Publicado hace", "")
    new_df['price'] = new_df['price'].str.replace(".", "")
    new_df['area'] = new_df['area'].str.replace("m²", "").str.replace("totales", "")
    new_df['rooms'] = new_df['rooms'].str.replace("habitaciones", "").str.replace("habitación", "").str.replace(" ", "")

    new_df['baths'] = new_df['baths'].str.replace("baños", "").str.replace("baño", "").str.replace(" ", "")
    new_df['Codigo_inmueble'] = new_df['Codigo_inmueble'].str.replace("Código de la propiedad", "").str.replace(" ", "")
    new_df['Area_construida'] = new_df['Area_construida'].str.replace("m²", "").str.replace(" ", "")
    new_df['Area_total'] = new_df['Area_total'].str.replace("m²", "").str.replace(" ", "")
    new_df['Descripcion'] = new_df['Descripcion'].str.replace("<br>", " ")
    new_df['longitud'] = new_df['longitud'].str.replace(".", ",")
    new_df['latitud'] = new_df['latitud'].str.replace(".", ",")
    new_df['Codigo'] = new_df['Url'].apply(lambda x: x.split("/")[3] if isinstance(x, str) and len(x.split("/")) > 3 else None)
    new_df['Codigo'] = new_df['Codigo'].apply(lambda x: x.split("-")[1] if isinstance(x, str) and len(x.split("-")) > 4 else None)
    new_df['Consulta'] = pd.Timestamp.now()
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

def internal(df):

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
    location = []
    features = []
    description = []  
    publishby = []

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
                driver.get(link)
                time.sleep(tiempo)

                #Generales 
                #############################################################################################
                div_general = driver.find_elements(By.XPATH, '//div[contains(@class, "ui-vip-core-container--column__right")]')
                
                #Locación 
                #############################################################################################
                div_location = driver.find_elements(By.XPATH, '//div[contains(@class, "ui-pdp-container__row ui-pdp-container__row--location")]')
                
                #Caracteristicas_destacadas 
                #############################################################################################
                div_features = driver.find_elements(By.XPATH, '//section[contains(@class, "ui-vpp-highlighted-specs pl-0 pr-0")]')
                
                #Descripcion inmueble 
                #############################################################################################
                div_description = driver.find_elements(By.XPATH, '//div[contains(@id, "description")]')
                

                #Publicado por y hace
                div_publish= driver.find_elements(By.XPATH, '//div[contains(@class, "ui-vip-seller-profile ui-box-component")]')
                
                
                gen = div_elements(div_general, general)
                loc = div_elements(div_location, location)
                fea = div_elements(div_features, features)
                des = div_elements(div_description, description)
                pub = div_elements(div_publish, publishby)
                
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


    data_list = []  # publicado_hace_val,
    # publicado_hace_val,
    for gen_v, loc_v, fea_v, des_v, pub_v, link in zip(
             gen, loc, fea, des, pub, enlaces_list
    ):
        row_data = {
            'general': gen_v,
            'location': loc_v,
            'features': fea_v,
            'description': des_v,
            'publish':pub_v,
            'Url': link  # Utilizamos el enlace de scraping en tiempo real
        }
        data_list.append(row_data)
    df = pd.DataFrame(data_list) 

    
    # Mensaje de aviso de que el scraping terminó
    aviso = f"¡El DataFrame de tamaño {df.shape} df_inmobiliarias de FINCA RAIZ está disponible para su análisis!"
    display(HTML(f"<div style='background-color: #b8daba; padding: 10px; border: 1px solid #007723; border-radius: 5px;'><strong>IMBUEBLES DISPONIBLE:</strong> {aviso}</div>"))
    
    return df
