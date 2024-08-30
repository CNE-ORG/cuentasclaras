import pandas as pd
import os

def cargar_datos1():
    # Función para cargar y filtrar los datos
    files = os.listdir("c:\\archivos")
    os.chdir(r'C:\archivos')
    csv_path = 'organizaciones_patrimonio.xlsx'
    df = pd.read_excel(csv_path)
    return df

def cargar_datos2():
    # Función para cargar y filtrar los datos
    files = os.listdir("c:\\archivos")
    os.chdir(r'C:\archivos')
    csv_path2 = 'organizaciones_patrimonio2.xlsx'
    df2 = pd.read_excel(csv_path2)
    return df2    
    
def cargar_registros():
    # Función para cargar y filtrar los datos
    df3 = ''
    return df3    