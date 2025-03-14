from django.shortcuts import render, redirect
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import RedirectView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from .forms import PasswordResetForm, SetPasswordForm
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from .forms import CustomLoginForm 

UserModel = get_user_model()

class LoginFormView(LoginView):
    template_name = "login.html"
    authentication_form = CustomLoginForm 

    def form_invalid(self, form):
        captcha_error = "captcha" in form.errors
        print("Captcha Error:", captcha_error)  
        return self.render_to_response(self.get_context_data(form=form, captcha_error=captcha_error))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Iniciar Sesión"
        context["captcha_error"] = kwargs.get("captcha_error", False)
        return context
    
class logoutredirect(RedirectView):
    pattern_name="login"
    
    def dispatch(self, request,*kwargs ):
        logout(request)
        return super().dispatch(request, *kwargs)
    
class PasswordResetView(FormView):
    template_name = "register/password_reset_form.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Restablecer Contraseña"
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            messages.success(self.request, 'Si ese correo está registrado, se ha enviado un correo de restablecimiento de contraseña.')
            return super().form_valid(form)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = self.request.build_absolute_uri(
            reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )


        subject = 'Restablecer contraseña'
        message = render_to_string('register/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
        })

        send_mail(subject, message, None, [email], html_message=message)

        messages.success(self.request, 'Se ha enviado un correo de restablecimiento de contraseña.')
        return super().form_valid(form)
    
class PasswordResetConfirmView(FormView):
    template_name = 'register/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

    def get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.user = self.get_user(self.kwargs['uidb64'])
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Contraseña restablecida con éxito.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validlink'] = self.user is not None and default_token_generator.check_token(self.user, self.kwargs['token'])
        if not context['validlink']:
            context['title'] = 'Restablecimiento de contraseña fallido'
        return context

class PasswordResetCompleteView(TemplateView):
    template_name = "register/password_reset_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Restablecimiento Completo"
        return context