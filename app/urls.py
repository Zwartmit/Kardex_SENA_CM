from django.urls import path
from app.views import *
from app.views.movimiento.views import *
from app.views.elemento.views import *
from app.views.programa.views import *

app_name = 'app'
urlpatterns = [
    path('elemento/listar/', ElementoListView.as_view(), name='elemento_lista'),
    path('elemento/crear/', ElementoCreateView.as_view(), name='elemento_crear'),
    path('elemento/editar/<int:pk>/', ElementoUpdateView.as_view(), name='elemento_editar'),
    path('elemento/eliminar/<int:pk>/', ElementoDeleteView.as_view(), name='elemento_eliminar'),
    
    path('programa/listar/', ProgramaListView.as_view(), name='programa_lista'),
    path('programa/crear/', ProgramaCreateView.as_view(), name='programa_crear'),
    path('programa/editar/<int:pk>/', ProgramaUpdateView.as_view(), name='programa_editar'),
    path('programa/eliminar/<int:pk>/', ProgramaDeleteView.as_view(), name='programa_eliminar'),

    path('movimiento/listar/', MovimientoListView.as_view(), name='movimiento_lista'),
    path('movimiento/crear/', MovimientoCreateView.as_view(), name='movimiento_crear'),
]
