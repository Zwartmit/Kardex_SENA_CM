from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="datos.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Aquí puedes personalizar el contenido del PDF
    p.drawString(100, height - 50, "ID | Descripción | Fecha | Proyecto | Ficha")

    y = height - 70
    for p in object_list:
        p.drawString(100, y, f"{p.id} | {p.descripcion} | {p.fecha} | {p.proyecto} | {p.num_ficha}")
        y -= 15

    p.showPage()
    p.save()
    return response
