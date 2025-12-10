from flask import send_file
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime
import json
from app.models import db, Proyecto, HistoricoCalculo, FormulaISO, ReferenciaNorma

FORMULAS_NOMBRES = {
    'ICP': 'Índice de Cumplimiento de Planificación',
    'NC': 'Índice de No Conformidades',
    'FR': 'Tasa de Fallos',
    'MTBF': 'Tiempo Medio Entre Fallos',
    'TPR': 'Tiempo Promedio de Respuesta',
    'IVC': 'Índice de Vulnerabilidades Críticas',
    'CC': 'Complejidad Ciclomática',
    'TS': 'Tasa de Sobrevivencia',
    'IC': 'Índice de Compatibilidad',
    'Ef': 'Eficiencia',
    'E': 'Exactitud',
    'Uso': 'Tasa de Uso de Recursos',
    'IM': 'Índice de Interoperabilidad Multiplataforma'
}

def get_color_interpretacion(nivel):
    """Retorna el color según el nivel de interpretación"""
    colores = {
        'excelente': colors.HexColor('#059669'),
        'bueno': colors.HexColor('#10b981'),
        'aceptable': colors.HexColor('#f59e0b'),
        'malo': colors.HexColor('#ef4444'),
        'critico': colors.HexColor('#dc2626')
    }
    return colores.get(nivel, colors.HexColor('#6b7280'))

def get_interpretacion_texto(nivel):
    """Retorna texto descriptivo según el nivel"""
    interpretaciones = {
        'excelente': 'Excelente - Cumple con los estándares de calidad máximos',
        'bueno': 'Bueno - Cumple adecuadamente con los estándares',
        'aceptable': 'Aceptable - Cumple de manera básica con los estándares',
        'malo': 'Malo - No cumple adecuadamente con los estándares',
        'critico': 'Crítico - Incumplimiento grave de los estándares'
    }
    return interpretaciones.get(nivel, 'Desconocido')

def generar_reporte_pdf(proyecto_id):
    """Genera un reporte PDF con datos del proyecto"""
    try:
        # Obtener datos del proyecto
        proyecto = Proyecto.query.get(proyecto_id)
        if not proyecto:
            return None, "Proyecto no encontrado"
        
        # Obtener histórico de cálculos
        historico = HistoricoCalculo.query.filter_by(proyecto_id=proyecto_id).all()
        
        # Crear PDF en memoria
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#047857'),
            spaceAfter=20,
            alignment=1
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#059669'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=8
        )
        
        # Contenido del PDF
        content = []
        
        # Título
        content.append(Paragraph("REPORTE DE PROYECTO ISO", title_style))
        content.append(Spacer(1, 0.2*inch))
        
        # Información del Proyecto
        content.append(Paragraph("INFORMACION DEL PROYECTO", heading_style))
        
        proyecto_data = [
            ['Nombre', proyecto.nombre or 'N/A'],
            ['URL Repositorio', (proyecto.url_github or 'N/A')[:50]],
            ['Total Commits', str(proyecto.total_commits or 0)],
            ['Lineas Codigo', str(proyecto.total_loc or 0)],
            ['Complejidad', str(round(proyecto.complejidad_ciclomatica or 1.0, 2))],
            ['Fecha Analisis', datetime.now().strftime('%d/%m/%Y %H:%M')]
        ]
        
        proyecto_table = Table(proyecto_data, colWidths=[2*inch, 4*inch])
        proyecto_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0fdf4')),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#047857')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1fae5')),
        ]))
        content.append(proyecto_table)
        content.append(Spacer(1, 0.3*inch))
        
        # Histórico de Cálculos
        if historico:
            content.append(Paragraph("HISTORICO DE CALCULOS", heading_style))
            
            historico_data = [['Formula', 'Nombre', 'Resultado', 'Interpretacion', 'Fecha']]
            
            for calculo in historico:
                nombre_formula = FORMULAS_NOMBRES.get(calculo.formula, 'Desconocida')
                
                # Obtener interpretación
                interpretacion_texto = 'N/A'
                if calculo.interpretacion_json:
                    try:
                        interp = json.loads(calculo.interpretacion_json) if isinstance(calculo.interpretacion_json, str) else calculo.interpretacion_json
                        nivel = interp.get('nivel', 'desconocido').lower()
                        interpretacion_texto = get_interpretacion_texto(nivel)
                    except:
                        pass
                
                # Truncar textos largos
                nombre_corto = nombre_formula[:18] + '..' if len(nombre_formula) > 20 else nombre_formula
                interp_corto = interpretacion_texto[:20] + '..' if len(interpretacion_texto) > 22 else interpretacion_texto
                
                historico_data.append([
                    calculo.formula,
                    nombre_corto,
                    f"{calculo.resultado:.2f}",
                    interp_corto,
                    datetime.fromisoformat(str(calculo.fecha_calculo)).strftime('%d/%m/%y')
                ])
            
            historico_table = Table(historico_data, colWidths=[0.8*inch, 1.4*inch, 0.9*inch, 1.2*inch, 0.8*inch])
            historico_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1fae5')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')]),
            ]))
            content.append(historico_table)
            content.append(Spacer(1, 0.3*inch))
            
            # Análisis
            content.append(PageBreak())
            content.append(Paragraph("ANALISIS E INTERPRETACION", heading_style))
            
            resultados = [c.resultado for c in historico]
            if resultados:
                promedio = sum(resultados) / len(resultados)
                maximo = max(resultados)
                minimo = min(resultados)
                
                analisis_data = [
                    ['Metrica', 'Valor'],
                    ['Numero Calculos', str(len(historico))],
                    ['Promedio', f"{promedio:.2f}"],
                    ['Maximo', f"{maximo:.2f}"],
                    ['Minimo', f"{minimo:.2f}"],
                ]
                
                analisis_table = Table(analisis_data, colWidths=[3*inch, 2*inch])
                analisis_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f0fdf4')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1fae5')),
                ]))
                content.append(analisis_table)
                content.append(Spacer(1, 0.2*inch))
            
            # Conclusiones
            content.append(Paragraph("CONCLUSIONES", heading_style))
            
            conclusion_text = f"""
            Se han realizado {len(historico)} calculos de formulas ISO para el proyecto {proyecto.nombre}.
            Los resultados muestran un analisis de las metricas de calidad segun estandares ISO/IEC.
            <br/><br/>
            Proximos Pasos:<br/>
            - Revisar resultados criticos para acciones correctivas<br/>
            - Implementar mejoras en areas de bajo desempeno<br/>
            - Realizar seguimiento continuo de metricas<br/>
            <br/>
            <i>Reporte generado por MetricISO el {datetime.now().strftime('%d/%m/%Y %H:%M')}</i>
            """
            
            content.append(Paragraph(conclusion_text, normal_style))
        else:
            content.append(Paragraph("No hay calculos registrados aun para este proyecto.", normal_style))
        
        # Generar PDF
        doc.build(content)
        pdf_buffer.seek(0)
        
        return pdf_buffer, None
    
    except Exception as e:
        import traceback
        print(f"Error generando PDF: {str(e)}")
        print(traceback.format_exc())
        return None, str(e)
