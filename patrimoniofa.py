# Importar libreria requerida
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
import streamlit as st
from src.reportes import reporte1, reporte2, todos, varios
from src.cargar import cargar_datos1, cargar_datos2, cargar_registros, load_data1 
from streamlit_option_menu import option_menu
from typing import List, Tuple

def write():

    url = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/organizaciones_patrimonio.xlsx'
    #df = cargar_datos1()
    df = load_data1(url)
    #df2 = cargar_datos2()

    # Filtros interactivos
    filtro_grupo = st.sidebar.selectbox('Filtrar por Agrupacion Politica', df['nombre_agrupacion_politica'].unique())

    if filtro_grupo== 'Todos':
        df_filtrado = df['nombre_agrupacion_politica'].notna()
    else:
        df_filtrado = df[(df['nombre_agrupacion_politica'] == filtro_grupo) ]

    dataset = df_filtrado

    # Aplicar filtros a los datos
    df_filtrado = df[(df['nombre_agrupacion_politica'] == filtro_grupo) ]
    dataset = df_filtrado

    # Agrupar los datos por tipo
    data_agrupada = df_filtrado.groupby(['tipo', 'codigo', 'nombre']).agg({'valor': 'sum'}).reset_index()

    # Filtrar ingresos y egresos
    ingresos_df = data_agrupada[data_agrupada['tipo'] == 1]
    egresos_df = data_agrupada[data_agrupada['tipo'] == 2]

    # Calcular totales
    total_ingresos = ingresos_df['valor'].sum()
    total_egresos = egresos_df['valor'].sum()
    
    # menu lateral
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Candidatos', 'Organizacion'], 
                               icons=['house', 'people', 'building'], menu_icon="cast", default_index=0)

    if selected == "Home":

            # Mostrar resumen de los datos
            st.subheader('Resumen de Datos Filtrados')
            st.write('Organizacion Politica:', dataset['nombre_agrupacion_politica'].unique()[0])
            st.write('Total Ingresos:', f'{total_ingresos:,.2f}')
            st.write('Total Egresos:', f'{total_egresos:,.2f}')

            # Mostrar tabla de datos filtrados
            st.subheader('Datos Filtrados')

            ## KPIs

            @st.cache_data
            def calculate_kpis(df: pd.DataFrame) -> List[float]:
                    valor_total =(df_filtrado['valor'].sum())
                    Total_valor = f"{valor_total:.2f}M"
                    total_org = df_filtrado['org_id'].nunique()
                    Promedio_org = f"{valor_total / total_org:.2f}K"
                    return [Total_valor, total_org, Promedio_org, total_org]
            

            def display_kpi_metrics(kpis: List[float], kpi_names: List[str]):
                    st.header("KPI Metrics")
                    for i, (col, (kpi_name, kpi_value)) in enumerate(zip(st.columns(4), zip(kpi_names, kpis))):
                        col.metric(label=kpi_name, value=kpi_value)


            kpis = calculate_kpis(df)
            kpi_names = ["Vlr_Total", "Cantidad Organizaciones", "Promedio Org", "Cantidad Org"]
            display_kpi_metrics(kpis, kpi_names)

            st.write("---")
            st.subheader("Top 10 Organizaciones")
            st.write(df_filtrado.head(10))

    elif selected == "Candidatos":

            st.write("## Informes")
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

    elif selected == "Organizacion":
            pdf_path1 = "reporte1.pdf"
            reporte1(dataset,ingresos_df,egresos_df,total_ingresos,total_egresos, pdf_path1)

if __name__ == "__main__":
    write()