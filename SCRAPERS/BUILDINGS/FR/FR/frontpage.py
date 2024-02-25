
import pandas as pd 
import re 
import time



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  
from selenium.common.exceptions import NoSuchElementException


from .tools import randomtime
from .directories import driver_directory


def scrapeFrontPage(link):  
    '''
    The function is the main 
    scraper for the principal page in FR webpage. 
    This function iterates 40 pages in the website, 
    this depends if there is information in the main url.
    '''

    # Driver directory:
    driver_path = driver_directory()
    DRIVER = driver_path
    tiempo = randomtime()
    pages = 40
    # Initilize the options of the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")  
    service = Service(f'{DRIVER}')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(link)

    list_html_data = []

    def parse_html(html_content):
        return {'HTML_Content': html_content}

    # Iterate fos the maximun nomber of pages (40, for this website), and get the information
    for i in range(pages):
        try:

            div_elements = driver.find_elements(By.XPATH, "//article[contains(@class, 'MuiPaper-outlined MuiPaper-rounded')]")
            df_rows = []

            # Iterate each html element text, and save it in a dataframe
            for element in div_elements:
                html_content = element.get_attribute('outerHTML')
                data = parse_html(html_content)
                df_rows.append(data)
            
            list_html_data.extend(df_rows)

            #################################################################
            ############  Go to the next oage and continuing scraping 
            #################################################################

            next_button_xpath = '//ul[contains(@class, "MuiPagination-ul")]/li/button[contains(@aria-label, "Go to next page")]'
            next_button_alt_xpath = '//button[contains(@aria-label, "Go to next page")]'

            try:
                next_button = driver.find_element(By.XPATH, next_button_xpath)
                if not next_button.get_attribute("disabled"):
                    driver.execute_script("arguments[0].click();", next_button)
                else:
                    next_button_alt = driver.find_element(By.XPATH, next_button_alt_xpath)
                    if not next_button_alt.get_attribute("disabled"):
                        driver.execute_script("arguments[0].click();", next_button_alt)
                    else:
                        break
            except NoSuchElementException:
                break
                
            time.sleep(tiempo)


        except Exception as e:
            print(f"Error al procesar la página {i+1}: {str(e)}")
            break

    # Save the scraped data in a dataframe 
    df = pd.DataFrame(list_html_data)

    driver.quit()
    time.sleep(tiempo)

    return df


def regexFrontData(df):

    '''
    This funciton helps to clean the information. 
    At first time is a text of html, however,  
    with this, is going to get all the information 
    visible you can extract. 
    '''
    # Regular expressions of the data for extract 
    enlaces_regex = r'href="(/[^"]+)"'
    destacados_regex = r'<span[^>]*>([^<]+)</span>'
    ubicacion_regex = r'title="([^"]+)"'
    publicado_regex = r'<span>Por <\/span><span><b>([^<]+)<\/b></span>'
    proyectos_regex = r'<span>.*?<b>([^<]+)</b>.*?</span>'
    precios_regex = r'<b>([^<]+)</b>'
    descrip_regex = r'alt="([^"]+)"'
    areas_regex = r'(Áreas desde\s*([\d,\.]+m)|(\d+\.?\d*m²))'
    habs_regex = r'(\d+)\s*ha\.'
    banos_regex = r'(\d+)\s*ba\.'
    parking_regex = r'(\d+)\s*pa\.'
    
    # Create lists for storage the results 
    lista_enlaces = []
    destacado = []
    ubicacion = []
    publicado = []
    proy = []
    prec = []
    area = []
    habs = []
    baths = []
    park = []
    descrip = []

    # Iterate between the rows 
    for index, row in df.iterrows():
        html_content = row['HTML_Content']

        # Apply the regular expressions for get the relevant information 
        enlaces_match = re.search(enlaces_regex, html_content)
        enlace = enlaces_match.group(1) if enlaces_match else ''
        lista_enlaces.append(enlace)

        destacados_match = re.search(destacados_regex, html_content)
        destacado_text = destacados_match.group(1) if destacados_match else ''
        destacado.append(destacado_text)

        ubicacion_match = re.search(ubicacion_regex, html_content)
        ubicacion_text = ubicacion_match.group(1) if ubicacion_match else ''
        ubicacion.append(ubicacion_text)

        publicado_match = re.search(publicado_regex, html_content)
        publicado_text = publicado_match.group(1) if publicado_match else 'Anuncio Particular'
        publicado.append(publicado_text)

        proyectos_match = re.search(proyectos_regex, html_content)
        proy_text = proyectos_match.group(1) if proyectos_match else ''
        proy.append(proy_text)

        precios_match = re.search(precios_regex, html_content)
        prec_text = precios_match.group(1) if precios_match else ''
        prec.append(prec_text)

        areas_match = re.search(areas_regex, html_content)
        area_text = areas_match.group(1) if areas_match else ''
        area.append(area_text)
        
        habs_match = re.search(habs_regex, html_content)
        habs_text = habs_match.group(1) if habs_match else ''
        habs.append(habs_text)

        baths_match = re.search(banos_regex, html_content)
        baths_text = baths_match.group(1) if baths_match else ''
        baths.append(baths_text)
        
        park_match = re.search(parking_regex, html_content)
        park_text = park_match.group(1) if park_match else ''
        park.append(park_text)
        
        descrip_match = re.search(descrip_regex, html_content)
        descrip_text = descrip_match.group(1) if descrip_match else ''
        descrip.append(descrip_text)


    # Add the lists to a dataframe  
    df['Link'] = lista_enlaces
    df['Link'] = 'https://www.fincaraiz.com.co' + df['Link']
    df['Destacado'] = destacado
    df['Ubicacion'] = ubicacion
    df[['Zona', 'ciudad_municipio']] = df['Ubicacion'].str.split(' - ', n=1, expand=True)
    df['Publicado_por'] = publicado
    df['Tipo'] = proy
    df['Precio'] = prec
    df['Area'] = area
    df['Habitaciones'] = habs
    df['Banos'] = baths
    df['Parqueaderos'] = park
    df['Descripcion'] = descrip
    df['Codigo'] = df['Link'].str.extract(r'(\d+)$')
    df['Consulta'] = pd.Timestamp.now()
    df['WEB'] = 'FR'

    df['Inmueble'] = df['Tipo'].apply(lambda x: x.split(" ")[0] if isinstance(x, str) and len(x.split(" ")) > 1 else None)
    df['Operacion'] = df['Tipo'].apply(lambda x: x.split(" ")[2] if isinstance(x, str) and len(x.split(" ")) >= 3 else None)
    
    df.drop(['HTML_Content'], axis=1, inplace=True)
    df = df.drop_duplicates(subset=['Codigo'])
    
    return df