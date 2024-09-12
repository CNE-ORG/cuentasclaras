import pandas as pd
import os
import requests
from io import BytesIO


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
    
def load_data1(url):
    # Descargamos el archivo desde la URL
    response = requests.get(url)
    response.raise_for_status()  # Esto lanzará una excepción si la descarga falla

    # Cargamos los datos desde el archivo Excel
    df = pd.read_excel(BytesIO(response.content), engine='openpyxl')
    
    return df
    
def load_data2(url2):
    # Descargamos el archivo desde la URL
    response = requests.get(url2)
    response.raise_for_status()  # Esto lanzará una excepción si la descarga falla

    # Cargamos los datos desde el archivo Excel
    df2 = pd.read_excel(BytesIO(response.content), engine='openpyxl')
    
    return df2

def load_data3(url3):
    # Descargamos el archivo desde la URL
    response = requests.get(url3)
    response.raise_for_status()  # Esto lanzará una excepción si la descarga falla

    # Cargamos los datos desde el archivo Excel
    df3 = pd.read_excel(BytesIO(response.content), engine='openpyxl')
    
    return df3  

def load_data4(url4):
    # Descargamos el archivo desde la URL
    response = requests.get(url4)
    response.raise_for_status()  # Esto lanzará una excepción si la descarga falla

    # Cargamos los datos desde el archivo Excel
    df4 = pd.read_excel(BytesIO(response.content), engine='openpyxl')
    
    return df4


def load_data5(url5):
    # Descargamos el archivo desde la URL
    response = requests.get(url5)
    response.raise_for_status()  # Esto lanzará una excepción si la descarga falla

    # Cargamos los datos desde el archivo Excel
    df5 = pd.read_excel(BytesIO(response.content), engine='openpyxl')
    
    return df5 

def load_data6(url6):
    # Descargamos el archivo desde la URL
    response = requests.get(url6)
    response.raise_for_status()  # Esto lanzará una excepción si la descarga falla

    # Cargamos los datos desde el archivo Excel
    df6 = pd.read_excel(BytesIO(response.content), engine='openpyxl')
    
    return df6

def load_data7(url7):
    # Descargamos el archivo desde la URL
    response = requests.get(url7)
    response.raise_for_status()  # Esto lanzará una excepción si la descarga falla

    # Cargamos los datos desde el archivo Excel
    df7 = pd.read_excel(BytesIO(response.content), engine='openpyxl')
    
    return df7       
