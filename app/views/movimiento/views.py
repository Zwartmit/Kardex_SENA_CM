from pyexpat.errors import messages
from django.forms import modelformset_factory
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
    context_object_name = 'movimientos'  # Definimos el nombre de la variable que pasará el listado de movimientos al contexto
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Añadimos información extra al contexto
        context['titulo'] = 'Listado de movimientos'
        context['entidad'] = 'Listado de movimientos'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        context['crear_url'] = reverse_lazy('app:movimiento_crear')

        # Añadimos los elementos asociados a cada movimiento
        movimientos_con_elementos = []
        for movimiento in context['movimientos']:
            elementos = movimiento.elementos.all()  # Obtener los elementos relacionados con el movimiento
            movimientos_con_elementos.append({
                'movimiento': movimiento,
                'elementos': elementos
            })
        
        # Pasamos los movimientos con sus elementos al contexto
        context['movimientos_con_elementos'] = movimientos_con_elementos

        return context

###### CREAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoCreateView(CreateView):
    template_name = 'movimiento/crear.html'
    form_class = MovimientoForm

    def get(self, request, *args, **kwargs):
        form = MovimientoForm()
        formset = ElementoFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset, 'titulo': 'Registrar movimiento'})

    def post(self, request, *args, **kwargs):
        form = MovimientoForm(request.POST)
        formset = ElementoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Guardar el objeto Movimiento
            movimiento = form.save()

            # Guardamos los elementos, asociándolos con el movimiento
            elementos = formset.save(commit=False)
            for elemento in elementos:
                elemento.movimiento = movimiento
                elemento.save()

            # Redirigimos a la lista de movimientos con un mensaje de éxito
            return redirect(f"{reverse_lazy('app:movimiento_lista')}?created=True")

        # Si el formulario no es válido, mostramos el formulario con los errores
        return render(request, self.template_name, {'form': form, 'formset': formset, 'titulo': 'Registrar movimiento'})
    
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