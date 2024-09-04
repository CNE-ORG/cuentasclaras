import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
from fpdf import FPDF
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfMerger
import os
import subprocess
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.graphics.shapes import Line
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing


def reporte1(dataset,ingresos_df,egresos_df,total_ingresos,total_egresos, pdf_path):
    
    # Variables del encabezado
    total_patrimonio_bruto = dataset['total_patrimonio'].unique()[0]
    total_patrimonio_liquido = dataset['patrimonio_liquido'].unique()[0]
    nit = dataset['nit'].unique()[0]
    representante_legal = dataset['representante_legal'].unique()[0]
    organizacion_politica = dataset['nombre_agrupacion_politica'].unique()[0]
    codigo1 = dataset['codigo'].unique()[0]
    tipo1 = dataset['tipo'].unique()[0]
    documento_representante = dataset['documento_representante'].unique()[0]
    deudas = dataset['deudas'].unique()[0]
    total_patrimonio_neto = total_patrimonio_bruto - deudas

    # Configuración de la visualización
    fig = plt.figure(figsize=(10, 12))
    gs = GridSpec(5, 1, height_ratios=[0.8, 1, 2, 3, 4])

    # Títulos del reporte
    fig.suptitle("ORGANIZACIÓN ELECTORAL\nCONSEJO NACIONAL ELECTORAL\nFondo Nacional De Financiación Política\nDECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES", fontsize=14, fontweight='bold', ha='center')

    # Filtro título
    ax_filtro = fig.add_subplot(gs[0])
    ax_filtro.axis('off')
    ax_filtro.text(0.5, 0.7, f"Nombre Agrupación Política: {organizacion_politica}\n", ha='center', fontsize=12)
    ax_filtro.text(0.5, 0.5, f"NIT: {nit}", ha='center', fontsize=12)

    # encabezado con marco y firmas
    ax3 = fig.add_subplot(gs[1])
    ax3.axis('off')

    # Crear marco para el encabezado 1
    rect0 = mpatches.Rectangle((0, 0), 1.1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax3.transAxes, clip_on=False)
    ax3.add_patch(rect0)

    # Texto del encabezado 1
    ax3.text(0.1, 0.35, f"Representante Legal: {representante_legal}", ha='center', fontsize=10)
    ax3.text(0.8, 0.35, f"Cedula de Ciudadania: {documento_representante}", ha='center', fontsize=10)

    # Encabezado con consecutivo, patrimonio, representante legal y deudas
    ax0 = fig.add_subplot(gs[2])
    ax0.axis('tight')
    ax0.axis('off')

    # Datos de encabezado 2

    encabezado_data = [
        ["1", "Total Patrimonio Bruto a 31 de diciembre (Según Balance general)", f'{total_patrimonio_bruto:,.0f}'],
        ["2", "Deudas a 31 de diciembre (Según Balance general)", f'{deudas:,.0f}'],
        ["3", "Total patrimonio liquido a 31 de diciembre", f'{total_patrimonio_liquido:,.0f}']
    ]

    ax0.table(cellText=encabezado_data, colWidths=[0.1, 1, 0.2], cellLoc='center', loc='center')

    # Tabla detallada de ingresos y egresos
    ax1 = fig.add_subplot(gs[3])
    ax1.axis('tight')
    ax1.axis('off')

    # Preparar tabla de ingresos y egresos
    # Formatear los valores de la columna 'valor' con separadores de miles y 2 decimales
    ingresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in ingresos_df[['codigo', 'nombre', 'valor']].values]
    egresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in egresos_df[['codigo', 'nombre', 'valor']].values]


    # Crear la tabla completa con los valores formateados
    table_data = ingresos_data + \
                [["", "Total Ingresos Anuales", f'{total_ingresos:,.2f}']] + \
                egresos_data + \
                [["", "Total Egresos Anuales", f'{total_egresos:,.2f}']]

    # Definir la tabla con justificación centrada y tamaño de letra
    tabla = ax1.table(cellText=table_data, 
                    colLabels=["CODIGO", "CONCEPTO", "VALOR"], 
                    cellLoc='center',  # Justificación centrada por defecto
                    loc='center',
                    colWidths=[0.1, 1, 0.2],  # Ajustar el ancho de las columnas
                    fontsize=16)  # Tamaño inicial de la letra


    for key, cell in tabla.get_celld().items():
        if key[1] == 0 or key[1] == 1:  # Columnas 'Código' y 'Nombre'
            cell.set_text_props(ha='left')  # Alinear a la izquierda
        if key[1] == 2 :  # Columna valor
            cell.set_text_props(ha='right')  # Alinear a la izquierda        
        cell.set_fontsize(31)  # Aumentar el tamaño de la letra en todas las celdas


    # Pie de página con marco y firmas
    ax2 = fig.add_subplot(gs[4])
    ax2.axis('off')

    # Crear marco para el pie de página
    rect = mpatches.Rectangle((0, 0), 1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax2.transAxes, clip_on=False)
    ax2.add_patch(rect)

    # Texto del pie de página
    ax2.text(0.5, 0.35, "Las cifras se expresan en pesos colombianos", ha='center', fontsize=10)
    ax2.text(0.2, 0.1, "Firma del Representante Legal", ha='center', fontsize=10)
    ax2.text(0.8, 0.1, "Firma del Auditor", ha='center', fontsize=10)

    # Ajustar el layout
    st.pyplot(fig) 

    # Guardar la figura en un PDF temporal
    with PdfPages(pdf_path) as pdf:
            pdf.savefig(fig)
    plt.close(fig)  # Cerrar la figura para liberar memoria    

    
