from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Requerido. Máximo 30 caracteres.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Requerido. Máximo 30 caracteres.')
    email = forms.EmailField(max_length=254, required=True, help_text='Requerido. Ingrese una dirección de correo electrónico válida.')
    phone = forms.CharField(max_length=15, required=True, help_text='Requerido. Máximo 15 caracteres.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')