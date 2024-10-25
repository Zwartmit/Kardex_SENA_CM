from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from datetime import datetime
from app.models import *

################################################## Elementos ##################################################
@login_required
@never_cache
def export_elementos_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte de elementos"

    bold_font = Font(bold=True)
    center_alignment = Alignment(horizontal="center", vertical="center")
    green_fill = PatternFill(start_color="034231", end_color="034231", fill_type="solid")
    white_font = Font(color="FFFFFF")
    medium_border = Border(left=Side(style='medium'), 
                         right=Side(style='medium'), 
                         top=Side(style='medium'), 
                         bottom=Side(style='medium'))

    column_width = 20  
    for col in range(2, 10): 
        column_letter = get_column_letter(col)
        ws.column_dimensions[column_letter].width = column_width

    ws.row_dimensions[2].height = 38 
    ws.row_dimensions[3].height = 23  
    ws.row_dimensions[5].height = 20

    img = Image('app/views/reportes/logo_asuan.png') 
    img.width = 140  
    img.height = 50  
    ws.add_image(img, 'E2')
    ws.merge_cells('B2:I2')  
    ws['B2'].alignment = center_alignment
    ws['B2'].border = medium_border

    ws.merge_cells('B2:I2')
    ws['B2'].alignment = center_alignment
    ws.merge_cells('B3:I3')
    ws['B3'] = "Reporte de elementos"
    ws['B3'].font = Font(size=14, bold=True)
    ws['B3'].alignment = center_alignment
    ws['B3'].border = medium_border
    for col in range(3, 10):
        ws.cell(row=3, column=col).border = medium_border

    ws.merge_cells('B4:I4')
    fecha = datetime.now().strftime("%d/%m/%Y")
    ws['B4'] = f"Fecha: {fecha}"
    ws['B4'].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws['B4'].border = medium_border
    for col in range(3, 10):
        ws.cell(row=4, column=col).border = medium_border

    headers = ['ID', 'Elemento', 'Cantidad', 'Valor', 'Estado', 'Categoría', 'Marca', 'Presentación']
    for col_num, header in enumerate(headers, 2):
        cell = ws.cell(row=5, column=col_num)
        cell.value = header
        cell.fill = green_fill
        cell.font = white_font
        cell.alignment = center_alignment
        cell.border = medium_border

    elementos = Elemento.objects.all()
    for row_num, elemento in enumerate(elementos, 6):  
        ws.cell(row=row_num, column=2, value=elemento.id)
        ws.cell(row=row_num, column=3, value=elemento.elemento)
        ws.cell(row=row_num, column=4, value=elemento.cantidad)
        ws.cell(row=row_num, column=5, value=elemento.valor)
        ws.cell(row=row_num, column=6, value='Activo' if elemento.estado else 'Inactivo')
        ws.cell(row=row_num, column=7, value=elemento.id_categoria.categoria)
        ws.cell(row=row_num, column=8, value=elemento.id_marca.marca) 
        ws.cell(row=row_num, column=9, value=f"{elemento.id_presentacion.presentacion} {elemento.id_presentacion.unidad_medida}") 
        
        for col_num in range(2, 10): 
            cell = ws.cell(row=row_num, column=col_num)
            cell.alignment = center_alignment
            cell.border = medium_border

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte de elementos.xlsx'
    wb.save(response)
    return response