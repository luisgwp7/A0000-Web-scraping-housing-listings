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

categorias = ['apartamentos', 'casas', 'apartaestudios']

''''
The following function generate all the url's for rental housing in FR
'''
def frontpage(link):
    #Driver directory:
    DRIVER = 'C:/Users/luisG/GIT/SCRAPING/DRIVER/chromedriver.exe'
    tiempo = randomtime()
    pages = 40
    # Opciones del webdriver. No abrimos ventanas
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

    for i in range(pages):
        try:
            div_elements = driver.find_elements(By.XPATH, '//ol/div/li[contains(@class, "ui-search-layout__item")]')
            df_rows = []

            for element in div_elements:
                html_content = element.get_attribute('outerHTML')
                data = parse_html(html_content)
                df_rows.append(data)
                
                # Extender dataX con los datos de la página actual
            dataX.extend(df_rows)
                #Ir a la siguiente página

            try: 
                next_button = driver.find_element(By.XPATH, '//a[@title="Siguiente"]')
                driver.execute_script("arguments[0].click();", next_button)
            except:
                #print('No hay botón')
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


def renturlhousing():
    operaciones = ['arriendo'] 
 
    global df_enlaces  # Declarar df_enlaces como una variable global
    df_enlaces = pd.DataFrame(columns=["Enlace"])
    enlaces = []

    #########################################################################################################
    #RENTAL PRICE RANGES   
    ##################################################################


    l_a_apartamentos = [[0, 600000], [600000, 690000], [690000, 770000],
                            [770000, 840000], [840000, 895000], [895000, 950000]] 
        
    m_a_apartamento = 13500000    
        
    while m_a_apartamento < 1200000:
        aumento = 50000  
        nuevo_monto = m_a_apartamento + aumento
        if nuevo_monto > 1200000:
            nuevo_monto = 1200000
        l_a_apartamentos.append([m_a_apartamento, nuevo_monto])
        m_a_apartamento = nuevo_monto
            
    intervalo = [[1200000, 1300000], [1300000, 1350000], [1350000, 1400000],
                    [1400000, 1490000], [1490000, 1550000], [1550000, 1670000], 
                    [1670000, 1800000], [1800000, 1900000], [1900000, 2000000], 
                    [2000000, 2150000], [2150000, 2350000], [2350000, 2500000],
                    [2500000, 2650000], [2650000, 2900000], [2900000, 3100000],
                    [3100000, 3400000], [3400000, 3600000], [3600000, 3950000],
                    [3950000, 4300000], [4300000, 4700000], [4700000, 5500000],
                    [5500000, 6500000], [6500000, 8000000], [8000000, 10000000],
                    [10000000, 30000000], [30000000, 10000000000]]
    l_a_apartamentos.extend(intervalo)
            
        # ---------------------- CASAS        
    l_a_casas = [[0, 1300000], [1300000, 2000000]]     
    m_a_casas = 2000000    
        
    while m_a_casas < 9000000:
        aumento = 1000000  
        nuevo_monto = m_a_casas + aumento
        if nuevo_monto > 9000000:
            nuevo_monto = 9000000
        l_a_casas.append([m_a_casas, nuevo_monto])
        m_a_casas = nuevo_monto
            
    intervalo = [[9000000, 12000000], [12000000, 20000000], [20000000, 10000000000]]
    l_a_casas.extend(intervalo)    
        
        # ---------------------- APARTAESTUDIOS  
    l_a_apartaestudios = [[0, 850000], [850000, 1300000],
                            [1300000, 2300000], [2300000, 100000000000]]


    ##################################################################################################
    #                                      CREACIÓN DE ENLACES
    ##################################################################################################
    for operacion in operaciones:
        if operacion =='arriendo':
            for categoria in categorias:
                if categoria == 'apartamentos':
                    categoria_str = categoria.replace(' ', '-')
                    for intervalo in l_a_apartamentos:
                        precio_desde = intervalo[0]
                        precio_hasta = intervalo[1]
                        enlace = f"https://listado.mercadolibre.com.co/inmuebles/{categoria_str}/{operacion}/_PriceRange_{precio_desde}-{precio_hasta}"
                        enlaces.append(enlace)
                            
                elif categoria == 'casas':
                    categoria_str = categoria.replace(' ', '-')
                    for intervalo in l_a_casas:
                        precio_desde = intervalo[0]
                        precio_hasta = intervalo[1]
                        enlace = f"https://listado.mercadolibre.com.co/inmuebles/{categoria_str}/{operacion}/_PriceRange_{precio_desde}-{precio_hasta}"
                        enlaces.append(enlace)
                        
                elif categoria == 'apartaestudios':
                    categoria_str = categoria.replace(' ', '-')
                    for intervalo in l_a_apartaestudios:
                        precio_desde = intervalo[0]
                        precio_hasta = intervalo[1]
                        enlace = f"https://listado.mercadolibre.com.co/inmuebles/{categoria_str}/{operacion}/_PriceRange_{precio_desde}-{precio_hasta}"
                        enlaces.append(enlace)

        #Generar enlaces para 40 paginas 
    for enlace in enlaces:
        df_enlaces = pd.concat([df_enlaces, pd.DataFrame({"Enlace": [enlace]})], ignore_index=True)

    print(f'Enlaces generados: {len(df_enlaces)}')
    return df_enlaces