def reporte2(dataset,ingresos_df,egresos_df,total_ingresos,total_egresos, pdf_path):  
    
    
    # Variables del encabezado
    total_patrimonio_bruto = dataset['total_patrimonio'].unique()[0]
    total_patrimonio_liquido = dataset['patrimonio_liquido'].unique()[0]
    nit = dataset['nit'].unique()[0]
    representante_legal = dataset['representante_legal'].unique()[0]
    organizacion_politica = dataset['nombre_agrupacion_politica'].unique()[0]
    codigo1 = dataset['codigo'].unique()[0]
    tipo1 = dataset['tipo'].unique()[0]
    documento_representante = dataset['documento_representante'].unique()[0]
    deudas = dataset['deudas'].unique()[0]
    total_patrimonio_neto = total_patrimonio_bruto - deudas

    # Configuración de la visualización
    fig = plt.figure(figsize=(10, 12))
    gs = GridSpec(5, 1, height_ratios=[0.8, 1, 2, 3, 4])

    # Títulos del reporte
    fig.suptitle("ORGANIZACIÓN ELECTORAL\nCONSEJO NACIONAL ELECTORAL\nFondo Nacional De Financiación Política\nINFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN", fontsize=14, fontweight='bold', ha='center')

    # Filtro título
    ax_filtro = fig.add_subplot(gs[0])
    ax_filtro.axis('off')
    ax_filtro.text(0.5, 0.7, f"Nombre Agrupación Política: {organizacion_politica}\n", ha='center', fontsize=12)
    ax_filtro.text(0.5, 0.5, f"NIT: {nit}", ha='center', fontsize=12)

    # encabezado con marco y firmas
    ax3 = fig.add_subplot(gs[1])
    ax3.axis('off')

    # Crear marco para el encabezado 1
    rect0 = mpatches.Rectangle((0, 0), 1.1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax3.transAxes, clip_on=False)
    ax3.add_patch(rect0)

    # Texto del encabezado 1
    ax3.text(0.1, 0.35, f"Representante Legal: {representante_legal}", ha='center', fontsize=10)
    ax3.text(0.8, 0.35, f"Cedula de Ciudadania: {documento_representante}", ha='center', fontsize=10)

    # Encabezado con consecutivo, patrimonio, representante legal y deudas
    ax0 = fig.add_subplot(gs[2])
    ax0.axis('tight')
    ax0.axis('off')

    # Datos de encabezado 2

    encabezado_data = [
        ["1", "Total Patrimonio Bruto a 31 de diciembre (Según Balance general)", f'{total_patrimonio_bruto:,.0f}'],
        ["2", "Deudas a 31 de diciembre (Según Balance general)", f'{deudas:,.0f}'],
        ["3", "Total patrimonio liquido a 31 de diciembre", f'{total_patrimonio_liquido:,.0f}']
    ]

    ax0.table(cellText=encabezado_data, colWidths=[0.1, 1, 0.2], cellLoc='center', loc='center')

    # Tabla detallada de ingresos y egresos
    ax1 = fig.add_subplot(gs[3])
    ax1.axis('tight')
    ax1.axis('off')

    # Preparar tabla de ingresos y egresos
    # Formatear los valores de la columna 'valor' con separadores de miles y 2 decimales
    
    ingresos_data_filtro = ingresos_df[ingresos_df['codigo'] == 1]
    egresos_data_filtro = egresos_df[egresos_df['codigo'] == 2]
    
    ingresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in  ingresos_data_filtro[['codigo', 'nombre', 'valor']].values]
    egresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in egresos_data_filtro[['codigo', 'nombre', 'valor']].values]


    # Crear la tabla completa con los valores formateados
    table_data = ingresos_data + \
                [["", "", ""]] + \
                egresos_data + \
                [["", "", ""]]

    # Definir la tabla con justificación centrada y tamaño de letra
    tabla = ax1.table(cellText=table_data, 
                    colLabels=["CODIGO", "CONCEPTO", "VALOR"], 
                    cellLoc='center',  # Justificación centrada por defecto
                    loc='center',
                    colWidths=[0.1, 1, 0.2],  # Ajustar el ancho de las columnas
                    fontsize=16)  # Tamaño inicial de la letra


    for key, cell in tabla.get_celld().items():
        if key[1] == 0 or key[1] == 1:  # Columnas 'Código' y 'Nombre'
            cell.set_text_props(ha='left')  # Alinear a la izquierda
        if key[1] == 2 :  # Columna valor
            cell.set_text_props(ha='right')  # Alinear a la izquierda        
        cell.set_fontsize(31)  # Aumentar el tamaño de la letra en todas las celdas


    # Pie de página con marco y firmas
    ax2 = fig.add_subplot(gs[4])
    ax2.axis('off')

    # Crear marco para el pie de página
    rect = mpatches.Rectangle((0, 0), 1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax2.transAxes, clip_on=False)
    ax2.add_patch(rect)

    # Texto del pie de página
    ax2.text(0.5, 0.35, "Las cifras registradas en este formulario fueron tomadas fielmente del libro de Ingresos y Gastos.", ha='center', fontsize=10)
    ax2.text(0.2, 0.1, "Firma del Representante Legal", ha='center', fontsize=10)
    ax2.text(0.8, 0.1, "Firma del Auditor", ha='center', fontsize=10)
    ax2.text(0.5, 0.35, "NOTA: Para reportar los gastos en las casillas corespondientes, tener en cuenta el Articulo 11 ......", ha='center', fontsize=10)
##   ax2.text(0.5, 0.35, "NOTA: Para reportar los gastos en las casillas corespondientes, tener en cuenta el Articulo 11 de la Resolucion 3134 del 14 de diciembre de 2018 'De conformidad con el principio de la transparencia, al tenor de lo previsto en el articulo 19 de la Ley 1475 de 2011, los partidos o movimientos politicos con personeria juridica declarados en oposicion, al momento de hacer la rendicion publica de cuentas, deberan desagregar del total de los ingresos y gastos, el monto correspondiente al componente de la financiacion adicional, por lo que deberan discriminar el destino dado a estos recursos...' y conforme con los principios.", ha='center', fontsize=10)

    # Ajustar el layout
    st.pyplot(fig)  
    
    # Guardar la figura en un PDF temporal
    with PdfPages(pdf_path) as pdf:
        pdf.savefig(fig)
    plt.close(fig)  # Cerrar la figura para liberar memoria

