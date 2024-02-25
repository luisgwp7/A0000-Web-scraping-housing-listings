import pandas as pd 
from itertools import product

principal_url_housing = 'https://www.fincaraiz.com.co/apartaestudios-apartamentos-casas'
principal_url_housing_sales = f'{principal_url_housing}/venta'
principal_url_housing_rent = f'{principal_url_housing}/arriendos'

list_stratum = ['1', '2', '3', '4', '5', '6']
list_rooms_baths_parks = ['1', '2', '3', '4%2B']
list_prices_ranges_sales = [[0, 135000000], 
                            [135000000, 300000000], 
                            [300000000, 500000000], 
                            [500000000, 600000000],
                            [600000000, 1000000000],
                            [1000000000, 100000000000]]

list_prices_ranges_rent = [[0, 500000], 
                            [500000, 700000], 
                            [700000, 900000], 
                            [900000, 1200000],
                            [1200000, 1500000],
                            [1500000, 2000000],
                            [2000000, 2500000],
                            [2500000, 3000000],
                            [3000000, 3500000],
                            [3500000, 4000000],
                            [4000000, 4500000],
                            [4500000, 5000000],
                            [5000000, 5500000],
                            [5500000, 6000000],
                            [6000000, 6500000],
                            [6500000, 7000000],
                            [7000000, 7500000],
                            [7500000, 8000000],
                            [8000000, 8500000],
                            [8500000, 9000000],
                            [9000000, 15000000],
                            [15000000, 100000000000]]


def combinateCharacteristicsHousing(list_prices_ranges_operation, operation):
    
    '''
    Uses the combinations between rooms-baths-parkinglots.
    To this add the different prices ranges. 

    '''     

    if operation == 'Sales':
        combinations = list(product(list_stratum, 
                                    list_rooms_baths_parks, 
                                    list_rooms_baths_parks, 
                                    list_rooms_baths_parks, 
                                    list_prices_ranges_operation))
        
    elif operation == 'Rent':
        combinations = list(product(list_stratum, 
                                    list_rooms_baths_parks, 
                                    list_prices_ranges_operation))
    else:
        print('')

    return combinations

def createCombinationsHousingUrls(initial_url, list_prices_ranges_operation, operation):
    '''
    Using all the convinations and the initial url, 
    this just concatenate all the possible combinations 
    and creates the urls to request. 
    '''
    # Generate the combinations 
    combinations = combinateCharacteristicsHousing(list_prices_ranges_operation, operation)
    list_enlaces = []
    
    # Deopending on the operation concatenate the strings and create the diferent... 
    # ... combinations according to the main charachteristics

    if operation == 'Sales':
        for combination in combinations:
            stratum, baths, rooms, parks, price_range = combination
            precio_desde, precio_hasta = price_range
            
            enlace = f'''{initial_url}?pagina=1&usado=true&precioHasta={precio_hasta}&precioDesde={precio_desde}&habitaciones={rooms}&ba%C3%B1os={baths}&parqueaderos={parks}&estrato={stratum}'''
            list_enlaces.append(enlace)

    elif operation == 'Rent':

        for combination in combinations:
            stratum, rooms, price_range = combination
            precio_desde, precio_hasta = price_range
            enlace = f'''{initial_url}?pagina=1&usado=true&precioHasta={precio_hasta}&precioDesde={precio_desde}&habitaciones={rooms}&estrato={stratum}'''
            list_enlaces.append(enlace)
            
    else: 
        print('Check the operation')

    return list_enlaces

def returnUrlHousingtoScrap(operation):

    '''
    Create a df with the list of urls created with
    createCombinationsHousingUrls() function, 
    then returns this df.
    The opration could be: 
    - 'Sales'   or 
    - 'Rent'
    '''
    if operation == 'Sales':
        list_enlaces = createCombinationsHousingUrls(principal_url_housing_sales, list_prices_ranges_sales, operation)

        # Create a list of DataFrames and then concatenate them
        dfs = [pd.DataFrame({"Enlace": [enlace]}) for enlace in list_enlaces]
        df_enlaces = pd.concat(dfs, ignore_index=True)

        # Url's generated 
        enlaces_generados = df_enlaces.shape[0]
        print(f'Usted generó {enlaces_generados} enlaces principales de portada para ventas')

    elif operation == 'Rent':
        list_enlaces = createCombinationsHousingUrls(principal_url_housing_rent, list_prices_ranges_rent, operation)

        # Create a list of DataFrames and then concatenate them
        dfs = [pd.DataFrame({"Enlace": [enlace]}) for enlace in list_enlaces]
        df_enlaces = pd.concat(dfs, ignore_index=True)

        # Url's generated
        enlaces_generados = df_enlaces.shape[0]
        print(f'Usted generó {enlaces_generados} enlaces principales de portada para arriendo')
    else:
        print('The operation has to be "Sales" or "Rent"')
    return df_enlaces