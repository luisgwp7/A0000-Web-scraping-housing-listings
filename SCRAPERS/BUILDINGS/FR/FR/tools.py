
import pandas as pd 
import random
import subprocess


def savedata(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename + '.csv', sep=';', index=False, encoding='utf-16')

def randomtime():
    '''
    This random times are going to used in the scraping
    when the driver closes and opens. Additionally is going 
    to be used with the bottons of the pages 
    '''
    inicio = 1.0
    fin = 3.0
    tiempo = random.uniform(inicio, fin)
    return tiempo


def deltempfiles(ruta_bat):        
    '''
    deltempfiles: helps the user to delete the temporal files. 
    The function uses a .bat file, and execute the file. 
    ''' 
    subprocess.run(ruta_bat, shell=True) 