def reporte3(dataset,ingresos_df,egresos_df,total_ingresos,total_egresos, pdf_path):  
    
    
    # Variables del encabezado
    total_patrimonio_bruto = dataset['total_patrimonio'].unique()[0]
    total_patrimonio_liquido = dataset['patrimonio_liquido'].unique()[0]
    nit = dataset['nit'].unique()[0]
    representante_legal = dataset['representante_legal'].unique()[0]
    organizacion_politica = dataset['nombre_agrupacion_politica'].unique()[0]
    codigo1 = dataset['codigo'].unique()[0]
    tipo1 = dataset['tipo'].unique()[0]
    documento_representante = dataset['documento_representante'].unique()[0]
    deudas = dataset['deudas'].unique()[0]
    total_patrimonio_neto = total_patrimonio_bruto - deudas

    # Configuración de la visualización
    fig = plt.figure(figsize=(10, 12))
    gs = GridSpec(5, 1, height_ratios=[0.8, 1, 2, 3, 4])

    # Títulos del reporte
    fig.suptitle("ORGANIZACIÓN ELECTORAL\nCONSEJO NACIONAL ELECTORAL\nFondo Nacional De Financiación Política\nGASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011", fontsize=14, fontweight='bold', ha='center')

    # Filtro título
    ax_filtro = fig.add_subplot(gs[0])
    ax_filtro.axis('off')
    ax_filtro.text(0.5, 0.7, f"Nombre Agrupación Política: {organizacion_politica}\n", ha='center', fontsize=12)
    ax_filtro.text(0.5, 0.5, f"NIT: {nit}", ha='center', fontsize=12)

    # encabezado con marco y firmas
    ax3 = fig.add_subplot(gs[1])
    ax3.axis('off')

    # Crear marco para el encabezado 1
    rect0 = mpatches.Rectangle((0, 0), 1.1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax3.transAxes, clip_on=False)
    ax3.add_patch(rect0)

    # Texto del encabezado 1
    ax3.text(0.1, 0.35, f"Representante Legal: {representante_legal}", ha='center', fontsize=10)
    ax3.text(0.8, 0.35, f"Cedula de Ciudadania: {documento_representante}", ha='center', fontsize=10)

    # Encabezado con consecutivo, patrimonio, representante legal y deudas
    ax0 = fig.add_subplot(gs[2])
    ax0.axis('tight')
    ax0.axis('off')

    # Datos de encabezado 2

    encabezado_data = [
        ["1", "Total Patrimonio Bruto a 31 de diciembre (Según Balance general)", f'{total_patrimonio_bruto:,.0f}'],
        ["2", "Deudas a 31 de diciembre (Según Balance general)", f'{deudas:,.0f}'],
        ["3", "Total patrimonio liquido a 31 de diciembre", f'{total_patrimonio_liquido:,.0f}']
    ]

    ax0.table(cellText=encabezado_data, colWidths=[0.1, 1, 0.2], cellLoc='center', loc='center')

    # Tabla detallada de ingresos y egresos
    ax1 = fig.add_subplot(gs[3])
    ax1.axis('tight')
    ax1.axis('off')

    # Preparar tabla de ingresos y egresos
    # Formatear los valores de la columna 'valor' con separadores de miles y 2 decimales
    ingresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in ingresos_df[['codigo', 'nombre', 'valor']].values]
    egresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in egresos_df[['codigo', 'nombre', 'valor']].values]


    # Crear la tabla completa con los valores formateados
    table_data = ingresos_data + \
                [["", "Total Ingresos Anuales", f'{total_ingresos:,.2f}']] + \
                egresos_data + \
                [["", "Total Egresos Anuales", f'{total_egresos:,.2f}']]

    # Definir la tabla con justificación centrada y tamaño de letra
    tabla = ax1.table(cellText=table_data, 
                    colLabels=["CODIGO", "CONCEPTO", "VALOR"], 
                    cellLoc='center',  # Justificación centrada por defecto
                    loc='center',
                    colWidths=[0.1, 1, 0.2],  # Ajustar el ancho de las columnas
                    fontsize=16)  # Tamaño inicial de la letra


    for key, cell in tabla.get_celld().items():
        if key[1] == 0 or key[1] == 1:  # Columnas 'Código' y 'Nombre'
            cell.set_text_props(ha='left')  # Alinear a la izquierda
        if key[1] == 2 :  # Columna valor
            cell.set_text_props(ha='right')  # Alinear a la izquierda        
        cell.set_fontsize(31)  # Aumentar el tamaño de la letra en todas las celdas


    # Pie de página con marco y firmas
    ax2 = fig.add_subplot(gs[4])
    ax2.axis('off')

    # Crear marco para el pie de página
    rect = mpatches.Rectangle((0, 0), 1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax2.transAxes, clip_on=False)
    ax2.add_patch(rect)

    # Texto del pie de página
    ax2.text(0.5, 0.35, "Las cifras se expresan en pesos colombianos", ha='center', fontsize=10)
    ax2.text(0.2, 0.1, "Firma del Representante Legal", ha='center', fontsize=10)
    ax2.text(0.8, 0.1, "Firma del Auditor", ha='center', fontsize=10)

    # Ajustar el layout
    st.pyplot(fig)  
    
    # Guardar la figura en un PDF temporal
    with PdfPages(pdf_path) as pdf:
        pdf.savefig(fig)
    plt.close(fig)  # Cerrar la figura para liberar memoria

