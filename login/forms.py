from django import forms
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django_recaptcha.fields import ReCaptchaField

UserModel = get_user_model()

class UserEmailForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico no está registrado.')
        return email
    
    
class PasswordResetForm(forms.Form):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus'] = True

    email = forms.EmailField(label='Correo electrónico', required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No hay ningún usuario registrado con este correo electrónico.")
        return email
    

class SetPasswordForm(DjangoSetPasswordForm):
    def init(self, user, *args, **kwargs):
        self.user = user
        super().init(user, *args, **kwargs)

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user

class CustomLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
 
class LoginForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())