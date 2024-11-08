from django.urls import path
from app.views import *
from app.views.elemento.views import *
from app.views.reportes.views import exportar_pdf, exportar_excel
from app.views.movimiento.views import *

app_name = 'app'
urlpatterns = [
    ### CRUD ELEMENTOS ###
    path('elemento/listar/', ElementoListView.as_view(), name='elemento_lista'),
    path('elemento/crear/', ElementoCreateView.as_view(), name='elemento_crear'),
    path('elemento/editar/<int:pk>/', ElementoUpdateView.as_view(), name='elemento_editar'),
    path('elemento/eliminar/<int:pk>/', ElementoDeleteView.as_view(), name='elemento_eliminar'),

    ### CRUD MOVIMIENTOS ###
    path('movimiento/listar/', MovimientoListView.as_view(), name='movimiento_lista'),
    path('movimiento/crear/', MovimientoCreateView.as_view(), name='movimiento_crear'),
    # path('movimiento/editar/<int:pk>/', MovimientoUpdateView.as_view(), name='movimiento_editar'),
    # path('movimiento/eliminar/<int:pk>/', MovimientoDeleteView.as_view(), name='movimiento_eliminar'),

    ### REPORTES ###
    path('export/pdf/', exportar_pdf, name='exportar_pdf'),
    path('export/excel/', exportar_excel, name='exportar_excel'),
]
