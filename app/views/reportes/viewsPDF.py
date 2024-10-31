import io
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from app.models import Movimiento, DetalleMovimiento

@login_required
@never_cache
def exportar_pdf(request):
    title_text = "Reporte de movimientos"
    headers = ["ID", "Descripción", "Elementos", "Fecha", "Proyecto", "Ficha"]
    
    object_list = Movimiento.objects.all()
    data_rows = []

    for movimiento in object_list:
        elementos = DetalleMovimiento.objects.filter(movimiento=movimiento)
        
        detalles = []
        for detalle in elementos:
            detalles.append([detalle.elemento.item, detalle.cantidad])
        
        sub_table = Table(detalles, colWidths=[4 * inch, 1 * inch])
        sub_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        data_rows.append([
            movimiento.id,
            movimiento.descripcion,
            sub_table,
            movimiento.fecha.strftime("%d/%m/%Y"),
            movimiento.proyecto,
            movimiento.num_ficha
        ])

    filename = "Reporte de movimientos"
    return generate_pdf_report(title_text, headers, data_rows, filename)

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

    title = Paragraph(title_text, style_title)
    elements.append(title)

    data = [headers] + [[Paragraph(str(cell), centered_style) if not isinstance(cell, Table) else cell for cell in row] for row in data_rows]

    col_widths = [1 * inch, 2 * inch, None, 1 * inch, 1 * inch, 1 * inch]
    table = Table(data, colWidths=col_widths)
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#04644B")),
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
