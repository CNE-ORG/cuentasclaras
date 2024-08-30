import pandas as pd
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
