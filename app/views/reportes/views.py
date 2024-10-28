from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from app.forms import ReporteForm
from django.shortcuts import render
from app.views.reportes.viewsExcel import *
from app.views.reportes.viewsPDF import *
from django.utils.dateparse import parse_date

def get(self, request, *args, **kwargs):
    
    contexto = {
        'titulo': 'Generar reportes',
    }
    return render(request, 'reportes.html', contexto)

@login_required
@never_cache
def reporte_selector(request):
    
    if request.method == 'POST':
        tipo_reporte = request.POST.get('tipo_reporte')
        formato = request.POST.get('formato')

        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        fecha_inicio = parse_date(fecha_inicio) if fecha_inicio else None
        fecha_fin = parse_date(fecha_fin) if fecha_fin else None

        print("Fecha de inicio:", fecha_inicio)
        print("Fecha de fin:", fecha_fin)
        
        if formato == 'excel':
            if tipo_reporte == 'producto':
                return export_elementos_excel(request)
        elif formato == 'pdf':
            if tipo_reporte == 'producto':
                return export_elementos_pdf(request)
    else:
        form = ReporteForm() 

    contexto = {
        'titulo': 'Generar reportes',
        'entidad': 'Generar reportes'
    }
    
    return render(request, 'reportes.html', contexto)

