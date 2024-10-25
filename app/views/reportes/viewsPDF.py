import io
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from app.models import *

def generate_pdf_report(title_text, headers, data_rows, filename):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A3))
    elements = []

    styles = getSampleStyleSheet()
    style_title = styles['Title']
    style_normal = styles['Normal']

    centered_style = ParagraphStyle(
        name='CenteredStyle',
        parent=styles['Normal'],
        alignment=1 
    )

    image_path = 'app/views/reportes/logo_asuan.png'
    image = Image(image_path)
    image_width = 3 * inch  
    image_height = 1 * inch
    image.drawHeight = image_height
    image.drawWidth = image_width
    image.hAlign = 'CENTER'

    elements.append(image)
    elements.append(Spacer(1, 12))

    title = Paragraph(title_text, style_title)
    elements.append(title)

    fecha = datetime.now().strftime("%d/%m/%Y")
    date_paragraph = Paragraph(f"Fecha: {fecha}", centered_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 12))

    data = [headers] + data_rows

    col_widths = [2 * inch, 2 * inch, 2 * inch, 2 * inch, 2 * inch, 2 * inch]
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#034231")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}.pdf'
    return response

################################################## Elementos ##################################################
@login_required
@never_cache
def export_elementos_pdf(request):
    headers = ['ID', 'Elemento', 'Cantidad', 'Valor', 'Categoría', 'Marca', 'Presentación', 'Estado']
    data_rows = [
        [
            elemento.id, elemento.elemento, elemento.cantidad, elemento.valor,
            elemento.id_categoria.categoria, elemento.id_marca.marca, 
        ]
        for elemento in Elemento.objects.all()
    ]
    return generate_pdf_report("Reporte de elementos", headers, data_rows, "Reporte de elementos")