def reporte4(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc, pdf_path):
    
    # Variables del encabezado
    organizacion_politica = datasetc['nombre'].unique()[0]
    nombre_completo = datasetc['nombre_completo'].unique()[0]
    numero_documento = datasetc['numero_documento'].unique()[0]

    # Configuración de la visualización
    fig = plt.figure(figsize=(10, 12))
    gs = GridSpec(5, 1, height_ratios=[0.8, 1, 2, 3, 4])

    # Títulos del reporte
    fig.suptitle("ORGANIZACIÓN ELECTORAL\nCONSEJO NACIONAL ELECTORAL\nFondo Nacional De Financiación Política\nINFORME INDIVIDUAL DE INGRESOS Y GASTOS DE LA CAMPAÑA", fontsize=14, fontweight='bold', ha='center')

    # Filtro título
    ax_filtro = fig.add_subplot(gs[0])
    ax_filtro.axis('off')
    ax_filtro.text(0.5, 0.7, f"Nombre Agrupación Política: {organizacion_politica}\n", ha='center', fontsize=12)
 #   ax_filtro.text(0.5, 0.5, f"NIT: {nit}", ha='center', fontsize=12)

    # encabezado con marco y firmas
    ax3 = fig.add_subplot(gs[1])
    ax3.axis('off')

    # Crear marco para el encabezado 1
    rect0 = mpatches.Rectangle((0, 0), 1.1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax3.transAxes, clip_on=False)
    ax3.add_patch(rect0)

    # Texto del encabezado 1
    ax3.text(0.1, 0.35, f"Candidato: {nombre_completo}", ha='center', fontsize=10)
    ax3.text(0.8, 0.35, f"Cedula de Ciudadania: {numero_documento}", ha='center', fontsize=10)

    # Encabezado con consecutivo, patrimonio, representante legal y deudas
    ax0 = fig.add_subplot(gs[2])
    ax0.axis('tight')
    ax0.axis('off')

    # Datos de encabezado 2

    encabezado_data = [
        ["1", "Total Ingresos a 31 de diciembre (Según Balance general)", f'{total_ingresosc:,.0f}'],
        ["2", "Total Gastos  a 31 de diciembre", f'{total_egresosc:,.0f}']
    ]

    ax0.table(cellText=encabezado_data, colWidths=[0.1, 1, 0.2], cellLoc='center', loc='center')

    # Tabla detallada de ingresos y egresos
    ax1 = fig.add_subplot(gs[3])
    ax1.axis('tight')
    ax1.axis('off')

    # Preparar tabla de ingresos y egresos
    # Formatear los valores de la columna 'valor' con separadores de miles y 2 decimales
    ingresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in ingresos_dfc[['codigo', 'descripcion', 'valor']].values]
    egresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in egresos_dfc[['codigo', 'descripcion', 'valor']].values]


    # Crear la tabla completa con los valores formateados
    table_data = ingresos_data + \
                [["", "Total Ingresos Anuales", f'{total_ingresosc:,.2f}']] + \
                egresos_data + \
                [["", "Total Egresos Anuales", f'{total_egresosc:,.2f}']]

    # Definir la tabla con justificación centrada y tamaño de letra
    tabla = ax1.table(cellText=table_data, 
                    colLabels=["CODIGO", "CONCEPTO", "VALOR"], 
                    cellLoc='center',  # Justificación centrada por defecto
                    loc='center',
                    colWidths=[0.1, 1, 0.2],  # Ajustar el ancho de las columnas
                    fontsize=16)  # Tamaño inicial de la letra


    for key, cell in tabla.get_celld().items():
        if key[1] == 0 or key[1] == 1:  # Columnas 'Código' y 'Nombre'
            cell.set_text_props(ha='left')  # Alinear a la izquierda
        if key[1] == 2 :  # Columna valor
            cell.set_text_props(ha='right')  # Alinear a la izquierda        
        cell.set_fontsize(31)  # Aumentar el tamaño de la letra en todas las celdas


    # Pie de página con marco y firmas
    ax2 = fig.add_subplot(gs[4])
    ax2.axis('off')

    # Crear marco para el pie de página
    rect = mpatches.Rectangle((0, 0), 1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax2.transAxes, clip_on=False)
    ax2.add_patch(rect)

    # Texto del pie de página
    ax2.text(0.5, 0.35, "Las cifras registradas en este formulario fueron tomadas fielmente del libro de Ingresos y Gastos.", ha='center', fontsize=10)
    ax2.text(0.2, 0.1, "Firma del Candidato", ha='center', fontsize=10)
    ax2.text(0.8, 0.1, "Firma del Auditor", ha='center', fontsize=10)

    # Ajustar el layout
    st.pyplot(fig) 

    # Guardar la figura en un PDF temporal
    with PdfPages(pdf_path) as pdf:
            pdf.savefig(fig)
    plt.close(fig)  # Cerrar la figura para liberar memoria 