''''
The following function generate all the url's for used housing for sale in FR
'''

def saleurlhousing():
    operaciones = ['venta']
    global df_enlaces  # Declarar df_enlaces como una variable global
    df_enlaces = pd.DataFrame(columns=["Enlace"])
    enlaces = []
    #########################################################################################################
    #                                    RANGOS DE PRECIOS DE VENTAS  
    #########################################################################################################
        
        # ---------------------- APARTAMENTOS
    l_v_apartamento = [[0, 100000000],[100000000, 105000000],
                        [105000000, 110000000],[110000000, 115000000],
                        [115000000, 117500000],[117500000, 120000000],
                        [120000000, 125000000],[125000000, 130000000],
                        [130000000, 135000000]
                        ]

    m_v_apartamento = 135000000

        # Aumento aleatorio hasta llegar a 1000 millones
    while m_v_apartamento < 435000000:
        aumento = 2500000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 435000000:
            nuevo_monto = 435000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto

    intervalo = [[435000000, 440000000], [440000000, 445000000]]
    l_v_apartamento.extend(intervalo)
        
    while m_v_apartamento < 455000000:
        aumento = 2500000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 455000000:
            nuevo_monto = 455000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto
        
        # Aumento aleatorio hasta llegar a 1000 millones
    while m_v_apartamento < 475000000:
        aumento = 5000000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 475000000:
            nuevo_monto = 475000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto

    while m_v_apartamento < 485000000:
        aumento = 2500000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 485000000:
            nuevo_monto = 485000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto

    while m_v_apartamento < 545000000:
        aumento = 5000000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 545000000:
            nuevo_monto = 545000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto 

    while m_v_apartamento < 565000000:
        aumento = 2500000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 565000000:
            nuevo_monto = 565000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto 

    while m_v_apartamento < 645000000:
        aumento = 5000000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 645000000:
            nuevo_monto = 645000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto 

    while m_v_apartamento < 655000000:
        aumento = 2500000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 655000000:
            nuevo_monto = 655000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto

    intervalo = [[655000000, 670000000]]
    l_v_apartamento.extend(intervalo)

    while m_v_apartamento < 690000000:
        aumento = 10000000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 690000000:
            nuevo_monto = 690000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto

    while m_v_apartamento < 700000000:
        aumento = 5000000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 700000000:
            nuevo_monto = 700000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto

    intervalo = [[700000000, 715000000], [715000000, 725000000],
                    [725000000, 745000000]]
    l_v_apartamento.extend(intervalo)

    while m_v_apartamento < 755000000:
        aumento = 5000000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 755000000:
            nuevo_monto = 755000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto

    intervalo = [[755000000, 775000000]]
    l_v_apartamento.extend(intervalo)

    while m_v_apartamento < 805000000:
        aumento = 10000000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 805000000:
            nuevo_monto = 805000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto 

    intervalo = [[805000000, 825000000],[825000000, 845000000]]
    l_v_apartamento.extend(intervalo)      

    while m_v_apartamento < 855000000:
        aumento = 5000000  
        nuevo_monto = m_v_apartamento + aumento
        if nuevo_monto > 855000000:
            nuevo_monto = 855000000
        l_v_apartamento.append([m_v_apartamento, nuevo_monto])
        m_v_apartamento = nuevo_monto         

    intervalo = [[855000000, 875000000],[875000000, 895000000],
                    [895000000, 905000000],[905000000, 940000000],
                    [940000000, 950000000],[950000000, 970000000],
                    [970000000, 985000000],[985000000, 1000000000]]
    l_v_apartamento.extend(intervalo)

        # ---------------------- CASAS  
    l_v_casas = [[0, 115000000], [115000000, 130000000],
                        [130000000, 145000000]]
        
    m_v_casas = 145000000
        
    while m_v_casas < 245000000:
        aumento = 10000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 245000000:
            nuevo_monto = 245000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
            
    while m_v_casas < 255000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 255000000:
            nuevo_monto = 255000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 

    while m_v_casas < 275000000:
        aumento = 10000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 275000000:
            nuevo_monto = 275000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto  
            
    while m_v_casas < 285000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 285000000:
            nuevo_monto = 285000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
            
    intervalo = [[285000000, 295000000]]
    l_v_casas.extend(intervalo)
            
    while m_v_casas < 305000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 305000000:
            nuevo_monto = 305000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
            
    intervalo = [[305000000, 315000000]]
    l_v_casas.extend(intervalo)     
            
    while m_v_casas < 325000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 325000000:
            nuevo_monto = 325000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
                
    while m_v_casas < 345000000:
        aumento = 10000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 345000000:
            nuevo_monto = 345000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
                    
    while m_v_casas < 355000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 355000000:
            nuevo_monto = 355000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
                            
    while m_v_casas < 375000000:
        aumento = 10000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 375000000:
            nuevo_monto = 375000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
                            
    while m_v_casas < 385000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 385000000:
            nuevo_monto = 385000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
            
    intervalo = [[385000000, 395000000],[395000000, 400000000]]
    l_v_casas.extend(intervalo)
                                
    while m_v_casas < 430000000:
        aumento = 10000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 430000000:
            nuevo_monto = 430000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
                    
    intervalo = [[430000000, 445000000]]
    l_v_casas.extend(intervalo)
            
    while m_v_casas < 455000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 455000000:
            nuevo_monto = 455000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
            
    intervalo = [[455000000, 470000000]]
    l_v_casas.extend(intervalo) 
        
    while m_v_casas < 500000000:
        aumento = 10000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 500000000:
            nuevo_monto = 500000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto
                
    while m_v_casas < 545000000:
        aumento = 15000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 545000000:
            nuevo_monto = 545000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto
                
    while m_v_casas < 555000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 555000000:
            nuevo_monto = 555000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto  
            
    intervalo = [[555000000, 575000000]]
    l_v_casas.extend(intervalo)
        
    while m_v_casas < 595000000:
        aumento = 10000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 595000000:
            nuevo_monto = 595000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto    

    while m_v_casas < 605000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 605000000:
            nuevo_monto = 605000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
            
    while m_v_casas < 645000000:
        aumento = 20000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 645000000:
            nuevo_monto = 645000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto   
            
    while m_v_casas < 655000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 655000000:
            nuevo_monto = 655000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
            
    intervalo = [[655000000, 680000000], [680000000, 695000000],
                    [695000000, 700000000], [700000000, 720000000],
                    [720000000, 745000000]]
    l_v_casas.extend(intervalo)       
            
    while m_v_casas < 755000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 755000000:
            nuevo_monto = 755000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
            
    intervalo = [[755000000, 785000000], [785000000, 800000000], 
                    [800000000, 820000000], [820000000, 845000000]]
    l_v_casas.extend(intervalo)
        
    while m_v_casas < 855000000:
        aumento = 5000000  
        nuevo_monto = m_v_casas + aumento
        if nuevo_monto > 855000000:
            nuevo_monto = 855000000
        l_v_casas.append([m_v_casas, nuevo_monto])
        m_v_casas = nuevo_monto 
            
    intervalo = [[855000000, 890000000], [890000000, 900000000], 
                    [900000000, 925000000], [925000000, 950000000],
                    [950000000, 970000000], [970000000, 990000000], 
                    [990000000, 1000000000]]
    l_v_casas.extend(intervalo)
        
            
        
        ##################################################################################################
        #                                      CREACIÓN DE ENLACES
        ##################################################################################################
    for operacion in operaciones:
        if operacion == 'venta':
            for categoria in categorias:
                if categoria == 'apartamentos':
                    categoria_str = categoria.replace(' ', '-')
                    for intervalo in l_v_apartamento:
                        precio_desde = intervalo[0]
                        precio_hasta = intervalo[1]
                        enlace = f"https://listado.mercadolibre.com.co/inmuebles/{categoria_str}/{operacion}/inmuebles_PriceRange_{precio_desde}-{precio_hasta}_NoIndex_True"
                        enlaces.append(enlace)

                elif categoria == 'casas':
                    categoria_str = categoria.replace(' ', '-')  # Move this line inside the 'casas' block
                    for intervalo in l_v_casas:
                        precio_desde = intervalo[0]
                        precio_hasta = intervalo[1]
                        enlace = f"https://listado.mercadolibre.com.co/inmuebles/{categoria_str}/{operacion}/inmuebles_PriceRange_{precio_desde}-{precio_hasta}_NoIndex_True"
                        enlaces.append(enlace)

    
    for enlace in enlaces:
        df_enlaces = pd.concat([df_enlaces, pd.DataFrame({"Enlace": [enlace]})], ignore_index=True)

    print(f'Enlaces generados: {len(df_enlaces)}')
    return df_enlaces


def regexdata(df):
    enlaces_regex = r'href="([^"]+)"'
    tipo_regex = r'<span class="ui-search-item__group__element ui-search-item__subtitle-grid">([^<]+)</span>'
    publicado_regex = r'<h2[^>]*>([^<]+)</h2>'
    precios_regex = r'<span class="andes-money-amount__fraction" aria-hidden="true">([\d.]+)</span>'
    banos_regex = r'(\d+\s?baño)'
    habs_regex = r'(\d+\s?habita)' 
    areas_regex = r'(\d+\s?m²)'
    ubicacion_regex = r'<span class="ui-search-item__location-label">([^<]+)</span>'
    destacado2_regex = r'<div class="ui-search-item__highlighted-label">([^<]+)</div>'


    lista_enlaces = []
    publicado = []
    prec = []
    baths = []
    habs = []
    area = []
    ubicacion = []
    destacado2 = []
    tipo = []


    for index, row in df.iterrows():
        html_content = row['HTML_Content']
        # Aplicar las expresiones regulares a los fragmentos de HTML
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
    
    

    #Arreglos df
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
