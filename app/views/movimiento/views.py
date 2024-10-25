from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from app.models import Movimiento
from app.forms import MovimientoForm

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
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        success_url = reverse('app:movimiento_crear') + '?created=True'
        return redirect(success_url)

###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoUpdateView(UpdateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'movimiento/crear.html'
    success_url = reverse_lazy('app:movimiento_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar movimiento'
        context['entidad'] = 'Editar movimiento'
        context['error'] = 'Error al editar el movimiento.'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        success_url = reverse('app:movimiento_crear') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoDeleteView(DeleteView):
    model = Movimiento
    template_name = 'movimiento/eliminar.html'
    success_url = reverse_lazy('app:movimiento_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar movimiento'
        context['entidad'] = 'Eliminar movimiento'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'Movimiento eliminado con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar el movimiento.'})