def reporte5(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path, logo_path, informe):
    # Variables del encabezado
    total_patrimonio_bruto = dataset['total_patrimonio'].unique()[0]
    total_patrimonio_liquido = dataset['patrimonio_liquido'].unique()[0]
    nit = dataset['nit'].unique()[0]
    representante_legal = dataset['representante_legal'].unique()[0]
    organizacion_politica = dataset['nombre_agrupacion_politica'].unique()[0]
    documento_representante = dataset['documento_representante'].unique()[0]
    deudas = dataset['deudas'].unique()[0]
    
    total_patrimonio_neto = total_patrimonio_bruto - deudas
    
    # Crear PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    # Logo
    logo = Image(logo_path, width=2*inch, height=2*inch)
    elements.append(logo)
    
    # Encabezado
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    
    title = Paragraph(
        """<b>ORGANIZACIÓN ELECTORAL</b><br/>
        CONSEJO NACIONAL ELECTORAL<br/>
        Fondo Nacional De Financiación Política<br/>
        GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011""",
        styles["Title"]
    )
    elements.append(title)
    
    # Titulo del informe
    titulo_info = f"""
    <b>Informe :</b> {informe}<br/>
    """
    elements.append(Paragraph(titulo_info, styles["Normal"]))
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 12))
    
    encabezado_info = f"""
    <b>Nombre Agrupación Política:</b> {organizacion_politica}<br/>
    <b>NIT:</b> {nit}<br/>
    <b>Representante Legal:</b> {representante_legal} ({documento_representante})<br/>
    """
    
    elements.append(Paragraph(encabezado_info, styles["Normal"]))
    
    # Tabla de resumen
    data = [
        ["1", "Total Patrimonio Bruto a 31 de diciembre", f'{total_patrimonio_bruto:,.0f}'],
        ["2", "Deudas a 31 de diciembre", f'{deudas:,.0f}'],
        ["3", "Total Patrimonio Líquido a 31 de diciembre", f'{total_patrimonio_liquido:,.0f}'],
    ]
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    
    # Tabla detallada de ingresos y egresos
    ingresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in ingresos_df[['codigo', 'nombre', 'valor']].values]
    egresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in egresos_df[['codigo', 'nombre', 'valor']].values]
    
    table_data = ingresos_data + \
                [["", "Total Ingresos Anuales", f'{total_ingresos:,.2f}']] + \
                egresos_data + \
                [["", "Total Egresos Anuales", f'{total_egresos:,.2f}']]
    
    tabla = Table(table_data)
    tabla.setStyle(TableStyle([
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    
    elements.append(tabla)
    
    # Pie de página
    pie_de_pagina = f"""
    <b>Las cifras se expresan en pesos colombianos.</b><br/>
    Firma del Representante Legal_________________________<br/>
    Firma del Auditor_________________________<br/>
    """
    
    elements.append(Paragraph(pie_de_pagina, styles["Justify"]))
    
    # Generar PDF
    doc.build(elements)    

def reporte1c(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdf_path, logo_path):
    
    # Variables del encabezado
    organizacion_politica = datasetc['nombre'].unique()[0]
    nombre_completo = datasetc['nombre_completo'].unique()[0]
    numero_documento = datasetc['numero_documento'].unique()[0]
    nit = datasetc['tipo_organizacion'].unique()[0]

    # Crear PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=32, leftMargin=52, topMargin=32, bottomMargin=52)
    elements = []
    
    # Configuración de estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    
    # Logo y título
    logo = Image(logo_path, width=1*inch, height=1*inch)
    title = Paragraph(
        """<b>ORGANIZACIÓN ELECTORAL</b><br/>
        <b>CONSEJO NACIONAL ELECTORAL</b><br/>
        Fondo Nacional De Financiación Política<br/>""",
        styles["Title"]
    )
    
    # Crear una tabla para organizar el logo y el título en la misma línea
    title_logo_table = Table([[title, logo]], colWidths=[7.0 * inch, 1 * inch])
    title_logo_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (1, 0), 'TOP'),
    ]))
    elements.append(title_logo_table)
    
    # Espacio entre título y contenido
    elements.append(Spacer(1, 12))
    

    # Títulos del reporte
    #fig.suptitle("ORGANIZACIÓN ELECTORAL\nCONSEJO NACIONAL ELECTORAL\nFondo Nacional De Financiación Política\nINFORME INDIVIDUAL DE INGRESOS Y GASTOS DE LA CAMPAÑA", fontsize=14, fontweight='bold', ha='center')


    # Encabezado de la organización política
    encabezado_info = f"""
    <b>Nombre Candidato:</b> {nombre_completo}<br/>
    <b>Cedula de Ciudadania:</b> {numero_documento}<br/>
    <b>Nombre Agrupación Política:</b> {organizacion_politica} ({nit})<br/>
    """
    elements.append(Paragraph(encabezado_info, styles["Normal"]))
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 12))

    # Títulos de las tablas
    encabezado_tabla = [['CODIGO', 'CONCEPTO', 'VALOR']]
    
    # Tabla de resumen financiero
    data_resumen = [
        ["1", "Total Ingresos a 31 de diciembre (Según Balance general)", f'{total_ingresosc:,.0f}'],
        ["2", "Total Gastos  a 31 de diciembre", f'{total_egresosc:,.0f}'],
    ]
    tabla_resumen = Table(encabezado_tabla + data_resumen, colWidths=[0.5*inch, 6*inch, 1*inch])
    tabla_resumen.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabla_resumen)
    
    # Espacio antes de las tablas detalladas
    elements.append(Spacer(1, 12))


    # Tablas detalladas de ingresos y egresos
    ingresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in ingresos_dfc[['codigo', 'descripcion', 'valor']].values]
    egresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in egresos_dfc[['codigo', 'descripcion', 'valor']].values]
    
    # Añadir totales
    ingresos_data.append(["", "Total Ingresos Anuales", f'{total_ingresosc:,.2f}'])
    egresos_data.append(["", "Total Egresos Anuales", f'{total_egresosc:,.2f}'])
    
    # Crear tabla de ingresos y egresos
    tabla_ingresos_egresos = Table(encabezado_tabla + ingresos_data + egresos_data, colWidths=[0.5*inch, 6*inch, 1*inch])
    tabla_ingresos_egresos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    elements.append(tabla_ingresos_egresos)

   # Pie de página
    pie_de_pagina = Paragraph(
        """<b>Las cifras registradas en este formulario fueron tomadas fielmente del libro de Ingresos y Gastos.</b><br/>
        Firma del Candidato_________________________<br/>
        Firma del Auditor_________________________<br/>""",
        styles["Justify"]
    )
   # elements.append(Spacer(1, 36))
   # elements.append(pie_de_pagina)
    
    # Añadir una línea horizontal utilizando Drawing
    line = Drawing(500, 10)
    line.add(Line(0, 0, 450, 0))
    
    # Añadir las líneas y el pie de página
    elements.append(line)
    elements.append(Spacer(1, 6))
    elements.append(pie_de_pagina)
    elements.append(Spacer(1, 6))
    elements.append(line)
    
    # Generar PDF
    doc.build(elements)      


