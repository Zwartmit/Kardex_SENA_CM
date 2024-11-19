from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from app.models import *
from app.forms import *

@method_decorator(never_cache, name='dispatch')
def lista_movimientos(request):
    nombre = {
        'titulo': 'Registro de movimientos realizados',
        'movimientos': Movimiento.objects.all()
    }
    return render(request, 'movimiento/listar.html', nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoListView(ListView):
    model = Movimiento
    template_name = 'movimiento/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de movimientos'
        context['entidad'] = 'Listado de movimientos'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        context['crear_url'] = reverse_lazy('app:movimiento_crear')

        # Obtener los elementos relacionados a los movimientos
        context['elementos'] = Elemento.objects.all()  # O ajusta la consulta según tu lógica
        return context

###### CREAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoCreateView(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'movimiento/crear.html'
    success_url = reverse_lazy('app:movimiento_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar movimiento'
        context['entidad'] = 'Registrar movimiento'
        context['error'] = 'Error al registrar el movimiento.'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        context['elementos'] = Elemento.objects.all()  # Lista de elementos opcional
        context['detalle_formset'] = DetalleMovimientoForm(self.request.POST or None, instance=self.object)
        context['elemento_form'] = ElementoForm()  # Formulario para el modelo Elemento
        return context

    def form_valid(self, form):
        # Guardar el objeto Movimiento
        movimiento = form.save()

        # Manejar el formulario de DetalleMovimiento si está incluido en el request
        detalle_form = DetalleMovimientoForm(self.request.POST)
        if detalle_form.is_valid():
            detalle = detalle_form.save(commit=False)
            detalle.movimiento = movimiento  # Asocia el detalle al movimiento creado
            detalle.save()

        # Manejar el formulario de Elemento si es necesario (opcional)
        elemento_form = ElementoForm(self.request.POST)
        if elemento_form.is_valid():
            elemento = elemento_form.save()

        return redirect(f"{self.success_url}?created=True")

# ###### EDITAR ######

# @method_decorator(never_cache, name='dispatch')
# class MovimientoUpdateView(UpdateView):
#     model = Movimiento
#     form_class = MovimientoForm
#     template_name = 'movimiento/crear.html'
#     success_url = reverse_lazy('app:movimiento_lista')

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = 'Editar movimiento'
#         context['entidad'] = 'Editar movimiento'
#         context['error'] = 'Error al editar el movimiento.'
#         context['listar_url'] = reverse_lazy('app:movimiento_lista')
#         return context

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         success_url = reverse('app:movimiento_crear') + '?updated=True'
#         return redirect(success_url)

# ###### ELIMINAR ######

# @method_decorator(never_cache, name='dispatch')
# class MovimientoDeleteView(DeleteView):
#     model = Movimiento
#     template_name = 'movimiento/eliminar.html'
#     success_url = reverse_lazy('app:movimiento_lista')

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = 'Eliminar movimiento'
#         context['entidad'] = 'Eliminar movimiento'
#         context['listar_url'] = reverse_lazy('app:movimiento_lista')
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         try:
#             self.object.delete()
#             return JsonResponse({'success': True, 'message': 'Movimiento eliminado con éxito.'})
#         except ProtectedError:
#             return JsonResponse({'success': False, 'message': 'No se puede eliminar el movimiento.'})