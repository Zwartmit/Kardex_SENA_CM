from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from app.models import Elemento
from app.forms import ElementoForm

@method_decorator(never_cache, name='dispatch')
def lista_elementos(request):
    nombre = {
        'titulo': 'Listado de elementos',
        'elementos': Elemento.objects.all()
    }
    return render(request, 'elemento/listar.html',nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class ElementoListView(ListView):
    model = Elemento
    template_name = 'elemento/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de elementos'
        context['entidad'] = 'Listado de elementos'
        context['listar_url'] = reverse_lazy('app:elemento_lista')
        context['crear_url'] = reverse_lazy('app:elemento_crear')
        return context

###### CREAR ######

@method_decorator(never_cache, name='dispatch')
class ElementoCreateView(CreateView):
    model = Elemento
    form_class = ElementoForm
    template_name = 'elemento/crear.html'
    success_url = reverse_lazy('app:elemento_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar elemento'
        context['entidad'] = 'Registrar elemento'
        context['error'] = 'Este elemento ya está registrado.'
        context['listar_url'] = reverse_lazy('app:elemento_crear')
        context['crear_url'] = reverse_lazy('app:elemento_lista')
        return context
    
    def form_valid(self, form):
        elemento = form.cleaned_data.get('elemento')
        if elemento is not None:
            elemento = elemento.lower()
            
            if Elemento.objects.filter(elemento_exact=elemento).exists():
                form.add_error('elemento', 'Ya existe un elemento registrado con ese nombre.')
                return self.form_invalid(form)

        response = super().form_valid(form)
        success_url = reverse('app:elemento_crear') + '?created=True'
        return redirect(success_url)
    
###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class ElementoUpdateView(UpdateView):
    model = Elemento
    form_class = ElementoForm
    template_name = 'elemento/crear.html'
    success_url = reverse_lazy('app:elemento_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar elemento'
        context['entidad'] = 'Editar elemento'
        context['error'] = 'Este elemento ya está registrado.'
        context['listar_url'] = reverse_lazy('app:elemento_lista')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        success_url = reverse('app:elemento_crear') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class ElementoDeleteView(DeleteView):
    model = Elemento
    template_name = 'elemento/eliminar.html'
    success_url = reverse_lazy('app:elemento_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar elemento'
        context['entidad'] = 'Eliminar elemento'
        context['listar_url'] = reverse_lazy('app:elemento_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'Elemento eliminado con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar el elemento.'})