def reporte6(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path, logo_path, informe):
    # Variables del encabezado
    total_patrimonio_bruto = dataset['total_patrimonio'].unique()[0]
    total_patrimonio_liquido = dataset['patrimonio_liquido'].unique()[0]
    nit = dataset['nit'].unique()[0]
    representante_legal = dataset['representante_legal'].unique()[0]
    organizacion_politica = dataset['nombre_agrupacion_politica'].unique()[0]
    documento_representante = dataset['documento_representante'].unique()[0]
    deudas = dataset['deudas'].unique()[0]
    
    total_patrimonio_neto = total_patrimonio_bruto - deudas
    
    # Crear PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=32, leftMargin=52, topMargin=32, bottomMargin=52)
    elements = []
    
    # Configuración de estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    
    # Logo y título
    logo = Image(logo_path, width=1*inch, height=1*inch)
    title = Paragraph(
        """<b>ORGANIZACIÓN ELECTORAL</b><br/>
        <b>CONSEJO NACIONAL ELECTORAL</b><br/>
        Fondo Nacional De Financiación Política<br/>""",
        styles["Title"]
    )
    
    # Crear una tabla para organizar el logo y el título en la misma línea
    title_logo_table = Table([[title, logo]], colWidths=[7.0 * inch, 1 * inch])
    title_logo_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (1, 0), 'TOP'),
    ]))
    elements.append(title_logo_table)
    
    # Espacio entre título y contenido
    elements.append(Spacer(1, 12))
    
    # Titulo del informe
    titulo_info = f"""
    <b>Informe :</b> {informe}<br/>
    """
    elements.append(Paragraph(titulo_info, styles["Normal"]))
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 12))
    
    # Encabezado de la organización política
    encabezado_info = f"""
    <b>Nombre Agrupación Política:</b> {organizacion_politica}<br/>
    <b>NIT:</b> {nit}<br/>
    <b>Representante Legal:</b> {representante_legal} ({documento_representante})<br/>
    """
    elements.append(Paragraph(encabezado_info, styles["Normal"]))
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 12))
    
    # Títulos de las tablas
    encabezado_tabla = [['CODIGO', 'CONCEPTO', 'VALOR']]
    
    # Tabla de resumen financiero
    data_resumen = [
        ["1", "Total Patrimonio Bruto a 31 de diciembre", f'{total_patrimonio_bruto:,.0f}'],
        ["2", "Deudas a 31 de diciembre", f'{deudas:,.0f}'],
        ["3", "Total Patrimonio Líquido a 31 de diciembre", f'{total_patrimonio_liquido:,.0f}'],
    ]
    tabla_resumen = Table(encabezado_tabla + data_resumen, colWidths=[0.5*inch, 6*inch, 1*inch])
    tabla_resumen.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabla_resumen)
    
    # Espacio antes de las tablas detalladas
    elements.append(Spacer(1, 12))
    
    # Tablas detalladas de ingresos y egresos
    ingresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in ingresos_df[['codigo', 'nombre', 'valor']].values]
    egresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in egresos_df[['codigo', 'nombre', 'valor']].values]
    
    # Añadir totales
    ingresos_data.append(["", "Total Ingresos Anuales", f'{total_ingresos:,.2f}'])
    egresos_data.append(["", "Total Egresos Anuales", f'{total_egresos:,.2f}'])
    
    # Crear tabla de ingresos y egresos
    tabla_ingresos_egresos = Table(encabezado_tabla + ingresos_data + egresos_data, colWidths=[0.5*inch, 6*inch, 1*inch])
    tabla_ingresos_egresos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    elements.append(tabla_ingresos_egresos)
    
    # Pie de página
    pie_de_pagina = Paragraph(
        """<b>Las cifras se expresan en pesos colombianos.</b><br/>
        Firma del Representante Legal_________________________<br/>
        Firma del Auditor_________________________<br/>""",
        styles["Justify"]
    )
   # elements.append(Spacer(1, 36))
   # elements.append(pie_de_pagina)
    
    # Añadir una línea horizontal utilizando Drawing
    line = Drawing(500, 10)
    line.add(Line(0, 0, 450, 0))
    
    # Añadir las líneas y el pie de página
    elements.append(line)
    elements.append(Spacer(1, 6))
    elements.append(pie_de_pagina)
    elements.append(Spacer(1, 6))
    elements.append(line)
    
    # Generar PDF
    doc.build(elements)

