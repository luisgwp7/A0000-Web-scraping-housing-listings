
import pandas as pd 
import re 
import time

from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from IPython.display import display, HTML

from .tools import randomtime
from .directories import driver_directory

def getCurrentTime():
    return datetime.now()


def selectdfQ(df, Q, operacion):
    '''
    As you have diferect notebooks for run them at the same time 
    in different machines, this function selects the df to scrap. 
    Note that the principal df is splited in 4 parts, for the same 
    reason, you are going to have 4 notebooks for each operation, :
    "Venta" "Arriendo"
    Q: is the number of the df could be 1, 2, 3, 4
    '''
    # Excluir proyectos y dejar solo lo que tiene que ver con inmuebles 
    df_inmobiliaria = df[df.Tipo.isin([f'Apartamento en {operacion}', 
                                       f'Casa en {operacion}', 
                                       f'Apartaestudio en {operacion}',])].reset_index(drop=True)


    total_filas = len(df_inmobiliaria)
    tamaño_cuarto = total_filas // 4
    
    # Split the df in four parts  
    dfQ1 = df_inmobiliaria.iloc[:tamaño_cuarto]
    dfQ2 = df_inmobiliaria.iloc[tamaño_cuarto:tamaño_cuarto*2]
    dfQ3 = df_inmobiliaria.iloc[tamaño_cuarto*2:tamaño_cuarto*3]
    dfQ4 = df_inmobiliaria.iloc[tamaño_cuarto*3:]

    #Return the df according to the input of Q 
    if Q == 1:
        return dfQ1, print(f'You selected dfQ1 with: {len(dfQ1)} observations')
    elif Q == 2:
        return dfQ2, print(f'You selected dfQ2 with: {len(dfQ2)} observations')
    elif Q == 3:
        return dfQ3, print(f'You selected dfQ3 with: {len(dfQ3)} observations')
    elif Q == 4:
        return dfQ4, print(f'You selected dfQ4 with: {len(dfQ4)} observations')
    else:
        print("Error: Q must be a number between 1 and 4.")



def div_elements(div_element, Emptylist):
    
    '''
    div_elements: Is used in the scraper for storage the data.

    '''
    def parse_html(html_content):
        return {f'{div_element}': html_content}

    df_rows = []

    for element in div_element:
        html_content = element.get_attribute('outerHTML')
        data = parse_html(html_content)
        df_rows.append(data)
    if not df_rows:
        df_rows = ['']  

    Emptylist.extend(df_rows)

    return Emptylist




def obtener_palabras(row):
    '''
    obtener_palabras: Is used in function 
    regexdata() which clean the data.

    '''
    palabras = row['inmu_op'].split()
    tipo_inmueble = palabras[0] if palabras else None
    operation = palabras[-1] if palabras else None
    return pd.Series([tipo_inmueble, operation], index=['tipo_inmueble', 'operation'])




def regexInternalData(df):
    '''
    regexdata: This function uses the regular expressions for convert the 
    html text in real data.

    '''
    def apply_regex(regex, name_row, list_empty, row):
        '''
        Extracts text from a nested dictionary value in a 
        specified row using a regular expression.

        Parameters:
        - regex (str): The regular expression pattern to be applied.
        - name_row (str): The key representing the desired value in the dictionary (row_dict).
        - list_empty (list): A list where the extracted text or an empty string will be appended.
        - row (dict): The dictionary containing the data.

        Returns:
        None. Modifies list_empty in place.

        Usage:
        result_list = []
        apply_regex(r'\w+', 'name', result_list, data_row)
        '''
        row_dict = row[name_row]

        if isinstance(row_dict, dict):
            general = row_dict.values()
            # Convert the dictionary value to a string
            general = list(general)[0]  
            match = re.search(regex, general)
            text = match.group(1) if match else ''
            list_empty.append(text)
        else:
            list_empty.append('')

    def extract_names(value):
        # Extracts names from a string using a regular expression.
        matches = re.findall('"name":"([^"]+)"', value)

        # Unir los resultados con el operador '|'
        result = " | ".join(matches)

        return result
    
    # These are all the relevant variables you can get from the...
    # ... principal script that has all the information 

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

    # Initialize the empty list for storage the data of each variable
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

    # Clean the data. 
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




def scrapedInternalPage(df):
    '''
    internal: This is the most important function, 
    the scraper use just one xpath that contains all the information of the page. 
    Aditionaly, the scraper only takes five minutes open, after five minutes, the driver closes itself,
    and start again with the other links storaged in the main df

    '''
    # Driver directory:
    driver_path = driver_directory()
    DRIVER = driver_path
    
    # Time that the driver is open 
    minutes = 5

    # Options and service of the driver
    service = Service(f'{DRIVER}')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)

    enlaces_list = []
    general = []
    total_enlaces = len(df)
    enlaces_procesados = 0
    enlaces_procesados_desde_ultima_cierre = 0
    last_reset_time = getCurrentTime()

    try:
        start_time = datetime.now()
        print(f"The process started at {start_time.strftime('%H:%M')} of {start_time.strftime('%d/%m/%Y')}")
        
        index = 0
        continue_scraping = True

        while continue_scraping and index < len(df):
            tiempo = randomtime()
            row = df.iloc[index]
            enlaces_procesados += 1
            enlaces_procesados_desde_ultima_cierre += 1
            link = row['Link']

            current_time = getCurrentTime()
            elapsed_time = current_time - last_reset_time

            if elapsed_time >= timedelta(minutes=minutes):
                try:
                    driver.quit()
                    print("5 minutes have happened. Restart the driver...")

                    driver = webdriver.Chrome(service=service, options=options)
                    last_reset_time = getCurrentTime()
                    enlaces_procesados_desde_ultima_cierre = 0
                except Exception as quit_exception:
                    print(f"Error in the driver: {quit_exception}")

            if enlaces_procesados % 50 == 0:
                print(f"Url's processed: {enlaces_procesados} of {total_enlaces}")

            try:
                driver.get(link)
                time.sleep(tiempo)

                div_general = driver.find_elements(By.XPATH, '//script[contains(@id, "__NEXT_DATA__")]')
                gen = div_elements(div_general, general)
                enlaces_list.append(link)

            except Exception as e:
                print(f"Error in the url: {link}")
                print(f"Exception: {str(e)}")
                print("Restart the driver and continue with the following url...")
                driver.quit()
                driver = webdriver.Chrome(service=service, options=options)

            else:
                index += 1

    except Exception as e:
        print(f"Error in the scraping: {e}")

    finally:
        try:
            driver.quit()
        except Exception as quit_exception:
            print(f"Error trying to close the driver: {quit_exception}")

    data_list = []

    for gen_v, link in zip(gen, enlaces_list):
        row_data = {
            'general': gen_v,
            'Url': link
        }
        data_list.append(row_data)
    df = pd.DataFrame(data_list)

    aviso = f"¡Your dataframe with {df.shape} observations is available!"
    display(HTML(f"<div style='background-color: #b8daba; padding: 10px; border: 1px solid #007723; border-radius: 5px;'><strong>IMBUEBLES DISPONIBLE:</strong> {aviso}</div>"))

    return df