
import pandas as pd 
import random
import subprocess

# Master directory
def master_dir():
    return f'C:/Users/luisG/GIT/SCRAPING/RESULTS/BUILDINGS'

def savedata(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename + '.csv', sep=';', index=False, encoding='utf-16')

def randomtime():
    #Tiempos
    inicio = 1.0
    fin = 3.0
    tiempo = random.uniform(inicio, fin)
    return tiempo



def deltempfiles(ruta_bat): 
    '''
    deltempfiles: helps the user to delete the temporal files. 
    The function uses a .bat file, and execute the file. 
    '''
    # Ejecutar el archivo .bat sin capturar la salida
    subprocess.run(ruta_bat, shell=True) 

