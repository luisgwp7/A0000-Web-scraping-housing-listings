import pandas as pd 
import re 
import time



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  


from .tools import randomtime
from .directories import driver_directory


def frontpage(link):

    '''
    The function is the main 
    scraper for the principal page in ML webpage. 
    This function iterates 50 pages in the website, 
    this depends if there is information in the main url.
    '''
    # Driver directory:
    driver_path = driver_directory()
    DRIVER = driver_path
    tiempo = randomtime()
    pages = 50
    # Initilize the options of the webdriver
    options = webdriver.ChromeOptions()
    service = Service(f'{DRIVER}')
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument("--no-sandbox")  # Desactivar sandboxing
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(link)

    # Creación de lista vacía para almacenar todos datos
    dataX = []

    def parse_html(html_content):
        return {'HTML_Content': html_content}
    # Iterate fos the maximun nomber of pages (40, for this website), and get the information
    for i in range(pages):
        try:
            div_elements = driver.find_elements(By.XPATH, '//ol/div/li[contains(@class, "ui-search-layout__item")]')
            df_rows = []

            # Iterate each html element text, and save it in a dataframe
            for element in div_elements:
                html_content = element.get_attribute('outerHTML')
                data = parse_html(html_content)
                df_rows.append(data)
                
            dataX.extend(df_rows)
            #################################################################
            ############  Go to the next oage and continuing scraping 
            #################################################################

            try: 
                next_button = driver.find_element(By.XPATH, '//a[@title="Siguiente"]')
                driver.execute_script("arguments[0].click();", next_button)
            except:
                break
            time.sleep(tiempo)


        except Exception as e:
            print(f"Error al procesar la página {i+1}: {str(e)}")
            break

    # Save the scraped data in a dataframe 
    df = pd.DataFrame(dataX)

    driver.quit()
    time.sleep(tiempo)

    return df


def regexdata(df):

    '''
    This funciton helps to clean the information. 
    At first time is a text of html, however,  
    with this, is going to get all the information 
    visible you can extract. 
    '''
    # Regular expressions of the data for extract 
    enlaces_regex = r'href="([^"]+)"'
    tipo_regex = r'<span class="ui-search-item__group__element ui-search-item__subtitle-grid">([^<]+)</span>'
    publicado_regex = r'<h2[^>]*>([^<]+)</h2>'
    precios_regex = r'<span class="andes-money-amount__fraction" aria-hidden="true">([\d.]+)</span>'
    banos_regex = r'(\d+\s?baño)'
    habs_regex = r'(\d+\s?habita)' 
    areas_regex = r'(\d+\s?m²)'
    ubicacion_regex = r'<span class="ui-search-item__location-label">([^<]+)</span>'
    destacado2_regex = r'<div class="ui-search-item__highlighted-label">([^<]+)</div>'
    
    # Create lists for storage the results 

    lista_enlaces = []
    publicado = []
    prec = []
    baths = []
    habs = []
    area = []
    ubicacion = []
    destacado2 = []
    tipo = []

    # Iterate between the rows 
    for index, row in df.iterrows():
        html_content = row['HTML_Content']

        # Apply the regular expressions for get the relevant information 
        enlaces_match = re.search(enlaces_regex, html_content)
        enlace = enlaces_match.group(1) if enlaces_match else ''
        lista_enlaces.append(enlace)

        publicado_match = re.search(publicado_regex, html_content)
        publicado_text = publicado_match.group(1) if publicado_match else 'Anuncio Particular'
        publicado.append(publicado_text)

        precios_match = re.search(precios_regex, html_content)
        prec_text = precios_match.group(1) if precios_match else ''
        prec.append(prec_text)

        baths_match = re.search(banos_regex, html_content)
        baths_text = baths_match.group(1) if baths_match else ''
        baths.append(baths_text)

        habs_match = re.search(habs_regex, html_content)
        habs_text = habs_match.group(1) if habs_match else ''
        habs.append(habs_text)

        areas_match = re.search(areas_regex, html_content)
        area_text = areas_match.group(1) if areas_match else ''
        area.append(area_text) 

        ubicacion_match = re.search(ubicacion_regex, html_content)
        ubicacion_text = ubicacion_match.group(1) if ubicacion_match else ''
        ubicacion.append(ubicacion_text)

        destacados2_match = re.search(destacado2_regex, html_content)
        destacado2_text = destacados2_match.group(1) if destacados2_match else ''
        destacado2.append(destacado2_text)

        tipo_match = re.search(tipo_regex, html_content)
        tipo_text = tipo_match.group(1) if tipo_match else ''
        tipo.append(tipo_text)

    # Add the lists to a dataframe  
    df['Link'] = lista_enlaces
    df['Link'] = df['Link'].str.replace(";", ".")

    df['Destacado'] = destacado2
    df['Ubicacion'] = ubicacion
    df[['Zona', 'ciudad_municipio']] = ''
    df['Publicado_por'] = ''
    df['Tipo'] = tipo
    df['Precio'] = prec
    df['Area'] = area
    df['Habitaciones'] = habs
    df['Banos'] = baths
    df['Parqueaderos'] = ''
    df['Descripcion'] = publicado
    
    

    # Other changes of the data 
    df['Precio'] = df['Precio'].str.replace(".", "")
    df['Banos'] = df['Banos'].str.replace(" baño", "")
    df['Habitaciones'] = df['Habitaciones'].str.replace(" habita", "")
    df['Area'] = df['Area'].str.replace("m²", "")
    df['Codigo'] = df['Link'].apply(lambda x: x.split("/")[3] if isinstance(x, str) and len(x.split("/")) > 3 else None)
    df['Codigo'] = df['Codigo'].apply(lambda x: x.split("-")[1] if isinstance(x, str) and len(x.split("-")) > 4 else None)
    df['Consulta'] = pd.Timestamp.now()
    df['WEB'] = 'ML'
    
    df['Inmueble'] = df['Tipo'].apply(lambda x: x.split(" ")[0] if isinstance(x, str) and len(x.split(" ")) > 1 else None)
    df['Operacion'] = df['Tipo'].apply(lambda x: x.split(" ")[2] if isinstance(x, str) and len(x.split(" ")) > 1 else None)

    df.drop(['HTML_Content'], axis=1, inplace=True)
    df = df.drop_duplicates(subset=['Codigo'])
    
    return df
