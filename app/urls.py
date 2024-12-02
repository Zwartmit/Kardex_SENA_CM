from django.urls import path
from app.views import *
from app.views.movimiento.views import *

app_name = 'app'
urlpatterns = [
    path('movimiento/listar/', MovimientoListView.as_view(), name='movimiento_lista'),
    path('movimiento/crear/', MovimientoCreateView.as_view(), name='movimiento_crear'),
    # path('movimiento/editar/<int:pk>/', MovimientoUpdateView.as_view(), name='movimiento_editar'),
    # path('movimiento/eliminar/<int:pk>/', MovimientoDeleteView.as_view(), name='movimiento_eliminar'),
]
