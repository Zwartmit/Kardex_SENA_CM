from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from app.models import Programa
from app.forms import ProgramaForm

@method_decorator(never_cache, name='dispatch')
def lista_programas(request):
    nombre = {
        'titulo': 'Programas de formación',
        'programas': Programa.objects.all()
    }
    return render(request, 'programa/listar.html', nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class ProgramaListView(ListView):
    model = Programa
    template_name = 'programa/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Programas de formación'
        context['entidad'] = 'Programas de formación'
        context['listar_url'] = reverse_lazy('app:programa_lista')
        context['crear_url'] = reverse_lazy('app:programa_crear')
        return context

###### CREAR ######

@method_decorator(never_cache, name='dispatch')
class ProgramaCreateView(CreateView):
    model = Programa
    form_class = ProgramaForm
    template_name = 'programa/crear.html'
    success_url = reverse_lazy('app:programa_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar programa'
        context['entidad'] = 'Registrar programa'
        context['error'] = 'Este programa ya está registrado.'
        context['listar_url'] = reverse_lazy('app:programa_crear')
        context['crear_url'] = reverse_lazy('app:programa_lista')
        return context
    
    def form_valid(self, form):
        programa = form.cleaned_data.get('programa')
        if programa is not None:
            programa = programa.strip().lower().capitalize()
            
            if Programa.objects.filter(programa=programa).exists():
                form.add_error('programa', 'Ya existe un programa registrado con ese nombre.')
                return self.form_invalid(form)

        self.object = form.save(commit=False)
        self.object.programa = programa
        self.object.save()

        success_url = reverse('app:programa_crear') + '?created=True'
        return redirect(success_url)
    
###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class ProgramaUpdateView(UpdateView):
    model = Programa
    form_class = ProgramaForm
    template_name = 'programa/crear.html'
    success_url = reverse_lazy('app:programa_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar programa'
        context['entidad'] = 'Editar programa'
        context['error'] = 'Este programa ya está registrado.'
        context['listar_url'] = reverse_lazy('app:programa_lista')
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.programa = self.object.programa.strip().lower().capitalize()
        self.object.save()
        success_url = reverse('app:programa_crear') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class ProgramaDeleteView(DeleteView):
    model = Programa
    template_name = 'programa/eliminar.html'
    success_url = reverse_lazy('app:programa_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar programa'
        context['entidad'] = 'Eliminar programa'
        context['listar_url'] = reverse_lazy('app:programa_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'Programa eliminado con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar el programa.'})
