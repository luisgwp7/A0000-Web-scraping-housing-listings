
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


categorias = ['lotes']

'''
The function frontpage(link, pages) is the main 
scraper for the principal page in FR
'''
def frontpage(link):
    #Driver directory:
    DRIVER = 'C:/Users/luisG/GIT/SCRAPING/DRIVER/chromedriver.exe'
    tiempo = randomtime()
    pages = 40
    # Opciones del webdriver. No abrimos ventanas
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar en modo sin cabeza
    options.add_argument("--no-sandbox")  
    service = Service(f'{DRIVER}')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(link)

    # Creación de lista vacía para almacenar todos datos
    dataX = []

    def parse_html(html_content):
        return {'HTML_Content': html_content}

    for i in range(pages):
        try:

            div_elements = driver.find_elements(By.XPATH, "//article[contains(@class, 'MuiPaper-outlined MuiPaper-rounded')]")
            df_rows = []

            for element in div_elements:
                html_content = element.get_attribute('outerHTML')
                data = parse_html(html_content)
                df_rows.append(data)
            
            # Extender dataX con los datos de la página actual
            dataX.extend(df_rows)

            #################################################################
            ############  Ir a la siguiente pagina y seguir escrapeando
            #################################################################

            # Hacer clic en el botón de siguiente página si está habilitado
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
                        #print("No se encontró el botón 'Siguiente página' o está deshabilitado")
                        break  # Salir del bucle si no hay más páginas disponibles

            except NoSuchElementException:
                #print("No se encontró el botón 'Siguiente página'")
                break
                
            time.sleep(tiempo)


        except Exception as e:
            print(f"Error al procesar la página {i+1}: {str(e)}")
            break

    
    df = pd.DataFrame(dataX)

    # Cierra navegador
    driver.quit()
    time.sleep(tiempo)

    return df


''''
The following function generate all the url's for rental housing in FR
'''

def renturlhousing():
    operaciones = ['venta'] 
 
    global df_enlaces  # Declarar df_enlaces como una variable global
    df_enlaces = pd.DataFrame(columns=["Enlace"])
    enlaces = []

    #########################################################################################################
    #RENTAL PRICE RANGES   
    #########################################################################################################

        # ---------------------- Lotes
    l_v_lotes = [[0, 50000000], [50000000, 90000000], [90000000, 120000000],
                        [120000000, 150000000], [150000000, 170000000], [170000000, 200000000]] 
    
    m_v_lotes = 200000000    

    while m_v_lotes < 2000000000:
        aumento = 50000000  
        nuevo_monto = m_v_lotes + aumento
        if nuevo_monto > 2000000000:
            nuevo_monto = 2000000000
        l_v_lotes.append([m_v_lotes, nuevo_monto])
        m_v_lotes = nuevo_monto

    intervalo = [[2000000000, 3000000000], [3000000000, 4000000000], 
                 [4000000000, 5000000000], [5000000000, 6000000000],
                 [6000000000, 10000000000], [10000000000, 100000000000],
                 [100000000000, 1000000000000]]
    l_v_lotes.extend(intervalo) 

    ##################################################################################################
    #                                      CREACIÓN DE ENLACES
    ##################################################################################################
    for intervalo in l_v_lotes:
        precio_desde = intervalo[0]
        precio_hasta = intervalo[1]
        enlace = f"https://fincaraiz.com.co/{categorias}/{operaciones}?pagina=1&precioDesde={precio_desde}&precioHasta={precio_hasta}"
        enlaces.append(enlace)

    #Generar enlaces para 40 paginas 
    for enlace in enlaces:
        df_enlaces = pd.concat([df_enlaces, pd.DataFrame({"Enlace": [enlace]})], ignore_index=True)

    # Enlaces generados
    enlaces_generados = df_enlaces.shape[0]
    print(f'Usted generó {enlaces_generados} enlaces principales de portada')
    return df_enlaces


def regexdata(df):
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
    
    # Crear listas para almacenar los resultados
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

    # Iterar a través de las filas del DataFrame
    for index, row in df.iterrows():
        html_content = row['HTML_Content']

        # Aplicar las expresiones regulares a los fragmentos de HTML
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


    # Agregar las listas de resultados como nuevas columnas en el DataFrame
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