def reporte2c(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc, pdf_path):
    
    # Variables del encabezado
    organizacion_politica = datasetc['nombre'].unique()[0]
    nombre_completo = datasetc['nombre_completo'].unique()[0]
    numero_documento = datasetc['numero_documento'].unique()[0]

    # Configuración de la visualización
    fig = plt.figure(figsize=(10, 12))
    gs = GridSpec(5, 1, height_ratios=[0.8, 1, 2, 3, 4])

    # Títulos del reporte
    fig.suptitle("ORGANIZACIÓN ELECTORAL\nCONSEJO NACIONAL ELECTORAL\nFondo Nacional De Financiación Política\nINFORME INDIVIDUAL DE INGRESOS Y GASTOS DE LA CAMPAÑA", fontsize=14, fontweight='bold', ha='center')

    # Filtro título
    ax_filtro = fig.add_subplot(gs[0])
    ax_filtro.axis('off')
    ax_filtro.text(0.5, 0.7, f"Nombre Agrupación Política: {organizacion_politica}\n", ha='center', fontsize=12)
 #   ax_filtro.text(0.5, 0.5, f"NIT: {nit}", ha='center', fontsize=12)

    # encabezado con marco y firmas
    ax3 = fig.add_subplot(gs[1])
    ax3.axis('off')

    # Crear marco para el encabezado 1
    rect0 = mpatches.Rectangle((0, 0), 1.1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax3.transAxes, clip_on=False)
    ax3.add_patch(rect0)

    # Texto del encabezado 1
    ax3.text(0.1, 0.35, f"Candidato: {nombre_completo}", ha='center', fontsize=10)
    ax3.text(0.8, 0.35, f"Cedula de Ciudadania: {numero_documento}", ha='center', fontsize=10)

    # Encabezado con consecutivo, patrimonio, representante legal y deudas
    ax0 = fig.add_subplot(gs[2])
    ax0.axis('tight')
    ax0.axis('off')

    # Datos de encabezado 2

    encabezado_data = [
        ["1", "Total Ingresos a 31 de diciembre (Según Balance general)", f'{total_ingresosc:,.0f}'],
        ["2", "Total Gastos  a 31 de diciembre", f'{total_egresosc:,.0f}']
    ]

    ax0.table(cellText=encabezado_data, colWidths=[0.1, 1, 0.2], cellLoc='center', loc='center')

    # Tabla detallada de ingresos y egresos
    ax1 = fig.add_subplot(gs[3])
    ax1.axis('tight')
    ax1.axis('off')

    # Preparar tabla de ingresos y egresos
    # Formatear los valores de la columna 'valor' con separadores de miles y 2 decimales
    ingresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in ingresos_dfc[['codigo', 'descripcion', 'valor']].values]
    egresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in egresos_dfc[['codigo', 'descripcion', 'valor']].values]


    # Crear la tabla completa con los valores formateados
    table_data = ingresos_data + \
                [["", "Total Ingresos Anuales", f'{total_ingresosc:,.2f}']] + \
                egresos_data + \
                [["", "Total Egresos Anuales", f'{total_egresosc:,.2f}']]

    # Definir la tabla con justificación centrada y tamaño de letra
    tabla = ax1.table(cellText=table_data, 
                    colLabels=["CODIGO", "CONCEPTO", "VALOR"], 
                    cellLoc='center',  # Justificación centrada por defecto
                    loc='center',
                    colWidths=[0.1, 1, 0.2],  # Ajustar el ancho de las columnas
                    fontsize=16)  # Tamaño inicial de la letra


    for key, cell in tabla.get_celld().items():
        if key[1] == 0 or key[1] == 1:  # Columnas 'Código' y 'Nombre'
            cell.set_text_props(ha='left')  # Alinear a la izquierda
        if key[1] == 2 :  # Columna valor
            cell.set_text_props(ha='right')  # Alinear a la izquierda        
        cell.set_fontsize(31)  # Aumentar el tamaño de la letra en todas las celdas


    # Pie de página con marco y firmas
    ax2 = fig.add_subplot(gs[4])
    ax2.axis('off')

    # Crear marco para el pie de página
    rect = mpatches.Rectangle((0, 0), 1, 0.5, linewidth=1, edgecolor='black', facecolor='none', transform=ax2.transAxes, clip_on=False)
    ax2.add_patch(rect)

    # Texto del pie de página
    ax2.text(0.5, 0.35, "Las cifras registradas en este formulario fueron tomadas fielmente del libro de Ingresos y Gastos.", ha='center', fontsize=10)
    ax2.text(0.2, 0.1, "Firma del Candidato", ha='center', fontsize=10)
    ax2.text(0.8, 0.1, "Firma del Auditor", ha='center', fontsize=10)

    # Ajustar el layout
    st.pyplot(fig) 

    # Guardar la figura en un PDF temporal
    with PdfPages(pdf_path) as pdf:
            pdf.savefig(fig)
    plt.close(fig)  # Cerrar la figura para liberar memoria          

def todos(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, logo):
    # Definir ruta para los archivos PDF temporales
    pdf_path1 = "reporte5.pdf"
    pdf_path2 = "reporte6.pdf"
    pdf_path3 = "reportemejorado.pdf"
    combined_pdf_path = "reporte_combinado.pdf"

    # Generar ambos reportes
    pdfs = []
    informe1 = "DECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES"
    reporte5(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path1, logo, informe1)
    pdfs.append(pdf_path1)
    
    informe1 = "INFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN"
    reporte6(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path2, logo, informe1)
    pdfs.append(pdf_path2)
    
    informe1 = "GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011"
    reporte_mejorado(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path3, logo, informe1)
    pdfs.append(pdf_path2)
    
    generar_pdf(pdfs)
    open_pdf(combined_pdf_path)

def todosc(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc):
    # Definir ruta para los archivos PDF temporales
    pdf_path1 = "reporte1c.pdf"
    pdf_path2 = "reporte2c.pdf"
    combined_pdf_path = "reporte_combinado.pdf"

    # Generar ambos reportes
    pdfs = []
    reporte1c(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc, pdf_path1)
    pdfs.append(pdf_path1)
    
    reporte2c(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc, pdf_path2)
    pdfs.append(pdf_path2)
    
    generar_pdf(pdfs)
    open_pdf(combined_pdf_path)
  
def todosc1(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdf, logo):
    # Definir ruta para los archivos PDF temporales
    pdf_path1 = "reporte1c.pdf"
    pdf_path2 = "reporte2c.pdf"
    combined_pdf_path = "reporte_combinado.pdf"

    # Generar ambos reportes
    pdfs = []
    reporte1c(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc,  pdf_path1, logo)
    pdfs.append(pdf_path1)
    
    generar_pdf(pdfs)
    open_pdf(combined_pdf_path)  
       
