# Importar libreria requerida
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
import streamlit as st
from src.reportes import reporte1, reporte2, reporte3, reporte4, reporte1c, reporte4c, todos, varios1, todosc, todosc1, open_pdf
from src.cargar import load_data1, load_data2, load_data3, load_data4, load_data5, load_data6, load_data7 
from streamlit_option_menu import option_menu
from typing import List, Tuple
import seaborn as sns

st.set_page_config(layout="wide")

# CSS personalizado para eliminar márgenes superiores
st.markdown(
    """
    <style>
    /* Quitar el espacio superior del contenedor principal */
    .css-18e3th9 {
        padding-top: 0px;
    }
    /* Subir el logo y ajustarlo al tope */
    .logo {
        margin-top: -70px;  /* Ajustar el logo más cerca del borde superior */
    }
    /* Alinear y subir el título */
    .title {
        margin-top: -60px;
        text-align: left;
        font-size: 2.5em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Cargar el logo y el título alineados
logo_url = "https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/cne.jpg"
st.markdown(f"""
    <div class="logo">
        <img src="{logo_url}" width="200">
    </div>
    """, unsafe_allow_html=True)

# Encabezado principal con markdown
# st.markdown("<h1 style='text-align: center; margin-top: 0px;'>Dashboard de Reportes de Organizaciones Políticas</h1>", unsafe_allow_html=True)

# Encabezado principal
st.title("Dashboard de Reportes de Organizaciones Políticas")
   
@st.cache_data
def load_and_cache_data(url1: str, url2: str, url3: str, url4: str, url5: str, url6: str, url7: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = load_data1(url1)
    df2 = load_data2(url2)
    df3 = load_data3(url3)
    df4 = load_data4(url4)
    df5 = load_data5(url5)
    df6 = load_data6(url6)
    df7 = load_data7(url7)
    return df, df2, df3, df4, df5, df6, df7

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

    url1 = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/organizaciones_patrimonio.xlsx'
    url2 = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/candidatos_consolidado.xlsx'
    url3 = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/descripcionesFun.xlsx'
    url4 = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/gastos_destinados.xlsx'
    url5 = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/descripcionesDes.xlsx'
    url6 = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/ingresos_destinados.xlsx'
    url7 = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/descripcionesDes.xlsx'
    logo = 'https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/cne.jpg'

    df, df2, df3, df4, df5, df6, df7 = load_and_cache_data(url1, url2, url3, url4, url5, url6, url7)
    
    # menu lateral
    with st.sidebar:
            selected = option_menu("Main Menu", 
                                   ["Home", 'Organizacion', 'Candidatos', 'Otros Informes'], 
                                   icons=['house', 'building', 'people', 'file'], 
                                   menu_icon="cast", 
                                   default_index=0)

    if selected == "Home":
                        
            # Unir con el archivo de descripciones
            dataset = df
            df_filtrado = df.merge(df3, on='codigo', how='left')
                                
            # Agrupar los datos por tipo
            data_agrupada = df_filtrado.groupby(['tipo', 'codigo', 'nombre', 'descripcion']).agg({'valor': 'sum'}).reset_index()
            
            # Filtrar ingresos y egresos
            ingresos_df = data_agrupada[data_agrupada['tipo'] == 1]
            egresos_df = data_agrupada[data_agrupada['tipo'] == 2]

            # Calcular totales
            total_ingresos = ingresos_df['valor'].sum()
            total_egresos = egresos_df['valor'].sum()
            
            data_grafica = df_filtrado.groupby(['tipo', 'nombre_agrupacion_politica']).agg({'valor': 'sum'}).reset_index()
            ingresos_grafica = data_grafica[data_grafica['tipo'] == 1]
            egresos_grafica = data_grafica[data_grafica['tipo'] == 2]
            
            # KPI Metrics
            kpis = calculate_kpis(df)
            kpi_names = ["Vlr_Total", "Cantidad Organizaciones", "Promedio Org", "Cantidad Org"]
            display_kpi_metrics(kpis, kpi_names)

            st.subheader("Visualización de Datos")

            # Gráficas en una tabla de 3x3
            st.write("**Gráficos Comparativos (Distribución Ingresos y Egresos)**")
            
            fig1, ax1 = plt.subplots()
            sns.barplot(x="codigo", y="valor", hue="tipo", data=df, ax=ax1)
            ax1.set_ylabel("Valor Total")
            ax1.set_xlabel("Código")
            
            fig2, ax2 = plt.subplots()
            distribucion_tipo = df.groupby('tipo')['valor'].sum()
            ax2.pie(distribucion_tipo, labels=["Ingresos", "Egresos"], autopct='%1.1f%%', colors=['#4CAF50', '#FF5722'])
            
            fig3, ax3 = plt.subplots()
            sns.lineplot(x="codigo", y="valor", hue="tipo", data=df, ax=ax3)
            ax3.set_ylabel("Valor Total")
            ax3.set_xlabel("Código")

            # Disposición 3x3 para gráficas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.pyplot(fig1)
            with col2:
                st.pyplot(fig2)
            with col3:
                st.pyplot(fig3)

            # Más gráficas pueden ir en las siguientes filas
            fig4, ax4 = plt.subplots()
            sns.barplot(x="codigo", y="valor", hue="tipo", data=df, ax=ax4)
            ax4.set_ylabel("Valor Total")
            ax4.set_xlabel("Código")
            
            fig5, ax5 = plt.subplots()
            st.write("**Ingresos por Agrupación Politica**")
            sns.barplot(x="nombre_agrupacion_politica", y="valor", hue="tipo", data=ingresos_grafica, ax=ax5)
            ax5.set_ylabel("Valor Total")
            ax5.set_xlabel("Código")
            # st.write(ingresos_df.head(10))
            
            fig6, ax6 = plt.subplots()
            ax6.pie(distribucion_tipo, labels=["Ingresos", "Egresos"], autopct='%1.1f%%', colors=['#4CAF50', '#FF5722'])

            # Segunda fila de gráficas
            col4, col5, col6 = st.columns(3)
            with col4:
                st.pyplot(fig4)
            with col5:
                st.pyplot(fig5)
            with col6:
                st.pyplot(fig6)
            
            st.write("---")
            st.subheader("Top 10 Organizaciones")
            st.write(ingresos_grafica.head(30))

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
            
            # otra BD gastos destinados
            df_filtradog = df4[df4['nombre_agrupacion_politica'] == filtro_grupo] if filtro_grupo != 'Todos' else df
            
            # Unir con el archivo de descripciones
            datasetg = df_filtradog.merge(df5, on='codigo', how='left')

            # Agrupar los datos por tipo
            data_agrupadag = datasetg.groupby(['tipo', 'codigo', 'descripcion']).agg({'valor': 'sum'}).reset_index()
            #datasetg = data_agrupadag

            # Filtrar ingresos y egresos
            ingresos_dfg = data_agrupadag[data_agrupadag['tipo'] == 1]
            egresos_dfg = data_agrupadag[data_agrupadag['tipo'] == 2]

            # Calcular totales
            total_ingresosg = ingresos_dfg['valor'].sum()
            total_egresosg = egresos_dfg['valor'].sum()
            
            # otra BD ingresos destinados
            df_filtradoi = df6[df6['nombre_agrupacion_politica'] == filtro_grupo] if filtro_grupo != 'Todos' else df
            dataseti = df_filtradoi
            
            # Agrupar los datos por tipo
            #data_agrupadai = dataseti.groupby(['tipo', 'codigo', 'concepto', 'persona', 'cedula', 'telefono', 'direccion', 'acta']).agg({'valor': 'sum'}).reset_index()
            
            
            # Agrupar los datos por tipo
            if not dataseti.empty:
                data_agrupadai = dataseti.groupby(['tipo', 'codigo', 'concepto', 'persona', 'cedula', 'telefono', 'direccion', 'acta']).agg({'valor': 'sum'}).reset_index()
            else:
                data_agrupadai = pd.DataFrame(columns=['tipo', 'codigo', 'concepto', 'persona', 'cedula', 'telefono', 'direccion', 'acta', 'valor'])
            
            # Filtrar ingresos y egresos
            ingresos_dfi = dataseti[dataseti['tipo'] == 1]
            egresos_dfi = dataseti[dataseti['tipo'] == 2]

            # Calcular totales
            #total_ingresosi = ingresos_dfi['valor'].sum()
            #total_egresosi = egresos_dfi['valor'].sum()
            
            # Calcular totales
            total_ingresosi = ingresos_dfi['valor'].sum() if not ingresos_dfi.empty else 0
            total_egresosi = egresos_dfi['valor'].sum() if not egresos_dfi.empty else 0
            

            st.write("## Informes de Organización")
            inputss = st.multiselect("Cuales Informes desea descargar?", ["Todos", "DECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES", "INFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN", "GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011", "CONTRIBUCIONES, DONACIONES Y CREDITOS, EN DINERO O EN ESPECIE, DE SUS AFILIADOS Y/O DE PARTICULARES"])
            st.write(inputss) 
            
            # Si se selecciona "Todos"
            if "Todos" in inputss:
                pdfs = []
                todos(dataset, datasetg, dataseti, ingresos_df, ingresos_dfg, ingresos_dfi, egresos_df, egresos_dfg, egresos_dfi, total_ingresos, total_ingresosg, total_ingresosi, total_egresos, total_egresosg, total_egresosi, logo)
            else:
                # Lista para almacenar las rutas de los PDFs generados
                pdfs = []

                # Generar los informes seleccionados
                if "DECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES" in inputss:
                    informe = inputss
                    pdf_path1 = "reporte1.pdf"
                    reporte1(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path1, logo, informe)
                    st.write(data_agrupada)
                    pdfs.append(pdf_path1)
                    
                if "INFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN" in inputss:
                    informe = inputss
                    pdf_path2 = "reporte2.pdf"
                    reporte2(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path2, logo, informe)
                    st.write(data_agrupada)
                    pdfs.append(pdf_path2)
                
                if "GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011" in inputss:
                    informe = inputss
                    pdf_path3 = "reporte3.pdf"
                    reporte3(datasetg, ingresos_dfg, egresos_dfg, total_ingresosg, total_egresosg, pdf_path3, logo, informe)
                    st.write(df_filtradog)
                    pdfs.append(pdf_path3)

                if "CONTRIBUCIONES, DONACIONES Y CREDITOS, EN DINERO O EN ESPECIE, DE SUS AFILIADOS Y/O DE PARTICULARES" in inputss:
                    informe = inputss
                    pdf_path4 = "reporte4.pdf"
                    reporte4(dataseti, ingresos_dfi, egresos_dfi, total_ingresosi, total_egresosi, pdf_path4, logo, informe)
                    st.write(ingresos_dfi)
                    pdfs.append(pdf_path4)                    

        # Si se seleccionó más de un informe, combinarlos
                if len(pdfs) > 1:
                    varios1(dataset, datasetg, dataseti, ingresos_df, ingresos_dfg, ingresos_dfi, egresos_df, egresos_dfg, egresos_dfi, total_ingresos, total_ingresosg, total_ingresosi, total_egresos, total_egresosg, total_egresosi, logo, pdfs)
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

            data_agrupadac = df_filtradocan.groupby(['tipo', 'codigo', 'nombre', 'descripcion']).agg({'total': 'sum'}).reset_index()

            # Filtrar ingresos y egresos
            ingresos_dfc = data_agrupadac[data_agrupadac['tipo'] == 1]
            egresos_dfc = data_agrupadac[data_agrupadac['tipo'] == 2]

            # Calcular totales
            total_ingresosc = ingresos_dfc['total'].sum()
            total_egresosc = egresos_dfc['total'].sum()
        
            st.write("## Informes Candidatos")
            inputsc = st.multiselect("Cuales Informes desea descargar?", ["Todos", "INFORME INDIVIDUAL DE INGRESOS Y GASTOS DE LA CAMPAÑA"])
            st.write(inputsc) 
            
            # Si se selecciona "Todos"
            if "Todos" in inputsc:
                pdfsc = []
                pdf_path1 = "reporte1c.pdf"
                todosc(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdf_path1, logo)
            else:
                # Lista para almacenar las rutas de los PDFs generados
                pdfsc = []

                # Generar los informes seleccionados
                if "INFORME INDIVIDUAL DE INGRESOS Y GASTOS DE LA CAMPAÑA" in inputsc:
                    informe = inputsc
                    pdf_path1 = "reporte1c.pdf"
                    reporte1c(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdf_path1, logo, informe)
                    pdfsc.append(pdf_path1)

        # Si se seleccionó más de un informe, combinarlos
            if len(pdfsc) > 1:
                todosc1(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdfsc, logo )
            elif len(pdfsc) == 1:
                open_pdf(pdfsc[0])  
            
    elif selected == "Otros Informes":

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

            st.write("## Otros Informes")
            inputss = st.multiselect("Cuales Informes desea descargar?", ["Todos", "DECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES", "INFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN", "GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011"])
            st.write(inputss) 
            
            
            # Si se selecciona "Todos"
            if "Todos" in inputss:
                pdfs = []
                todos(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos)
            else:
                # Lista para almacenar las rutas de los PDFs generados
                pdfs = []

        # Si se seleccionó más de un informe, combinarlos
                if len(pdfs) > 1:
                    varios(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdfs)
                elif len(pdfs) == 1:
                    open_pdf(pdfs[0])        
       

if __name__ == "__main__":
    write()