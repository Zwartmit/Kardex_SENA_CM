from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import render
from app.models import *
from app.forms import *

@method_decorator(never_cache, name='dispatch')
def lista_movimientos(request):
    nombre = {
        'titulo': 'Registro de movimientos realizados',
        'movimientos': Movimiento.objects.all(),
        'elementos': DetalleMovimiento.objects.all()
    }
    return render(request, 'movimiento/listar.html', nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoListView(ListView):
    model = Movimiento
    template_name = 'movimiento/listar.html'
    context_object_name = 'movimientos'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Movimientos realizados'
        context['entidad'] = 'Movimientos realizados'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        context['crear_url'] = reverse_lazy('app:movimiento_crear')

        movimientos_con_elementos = []
        for movimiento in context['movimientos']:
            detalles = movimiento.detalles.all()  
            movimientos_con_elementos.append({
                'movimiento': movimiento,
                'elementos': detalles 
            })

        context['movimientos_con_elementos'] = movimientos_con_elementos
        return context

###### CREAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoCreateView(CreateView):
    template_name = 'movimiento/crear.html'
    form_class = MovimientoForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = DetalleMovimientoFormSet()
        context = {
            'form': form,
            'formset': formset,
            'titulo': 'Registrar nuevo movimiento',
            'entidad': 'Registrar nuevo movimiento',
            'listar_url': reverse_lazy('app:movimiento_lista'),
            'crear_url': reverse_lazy('app:movimiento_crear'),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleMovimientoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                movimiento = form.save()

                detalles = formset.save(commit=False)
                for detalle in detalles:
                    detalle.movimiento = movimiento 
                    detalle.save()

                return JsonResponse({'success': True, 'message': 'Movimiento registrado correctamente.'})

            except Exception as e:
                print(f"Error al guardar el movimiento: {e}")
                return JsonResponse({'success': False, 'errors': str(e)})

        else:
            errors = {
                'form_errors': form.errors.as_json(),
                'formset_errors': formset.errors.as_json(),
            }
            return JsonResponse({'success': False, 'errors': errors})
        
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