def varios(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdfs):
    
    combined_pdf_path = "reporte_combinado.pdf"
    # Si se seleccionó más de un informe, combinarlos
    
    for pdf in pdfs:
        if pdf == "reporte5.pdf":
            reporte1(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf)
        elif pdf == "reporte6.pdf":
            reporte2(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf)
        elif pdf == "reporte3.pdf":
            reporte3(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf)
        elif pdf == "reporte1c.pdf":
            reporte1c(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdf_path, logo_path)
    
    if len(pdfs) > 1:
       generar_pdf(pdfs)
       open_pdf(combined_pdf_path)
    elif len(pdfs) == 1:
        open_pdf(pdfs[0])
        
def varios1(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdfs, logo):
    
    combined_pdf_path = "reporte_combinado.pdf"
    # Si se seleccionó más de un informe, combinarlos
    
    for pdf in pdfs:
        if pdf == "reporte1.pdf":
            informe1 = "DECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES"
            reporte5(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf, logo, informe1)
        elif pdf == "reporte2.pdf":
            informe1 = "INFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN"
            reporte6(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf, logo, informe1)
        elif pdf == "reporte3.pdf":
            informe1 = "GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011"
            reporte_mejorado(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf, logo, informe1)
    
    if len(pdfs) > 1:
       generar_pdf(pdfs)
       open_pdf(combined_pdf_path)
    elif len(pdfs) == 1:
        open_pdf(pdfs[0])        
        
        
def open_pdf(pdf_path):
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="Descargar PDF .....",
                    data=file,
                    file_name="https://raw.githubusercontent.com/CNE-ORG/cuentasclaras/main/data/reporte_combinado.pdf"
                )           
        else:
            st.error("El archivo PDF no fue encontrado.")    

def generar_pdf(pdfs):
    combined_pdf_path = "reporte_combinado.pdf"
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
        merger.write(combined_pdf_path)
 #       merger.close()

    # Eliminar los PDFs individuales después de combinarlos
 #   for pdf in pdfs:
 #       os.remove(pdf)
 
def reporte_mejorado(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path, logo_path, informe):
    # Variables del encabezado
    total_patrimonio_bruto = dataset['total_patrimonio'].unique()[0]
    total_patrimonio_liquido = dataset['patrimonio_liquido'].unique()[0]
    nit = dataset['nit'].unique()[0]
    representante_legal = dataset['representante_legal'].unique()[0]
    organizacion_politica = dataset['nombre_agrupacion_politica'].unique()[0]
    documento_representante = dataset['documento_representante'].unique()[0]
    deudas = dataset['deudas'].unique()[0]
    
    total_patrimonio_neto = total_patrimonio_bruto - deudas
    
    # Crear PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=2 * inch, leftMargin=2 * inch, topMargin=3 * inch, bottomMargin=2 * inch)
    elements = []
    
    # Configuración de estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    
    # Logo y título
    logo = Image(logo_path, width=1*inch, height=1*inch)  # Ajustar tamaño del logo
    title = Paragraph(
        """<b>ORGANIZACIÓN ELECTORAL</b><br/>
        <b>CONSEJO NACIONAL ELECTORAL</b><br/>
        Fondo Nacional De Financiación Política<br/>""",
        styles["Title"]
    )
    
    # Crear una tabla para organizar el logo y el título en la misma línea
    title_logo_table = Table([[title, logo]], colWidths=[4.5 * inch, 1.5 * inch])
    title_logo_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (1, 0), 'TOP'),
    ]))
    elements.append(title_logo_table)
    
    # Espacio entre título y contenido
    elements.append(Spacer(1, 12))
    
    # Titulo del informe
    titulo_info = f"""
    <b>Informe :</b> {informe}<br/>
    """
    elements.append(Paragraph(titulo_info, styles["Normal"]))
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 12))
    
    
    
    # Encabezado de la organización política
    encabezado_info = f"""
    <b>Nombre Agrupación Política:</b> {organizacion_politica}<br/>
    <b>NIT:</b> {nit}<br/>
    <b>Representante Legal:</b> {representante_legal} ({documento_representante})<br/>
    """
    elements.append(Paragraph(encabezado_info, styles["Normal"]))
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 12))
    
    # Títulos de las tablas
    encabezado_tabla = [['CODIGO', 'CONCEPTO', 'VALOR']]
    
    # Tablas detalladas de ingresos y egresos
    ingresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in ingresos_df[['codigo', 'nombre', 'valor']].values]
    egresos_data = [[row[0], row[1], f'{row[2]:,.2f}'] for row in egresos_df[['codigo', 'nombre', 'valor']].values]
    
    # Añadir totales
    ingresos_data.append(["", "Total Ingresos Anuales", f'{total_ingresos:,.2f}'])
    egresos_data.append(["", "Total Egresos Anuales", f'{total_egresos:,.2f}'])
    
    # Crear tabla de ingresos y egresos
    tabla_ingresos_egresos = Table(encabezado_tabla + ingresos_data + egresos_data, colWidths=[1.5*inch, 3.5*inch, 1.5*inch])
    tabla_ingresos_egresos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    elements.append(tabla_ingresos_egresos)
    
    # Espacio antes del pie de página
    elements.append(Spacer(1, 24))
    
    # Pie de página con líneas horizontales
    pie_de_pagina = Paragraph(
        """<b>Las cifras se expresan en pesos colombianos.</b><br/>
        Firma del Representante Legal_________________________<br/>
        Firma del Auditor_________________________<br/>""",
        styles["Normal"]
    )
    
    # Añadir una línea horizontal utilizando Drawing
    line = Drawing(500, 10)
    line.add(Line(0, 0, 450, 0))
    
    # Añadir las líneas y el pie de página
    elements.append(line)
    elements.append(Spacer(1, 6))
    elements.append(pie_de_pagina)
    elements.append(Spacer(1, 6))
    elements.append(line)
    
    # Generar PDF
    doc.build(elements)


    