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
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.graphics.shapes import Line
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing

def reporte1c(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdf_path, logo_path, informe, title_size=12):
    
    # Variables del encabezado
    organizacion_politica = datasetc['nombre'].unique()[0]
    nombre_completo = datasetc['nombre_completo'].unique()[0]
    numero_documento = datasetc['numero_documento'].unique()[0]
    nit = datasetc['tipo_organizacion'].unique()[0]

    # Crear PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=32, leftMargin=52, topMargin=32, bottomMargin=52)
    elements = []
    
     # Inicializar los estilos al principio de la función
    styles = getSampleStyleSheet()
    
    # Llamar a la función para crear el encabezado
    encabezado = crear_encabezado(logo_path, informe, title_size)
    elements.append(encabezado)
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 6))  # Reducido para ahorrar espacio
 
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


    # Espacio antes del pie de página
    elements.append(Spacer(1, 6))  # Reducido para ahorrar espacio

    # Llamar a la función para crear el pie de página
    pie_de_pagina = crear_pie_de_pagina()
    elements.append(pie_de_pagina)
    
    # Generar PDF
    doc.build(elements)      

def reporte4c(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdf_path, logo_path, informe, title_size=14):
    
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
    styles.add(ParagraphStyle(name="TitleCustom", fontSize=title_size, alignment=TA_CENTER))
    
    # Logo y título ajustable
    logo = Image(logo_path, width=1*inch, height=1*inch)
    title = Paragraph(
        """<b>ORGANIZACIÓN ELECTORAL</b><br/>
        <b>CONSEJO NACIONAL ELECTORAL</b><br/>
        Fondo Nacional De Financiación Política<br/>""",
        styles["TitleCustom"]
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
    <b>Nombre Candidato:</b> {nombre_completo}<br/>
    <b>Cedula de Ciudadania:</b> {numero_documento}<br/>
    <b>Nombre Agrupación Política:</b> {organizacion_politica} ({nit})<br/>
    """
    elements.append(Paragraph(encabezado_info, styles["Normal"]))
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 12))

    # Unificación de columnas en una sola encabezada por "PATRIMONIO"
    encabezado_tabla = [['PATRIMONIO']]
    
    # Tabla de resumen financiero
    data_resumen = [
        ["Total Ingresos a 31 de diciembre (Según Balance general):", f'{total_ingresosc:,.0f}'],
        ["Total Gastos a 31 de diciembre:", f'{total_egresosc:,.0f}'],
    ]
    tabla_resumen = Table(encabezado_tabla + data_resumen, colWidths=[6.5*inch, 1*inch])
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
    
    
    # Obtener estilos
    styles = getSampleStyleSheet()

    # Crear un estilo con ajuste de texto
    text_style = ParagraphStyle(name='TextStyle', fontName='Helvetica', fontSize=7, alignment=1)


    # Tablas detalladas de ingresos y egresos con ajuste de texto automático
    #ingresos_data = [[row[0], Paragraph(row[1], styles["Normal"]), f'{row[2]:,.2f}'] for row in ingresos_dfc[['codigo', 'descripcion', 'valor']].values]
    #egresos_data = [[row[0], Paragraph(row[1], styles["Normal"]), f'{row[2]:,.2f}'] for row in egresos_dfc[['codigo', 'descripcion', 'valor']].values]
    
    ingresos_data = [[row[0], Paragraph(row[1], text_style), f'{row[2]:,.2f}'] for row in ingresos_df[['codigo', 'nombre', 'valor']].values]
    egresos_data = [[row[0], Paragraph(row[1], text_style), f'{row[2]:,.2f}'] for row in egresos_df[['codigo', 'nombre', 'valor']].values]
    
    # Añadir totales
    #ingresos_data.append(["", "Total Ingresos Anuales", f'{total_ingresosc:,.2f}'])
    #egresos_data.append(["", "Total Egresos Anuales", f'{total_egresosc:,.2f}'])
    
    ingresos_data.append(["", Paragraph("Total Ingresos Anuales", text_style), f'{total_ingresos:,.2f}'])
    egresos_data.append(["", Paragraph("Total Egresos Anuales", text_style), f'{total_egresos:,.2f}'])
    
    # Crear tabla de ingresos y egresos
    tabla_ingresos_egresos = Table(ingresos_data + egresos_data, colWidths=[0.5*inch, 6*inch, 1*inch])
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

    # Espacio antes del pie de página
    elements.append(Spacer(1, 36))

    # Pie de página enmarcado
    pie_de_pagina = Paragraph(
        """<b>Las cifras registradas en este formulario fueron tomadas fielmente del libro de Ingresos y Gastos.</b><br/>
        Firma del Candidato_________________________<br/>
        Firma del Auditor_________________________<br/>""",
        styles["Justify"]
    )

    # Añadir líneas horizontales y verticales en el pie de página
    footer_table = Table(
        [[pie_de_pagina]],
        colWidths=[7.5*inch]
    )
    footer_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(footer_table)
    
    # Generar PDF
    doc.build(elements) 

def reporte1(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path, logo_path, informe, title_size=12):
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
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=28, leftMargin=28, topMargin=28, bottomMargin=28)
    elements = []
    
     # Inicializar los estilos al principio de la función
    styles = getSampleStyleSheet()
    
    # Llamar a la función para crear el encabezado
    encabezado = crear_encabezado(logo_path, informe, title_size)
    elements.append(encabezado)
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 6))  # Reducido para ahorrar espacio
    
    # Encabezado de la organización política
    encabezado_info = f"""
    <b>Nombre Agrupación Política:</b> {organizacion_politica}<br/>
    <b>NIT:</b> {nit}<br/>
    <b>Representante Legal:</b> {representante_legal} ({documento_representante})<br/>
    """
    elements.append(Paragraph(encabezado_info, styles["Normal"]))
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 6))  # Reducido para ahorrar espacio
    
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
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(tabla_resumen)
    
    # Espacio antes de las tablas detalladas
    elements.append(Spacer(1, 12))
    
    # Obtener estilos
    styles = getSampleStyleSheet()

    # Crear un estilo con ajuste de texto
    text_style = ParagraphStyle(name='TextStyle', fontName='Helvetica', fontSize=7, alignment=0, wordWrap='CJK')
    
    # Definir un nuevo estilo para los totales
    total_style = ParagraphStyle(name='TotalStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, spaceAfter=6, alignment=0)

    # Tablas detalladas de ingresos y egresos
    ingresos_data = [[row[0], Paragraph(row[1], text_style), f'{row[2]:,.2f}'] for row in ingresos_df[['codigo', 'nombre', 'valor']].values]
    egresos_data = [[row[0], Paragraph(row[1], text_style), f'{row[2]:,.2f}'] for row in egresos_df[['codigo', 'nombre', 'valor']].values]
    
    # Añadir totales
    ingresos_data.append([Paragraph("100", total_style), Paragraph("Total Ingresos Anuales", total_style), Paragraph(f'{total_ingresos:,.2f}', text_style)])
    egresos_data.append([Paragraph("200", total_style), Paragraph("Total Egresos Anuales", total_style), f'{total_egresos:,.2f}'])
    
    # Crear tabla de ingresos y egresos
    tabla_ingresos_egresos = Table(encabezado_tabla + ingresos_data + egresos_data, colWidths=[0.5*inch, 6*inch, 1*inch])
    tabla_ingresos_egresos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    elements.append(tabla_ingresos_egresos)
    
    # Espacio antes del pie de página
    elements.append(Spacer(1, 6))  # Reducido para ahorrar espacio

    # Llamar a la función para crear el pie de página
    pie_de_pagina = crear_pie_de_pagina()
    elements.append(pie_de_pagina)
    
    # Espacio antes del pie de página
    elements.append(Spacer(1, 6))  # Reducido para ahorrar espacio
    
    
    # Llamar a la función para crear el segundo pie de página
    pie_de_pagina2 = crear_pie_de_pagina2()
    elements.append(pie_de_pagina2)
    
    # Generar PDF
    doc.build(elements)    
   
def reporte2(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path, logo_path, informe, title_size=12):

    
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
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=28, leftMargin=28, topMargin=28, bottomMargin=28)
    elements = []
    
     # Inicializar los estilos al principio de la función
    styles = getSampleStyleSheet()
    
    # Llamar a la función para crear el encabezado
    encabezado = crear_encabezado(logo_path, informe, title_size)
    elements.append(encabezado)
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 6))  # Reducido para ahorrar espacio
    
    # Encabezado de la organización política
    encabezado_info = f"""
    <b>Nombre Agrupación Política:</b> {organizacion_politica}<br/>
    <b>NIT:</b> {nit}<br/>
    <b>Representante Legal:</b> {representante_legal} ({documento_representante})<br/>
    """
    elements.append(Paragraph(encabezado_info, styles["Normal"]))
    
    # Espacio antes de las tablas detalladas
    elements.append(Spacer(1, 32))
    
    # Obtener estilos
    styles = getSampleStyleSheet()

    # Crear un estilo con ajuste de texto
    text_style = ParagraphStyle(name='TextStyle', fontName='Helvetica', fontSize=7, alignment=0, wordWrap='CJK')
    
    # Definir un nuevo estilo para los totales
    total_style = ParagraphStyle(name='TotalStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, spaceAfter=6, alignment=0)

    # Filtro codigo
    # Filtrar ingresos y egresos
    ingresos_df2 = ingresos_df[ingresos_df['codigo'] == 1]
    egresos_df2 = egresos_df[egresos_df['codigo'] == 2] 

    # Tablas detalladas de ingresos y egresos
    ingresos_data = [[row[0], Paragraph(row[1], text_style), f'{row[2]:,.2f}'] for row in ingresos_df2[['codigo', 'nombre', 'valor']].values]
    egresos_data = [[row[0], Paragraph(row[1], text_style), f'{row[2]:,.2f}'] for row in egresos_df2[['codigo', 'nombre', 'valor']].values]
    
    # Añadir totales
    #ingresos_data.append([Paragraph("100", total_style), Paragraph("Total Ingresos Anuales", total_style), f'{total_ingresos:,.2f}'])
    #egresos_data.append(["200", Paragraph("Total Egresos Anuales", total_style), f'{total_egresos:,.2f}'])
    
    
    # Títulos de las tablas
    encabezado_tabla = [['CODIGO', 'CONCEPTO', 'VALOR']]
    
    # Crear tabla de ingresos y egresos
    tabla_ingresos_egresos = Table(encabezado_tabla + ingresos_data + egresos_data, colWidths=[0.5*inch, 6*inch, 1*inch])
    tabla_ingresos_egresos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    elements.append(tabla_ingresos_egresos)
    
    # Espacio antes del pie de página
    elements.append(Spacer(1, 24))  # Reducido para ahorrar espacio

    # Llamar a la función para crear el segundo pie de página
    pie_de_pagina3 = crear_pie_de_pagina3()
    elements.append(pie_de_pagina3)
    
    # Generar PDF
    doc.build(elements)  

def reporte3(datasetg, ingresos_dfg, egresos_dfg, total_ingresosg, total_egresosg, pdf_path, logo_path, informe, title_size=12):

    nit = datasetg['nit'].unique()[0]
    representante_legal = datasetg['representante_legal'].unique()[0]
    organizacion_politica = datasetg['nombre_agrupacion_politica'].unique()[0]
    documento_representante = datasetg['documento_representante'].unique()[0]
        
    # Crear PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=28, leftMargin=28, topMargin=28, bottomMargin=28)
    elements = []
    
     # Inicializar los estilos al principio de la función
    styles = getSampleStyleSheet()
    
    # Llamar a la función para crear el encabezado
    encabezado = crear_encabezado(logo_path, informe, title_size)
    elements.append(encabezado)
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 6))  # Reducido para ahorrar espacio
    
    # Encabezado de la organización política
    encabezado_info = f"""
    <b>Nombre Agrupación Política:</b> {organizacion_politica}<br/>
    <b>NIT:</b> {nit}<br/>
    <b>Representante Legal:</b> {representante_legal} ({documento_representante})<br/>
    """
    elements.append(Paragraph(encabezado_info, styles["Normal"]))
    
    # Espacio antes de las tablas detalladas
    elements.append(Spacer(1, 32))
    
    # Obtener estilos
    styles = getSampleStyleSheet()

    # Crear un estilo con ajuste de texto
    text_style = ParagraphStyle(name='TextStyle', fontName='Helvetica', fontSize=7, alignment=0, wordWrap='CJK')
    
    # Definir un nuevo estilo para los totales
    total_style = ParagraphStyle(name='TotalStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, spaceAfter=6, alignment=0)

    # Filtro codigo
    # Filtrar ingresos y egresos
    ingresos = ingresos_dfg[ingresos_dfg['tipo'] == 1]
    egresos = egresos_dfg[egresos_dfg['tipo'] == 2] 

    # Tablas detalladas de ingresos y egresos
    ingresos_data = [[row[0], Paragraph(row[1], text_style), f'{row[2]:,.2f}'] for row in ingresos[['codigo', 'descripcion', 'valor']].values]
    egresos_data = [[row[0], Paragraph(row[1], text_style), f'{row[2]:,.2f}'] for row in egresos[['codigo', 'descripcion', 'valor']].values]
    
    
    # Añadir totales
    egresos_data.append(["", Paragraph("Valor Total: $", total_style), f'{total_egresosg:,.2f}'])
    
    # Títulos de las tablas
    encabezado_tabla = [['CODIGO', 'CONCEPTO', 'VALOR']]
    
    # Crear tabla de ingresos y egresos
    tabla_ingresos_egresos = Table(encabezado_tabla + ingresos_data + egresos_data, colWidths=[0.5*inch, 6*inch, 1*inch])
    tabla_ingresos_egresos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    elements.append(tabla_ingresos_egresos)
    
    # Espacio antes del pie de página
    elements.append(Spacer(1, 24))  # Reducido para ahorrar espacio

    # Llamar a la función para crear el segundo pie de página
    pie_de_pagina3 = crear_pie_de_pagina3()
    elements.append(pie_de_pagina3)
    
    # Generar PDF
    doc.build(elements)       
    
def reporte4(dataseti, ingresos_dfi, egresos_dfi, total_ingresosi, total_egresosi, pdf_path, logo_path, informe, title_size=12):

    #nit = dataseti['nit'].unique()[0]
    #representante_legal = dataseti['representante_legal'].unique()[0]
    #organizacion_politica = dataseti['nombre_agrupacion_politica'].unique()[0]
    #documento_representante = dataseti['documento_representante'].unique()[0]
       
    # Verificar si dataseti tiene registros antes de acceder a sus datos
    if dataseti.empty:
        st.error("No hay datos disponibles para la agrupación política seleccionada.")
        return  # Detener la ejecución de la función si no hay datos

    # Asegurarse de que el valor de 'nit' esté presente
    nit_values = dataseti['nit'].unique()
    if len(nit_values) == 0:
        nit = "N/A"  # Valor por defecto si no hay NIT
    else:
        nit = nit_values[0]

    representante_legal_values = dataseti['representante_legal'].unique()
    if len(representante_legal_values) == 0:
        representante_legal = "N/A"  # Valor por defecto si no hay representante legal
    else:
        representante_legal = representante_legal_values[0]

    organizacion_politica_values = dataseti['nombre_agrupacion_politica'].unique()
    if len(organizacion_politica_values) == 0:
        organizacion_politica = "N/A"  # Valor por defecto si no hay nombre de agrupación política
    else:
        organizacion_politica = organizacion_politica_values[0]

    documento_representante_values = dataseti['documento_representante'].unique()
    if len(documento_representante_values) == 0:
        documento_representante = "N/A"  # Valor por defecto si no hay documento de representante
    else:
        documento_representante = documento_representante_values[0]
      
    # Crear PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter), rightMargin=28, leftMargin=28, topMargin=28, bottomMargin=28)
    elements = []
    
    # Inicializar los estilos al principio de la función
    styles = getSampleStyleSheet()
    
    # Llamar a la función para crear el encabezado
    encabezado = crear_encabezado(logo_path, informe, title_size)
    elements.append(encabezado)
    
    # Espacio antes de las tablas
    elements.append(Spacer(1, 6))  # Reducido para ahorrar espacio
    
    # Encabezado de la organización política
    encabezado_info = f"""
    <b>Nombre Agrupación Política:</b> {organizacion_politica}<br/>
    <b>NIT:</b> {nit}<br/>
    <b>Representante Legal:</b> {representante_legal} ({documento_representante})<br/>
    """
    elements.append(Paragraph(encabezado_info, styles["Normal"]))
    
    # Espacio antes de las tablas detalladas
    elements.append(Spacer(1, 32))
    
    # Obtener estilos
    styles = getSampleStyleSheet()

    # Crear un estilo con ajuste de texto
    text_style = ParagraphStyle(name='TextStyle', fontName='Helvetica', fontSize=7, alignment=0, wordWrap='CJK')
    
    # Definir un nuevo estilo para los totales
    total_style = ParagraphStyle(name='TotalStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, spaceAfter=6, alignment=0)

    # Filtro codigo
    # Filtrar ingresos y egresos
    ingresos = ingresos_dfi[ingresos_dfi['tipo'] == 1]
    egresos = egresos_dfi[egresos_dfi['tipo'] == 2] 

    # Tablas detalladas de ingresos y egresos
    ingresos_data = [[Paragraph(row[0], text_style), row[1], row[2], Paragraph(row[3], text_style),Paragraph(row[4], text_style), row[5], f'{row[6]:,.2f}'] for row in ingresos[['persona', 'cedula', 'telefono', 'direccion', 'concepto', 'acta', 'valor']].values]
    
    # Añadir totales
    ingresos_data.append(["", "", "", "", Paragraph("Valor Total: $", total_style), "", f'{total_ingresosi:,.2f}'])
    
    # Títulos de las tablas
    encabezado_tabla = [['NOMBRE DE LA PERSONA', 'NIT-CEDULA', 'TELEFONO', 'DIRECCION', 'CONCEPTO', 'ACTA', 'VALOR']]

    # Ajustar el ancho de las columnas para que se alineen mejor
    col_ancho = [2.4 * inch, 0.9 * inch, 0.8 * inch, 2 * inch, 2.5 * inch, 0.4 * inch, 1 * inch]

    # Crear tabla de ingresos y egresos
    tabla_ingresos_egresos = Table(encabezado_tabla + ingresos_data, colWidths=col_ancho)
    tabla_ingresos_egresos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    
    # Añadir la tabla ajustada a los elementos
    elements.append(tabla_ingresos_egresos)
    
    # Espacio antes del pie de página
    elements.append(Spacer(1, 24))  # Reducido para ahorrar espacio

    # Llamar a la función para crear el segundo pie de página
    pie_de_pagina3 = crear_pie_de_pagina3()
    elements.append(pie_de_pagina3)
    
    # Generar PDF
    doc.build(elements)          
    
def todos(dataset, datasetg, dataseti, ingresos_df, ingresos_dfg, ingresos_dfi, egresos_df, egresos_dfg, egresos_dfi, total_ingresos, total_ingresosg, total_ingresosi, total_egresos, total_egresosg, total_egresosi, logo):
    # Definir ruta para los archivos PDF temporales
    pdf_path1 = "reporte1.pdf"
    pdf_path2 = "reporte2.pdf"
    pdf_path3 = "reporte3.pdf"
    pdf_path4 = "reporte4.pdf"
    combined_pdf_path = "reporte_combinado.pdf"

    # Generar ambos reportes
    pdfs = []
    informe1 = "DECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES"
    reporte1(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path1, logo, informe1)
    if os.path.exists(pdf_path1):
        pdfs.append(pdf_path1)
    
    informe1 = "INFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN"
    reporte2(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf_path2, logo, informe1)
    if os.path.exists(pdf_path2):
        pdfs.append(pdf_path2)
    
    informe1 = "GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011"
    reporte3(datasetg, ingresos_dfg, egresos_dfg, total_ingresosg, total_egresosg, pdf_path3, logo, informe1)
    if os.path.exists(pdf_path3):
        pdfs.append(pdf_path3)
    
    informe1 = "CONTRIBUCIONES, DONACIONES Y CREDITOS, EN DINERO O EN ESPECIE, DE SUS AFILIADOS Y/O DE PARTICULARES"
    if not dataseti.empty:  # Verifica si hay datos antes de generar el reporte
        reporte4(dataseti, ingresos_dfi, egresos_dfi, total_ingresosi, total_egresosi, pdf_path4, logo, informe1)
    if os.path.exists(pdf_path4):
            pdfs.append(pdf_path4)
    
    generar_pdf(pdfs)
    open_pdf(combined_pdf_path)

def todosc(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdf, logo):
    # Definir ruta para los archivos PDF temporales
    pdf_path1 = "reporte1c.pdf"
    pdf_path2 = "reporte2c.pdf"
    combined_pdf_path = "reporte_combinado.pdf"

    # Generar ambos reportes
    pdfs = []
    informe = "INFORME INDIVIDUAL DE INGRESOS Y GASTOS DE LA CAMPAÑA"
    reporte1c(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc, pdf_path1, logo, informe)
    pdfs.append(pdf_path1)
   
    generar_pdf(pdfs)
    open_pdf(combined_pdf_path)
  
def todosc1(datasetc, ingresos_dfc, egresos_dfc, total_ingresosc, total_egresosc, pdf, logo):
    # Definir ruta para los archivos PDF temporales
    pdf_path1 = "reporte1c.pdf"
    pdf_path2 = "reporte2c.pdf"
    combined_pdf_path = "reporte_combinado.pdf"

    # Generar ambos reportes
    pdfs = []
    informe1 = "Error"
    reporte4c(datasetc,ingresos_dfc,egresos_dfc,total_ingresosc,total_egresosc, pdf_path1, logo, informe1)
    pdfs.append(pdf_path1)
    
    generar_pdf(pdfs)
    open_pdf(combined_pdf_path)  
       
       
def varios1(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdfs, logo):
    
    combined_pdf_path = "reporte_combinado.pdf"
    # Si se seleccionó más de un informe, combinarlos
    
    for pdf in pdfs:
        if pdf == "reporte1.pdf":
            informe1 = "DECLARACION DE PATRIMONIO, INGRESOS Y GASTOS ANUALES"
            reporte1(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf, logo, informe1)
        elif pdf == "reporte2.pdf":
            informe2 = "INFORME DE INGRESOS Y GASTOS ESTATUTO DE LA OPOSICIÓN"
            reporte2(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf, logo, informe2)
        elif pdf == "reporte3.pdf":
            informe3 = "GASTOS DESTINADOS PARA ACTIVIDADES CONTEMPLADAS EN EL ARTICULO 18 DE LA LEY 1475 DE 2011"
            reporte3(dataset, ingresos_df, egresos_df, total_ingresos, total_egresos, pdf, logo, informe3)            
    
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
    
    # Añadir todos los PDFs al merger
    for pdf in pdfs:
        if os.path.exists(pdf):  # Verifica si el archivo existe
            merger.append(pdf)
        else:
            print(f"Advertencia: El archivo {pdf} no se encontró y no se incluirá en el PDF combinado.")
    
    # Guardar el PDF combinado si hay archivos válidos
    if merger.pages:
        merger.write(combined_pdf_path)
        merger.close()
    else:
        print("No se generaron archivos PDF para combinar.") 
    
    # Cerrar el archivo
    merger.close()

    # Eliminar los PDFs individuales después de combinarlos
    for pdf in pdfs:
        os.remove(pdf)
        
def crear_encabezado(logo_path, informe, title_size=12):
    # Configuración de estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCustom", fontSize=title_size, alignment=TA_CENTER))
    
    informe = str(informe).strip('[]')
    informe = str(informe).strip("'")
    
    # Logo y título con el informe integrado, eliminando corchetes y la coma
    logo = Image(logo_path, width=1*inch, height=1*inch)
    title_content = f"""
        <b>ORGANIZACIÓN ELECTORAL</b><br/>
        <b>CONSEJO NACIONAL ELECTORAL</b><br/>
        Fondo Nacional De Financiación Política<br/>
        {informe} <br/>
    """
    
    # Crear el párrafo del título
    title = Paragraph(title_content, styles["TitleCustom"])
    
    # Crear una tabla para organizar el logo y el título en la misma línea
    title_logo_table = Table([[title, logo]], colWidths=[6.0 * inch, 1 * inch])
    title_logo_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (1, 0), 'TOP'),
    ]))
    
    return title_logo_table
    
def crear_pie_de_pagina():
    # Configuración de estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    
    # Pie de página enmarcado
    pie_de_pagina = Paragraph(
        """<b>Las cifras registradas en este formulario fueron tomadas fielmente del libro de Ingresos y Gastos.</b><br/>
        Firma del Representante Legal_________________________<br/>
        Firma del Auditor_________________________<br/>""",
        styles["Justify"]
    )

    # Añadir líneas horizontales y verticales en el pie de página
    footer_table = Table(
        [[pie_de_pagina]],
        colWidths=[7.5*inch]
    )
    footer_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    return footer_table
    
def crear_pie_de_pagina2():
    # Configuración de estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    
    # Pie de página con corrección de espacios
    pie_de_pagina2 = Paragraph(
        """<b>NOTA: Este espacio será diligenciado por la Organización Electoral</b><br/>
        Fecha de Presentación                         Ciudad:                       <br/>
        Total Folios: N/A                      <br/>
        Nombre de la persona que recibe el informe :                       <br/>
        Cargo:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Número de Cédula : ___<br/>""",
        styles["Justify"]
    )

    # Añadir líneas horizontales y verticales en el pie de página
    footer_table = Table(
        [[pie_de_pagina2]],
        colWidths=[7.5*inch]
    )
    footer_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    return footer_table
    
def crear_pie_de_pagina3():
    # Configuración de estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    
    # Pie de página con corrección de espacios
    pie_de_pagina3 = Paragraph(
        """Las cifras registradas en este formulario fueron tomadas fielmente del libro de Ingresos y Gastos.  <br/> 
         <br/> 
         <br/> 
         <br/> 
         _________________________________                           _________________________________  <br/>  
           Firma del Representante Legal                             Firma del Auditor Interno T.P  <br/> 
           <br/>
         <b>_____________________________________________________________________________________________</b <br/>  
           <b>NOTA: </b Para reportar los gastos en las casillas corespondientes, tener en cuenta el Articulo 11 de la Resolucion 3134 del 14 de <br/>
                    diciembre de 2018 "De conformidad con el principio de la transparencia, al tenor de lo previsto en el articulo 19 de la Ley 1475 de 2011,
                    <b>los partidos o movimientos politicos con personeria juridica declarados en oposicion, al momento de hacer la rendicion 
                    publica de cuentas, deberan desagregar del total de los ingresos y gastos, el monto correspondiente al componente de la 
                    financiacion adicional, por lo que deberan discriminar el destino dado a estos recursos..."</b y conforme con los principios.<br/>""",
        styles["Justify"]
    )

    # Añadir líneas horizontales y verticales en el pie de página
    footer_table = Table(
        [[pie_de_pagina3]],
        colWidths=[7.5*inch]
    )
    footer_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    return footer_table
  