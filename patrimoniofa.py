# Importar libreria requerida
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
import streamlit as st
from src.reportes import reporte1, reporte2, reporte3, reporte4, reporte1c, reporte2c, todos, varios, todosc, open_pdf
from src.cargar import load_data1, load_data2, load_data3 
from streamlit_option_menu import option_menu
from typing import List, Tuple


@st.cache_data
def load_and_cache_data(url1: str, url2: str, url3: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = load_data1(url1)
    df2 = load_data2(url2)
    df3 = load_data3(url3)
    return df, df2, df3

def calculate_kpis(df: pd.DataFrame) -> List[float]:
    valor_total = df['valor'].sum()
    total_org = df['org_id'].nunique()
    promedio_org = valor_total / total_org if total_org > 0 else 0
    return [f"{valor_total:.2f}M", total_org, f"{promedio_org:.2f}K", total_org]

def display_kpi_metrics(kpis: List[float], kpi_names: List[str]):
    st.header("KPI Metrics")
    cols = st.columns(4)
    for col, (kpi_name, kpi_value) in zip(cols, zip(kpi_names, kpis)):
        col.metric(label=kpi_name, value=kpi_value)

def write():

    url = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/organizaciones_patrimonio.xlsx'
    url2 = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/candidatos_consolidado.xlsx'
    url3 = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/descripciones.xlsx'

    df, df2, df3 = load_and_cache_data(url, url2, url3)
    
    # menu lateral
    with st.sidebar:
            selected = option_menu("Main Menu", 
                                   ["Home", 'Organizacion', 'Candidatos', 'Otros Informes'], 
                                   icons=['house', 'building', 'people', 'file'], 
                                   menu_icon="cast", 
                                   default_index=0)

    if selected == "Home":
            
            dataset = df
            
            # Unir con el archivo de descripciones
            df_filtrado = df.merge(df3, on='codigo', how='left')
                        
            # Agrupar los datos por tipo
            data_agrupada = df_filtrado.groupby(['tipo', 'codigo', 'nombre', 'descripcion']).agg({'valor': 'sum'}).reset_index()
            
            # Filtrar ingresos y egresos
            ingresos_df = data_agrupada[data_agrupada['tipo'] == 1]
            egresos_df = data_agrupada[data_agrupada['tipo'] == 2]

            # Calcular totales
            total_ingresos = ingresos_df['valor'].sum()
            total_egresos = egresos_df['valor'].sum()
            
            # Mostrar resumen de los datos
            st.subheader('Resumen de Datos Filtrados')
            st.write('Organizacion Politica:', dataset['nombre_agrupacion_politica'].unique()[0])
            st.write('Total Ingresos:', f'{total_ingresos:,.2f}')
            st.write('Total Egresos:', f'{total_egresos:,.2f}')

            # Mostrar tabla de datos filtrados
            st.subheader('Datos Filtrados')

            kpis = calculate_kpis(df_filtrado)
            kpi_names = ["Vlr_Total", "Cantidad Organizaciones", "Promedio Org", "Cantidad Org"]
            display_kpi_metrics(kpis, kpi_names)

            st.write("---")
            st.subheader("Top 10 Organizaciones")
            st.write(df_filtrado.head(10))

    elif selected == "Organizacion":

            # Filtros interactivos
            filtro_grupo = st.sidebar.selectbox('Filtrar por Agrupacion Politica', df['nombre_agrupacion_politica'].unique())
            df_filtrado = df[df['nombre_agrupacion_politica'] == filtro_grupo] if filtro_grupo != 'Todos' else df
            
            # Unir con el archivo de descripciones
            df_filtrado = df_filtrado.merge(df3, on='codigo', how='left')
            dataset = df_filtrado

            # Agrupar los datos por tipo
            data_agrupada = df_filtrado.groupby(['tipo', 'codigo', 'nombre', 'descripcion']).agg({'valor': 'sum'}).reset_index()

            # Filtrar ingresos y egresos
            ingresos_df = data_agrupada[data_agrupada['tipo'] == 1]
            egresos_df = data_agrupada[data_agrupada['tipo'] == 2]

            # Calcular totales
            total_ingresos = ingresos_df['valor'].sum()
            total_egresos = egresos_df['valor'].sum()

            st.write("## Informes de Organización")
            inputss = st.multiselect("Cuales Informes desea descargar?", ["Todos", "DECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES", "INFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN", "GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011"])
            st.write(inputss) 
            
            
            # Si se selecciona "Todos"
            if "Todos" in inputss:
                pdfs = []
                todos(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos)
            else:
                # Lista para almacenar las rutas de los PDFs generados
                pdfs = []

                # Generar los informes seleccionados
                if "DECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES" in inputss:
                    pdf_path1 = "reporte1.pdf"
                    reporte1(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path1)
                    pdfs.append(pdf_path1)
                    
                if "INFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN" in inputss:
                    pdf_path2 = "reporte2.pdf"
                    reporte2(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path2)
                    pdfs.append(pdf_path2)
                    
                if "GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011" in inputss:
                    pdf_path3 = "reporte3.pdf"
                    reporte3(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path3)
                    pdfs.append(pdf_path3)                    

        # Si se seleccionó más de un informe, combinarlos
                if len(pdfs) > 1:
                    varios(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdfs)
                elif len(pdfs) == 1:
                    open_pdf(pdfs[0])

    elif selected == "Candidatos":
            
            
            # Filtros interactivos
            filtro_grupo = st.sidebar.selectbox('Filtrar por Agrupacion Politica', df['nombre_agrupacion_politica'].unique())
            
            # filtrar el candidato
            df_filtradoc = df2[df2['nombre'] == filtro_grupo]
            
            # Unir con el archivo de descripciones
            df_filtradoc = df_filtradoc.merge(df3, on='codigo', how='left')
            
            filtro_corporacion = st.sidebar.selectbox('Filtrar por Corporación', df_filtradoc['nombre_corporacion'].unique())
            df_filtradocor = df_filtradoc[df_filtradoc['nombre_corporacion'] == filtro_corporacion]
            
            filtro_candidato = st.sidebar.selectbox('Filtrar por Candidato', df_filtradocor['nombre_completo'].unique())
            df_filtradocan = df_filtradocor[df_filtradocor['nombre_completo'] == filtro_candidato]
            datasetc = df_filtradocan

            data_agrupadac = df_filtradocan.groupby(['tipo', 'codigo', 'nombre', 'descripcion']).agg({'valor': 'sum'}).reset_index()

            # Filtrar ingresos y egresos
            ingresos_dfc = data_agrupadac[data_agrupadac['tipo'] == 1]
            egresos_dfc = data_agrupadac[data_agrupadac['tipo'] == 2]

            # Calcular totales
            total_ingresosc = ingresos_dfc['valor'].sum()
            total_egresosc = egresos_dfc['valor'].sum()
        
            st.write("## Informes Candidatos")
            inputsc = st.multiselect("Cuales Informes desea descargar?", ["Todos", "INFORME INDIVIDUAL DE INGRESOS Y GASTOS DE LA CAMPAÑA", "Otros"])
            st.write(inputsc) 
            
            # Si se selecciona "Todos"
            if "Todos" in inputsc:
                pdfs = []
                todosc(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc)
            else:
                # Lista para almacenar las rutas de los PDFs generados
                pdfs = []

                # Generar los informes seleccionados
                if "INFORME INDIVIDUAL DE INGRESOS Y GASTOS DE LA CAMPAÑA" in inputsc:
                    pdf_path1 = "reporte1c.pdf"
                    reporte1c(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc, pdf_path1)
                    pdfs.append(pdf_path1)
                   
                if "Otros" in inputsc:
                    pdf_path3 = "reporte2c.pdf"
                    reporte2c(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc, pdf_path3)
                    pdfs.append(pdf_path3)                    

        # Si se seleccionó más de un informe, combinarlos
            if len(pdfs) >= 1:
                varios(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdfs)
            
            
    elif selected == "Otros Informes":
        
            filtro_grupo = st.sidebar.selectbox('Filtrar por Agrupacion Politica', df['nombre_agrupacion_politica'].unique())       
            df_filtradoc = df2[df2['nombre'] == filtro_grupo]
            
            # Unir con el archivo de descripciones
            df_filtradoc = df_filtradoc.merge(df3, on='codigo', how='left')
            
            datasetc = df_filtradoc
            filtro_candidato = st.sidebar.selectbox('Filtrar por Candidato', df_filtradoc['nombre_completo'].unique())
            df_filtradoc = df_filtradoc[df_filtradoc['nombre_completo'] == filtro_candidato]

            data_agrupadac = df_filtradoc.groupby(['tipo', 'codigo', 'nombre', 'descripcion']).agg({'valor': 'sum'}).reset_index()

            # Filtrar ingresos y egresos
            ingresos_dfc = data_agrupadac[data_agrupadac['tipo'] == 1]
            egresos_dfc = data_agrupadac[data_agrupadac['tipo'] == 2]

            # Calcular totales
            total_ingresosc = ingresos_dfc['valor'].sum()
            total_egresosc = egresos_dfc['valor'].sum()
        
            pdf_path1 = "reporte4.pdf"
            reporte4(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc, pdf_path1)            

if __name__ == "__main__":
    write()