import openpyxl
from django.http import HttpResponse

def exportar_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="datos.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos"

    # Encabezados
    ws.append(["ID", "Descripción", "Fecha", "Proyecto", "Ficha"])

    # Filas de datos
    for p in object_list:
        ws.append([p.id, p.descripcion, p.fecha, p.proyecto, p.num_ficha])

    wb.save(response)
    return response
