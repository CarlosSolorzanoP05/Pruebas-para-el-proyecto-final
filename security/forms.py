from django import forms
from django.contrib.auth.models import User, Group

class UserRegistrationForm(forms.ModelForm):
    """Formulario minimalista para registrar nuevos usuarios con contraseña oculta"""
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}), label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

class UserRoleForm(forms.Form):
    """Formulario dinámico para asignarle un Rol (Grupo de Django) a un usuario"""
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        label="Seleccionar Usuario"
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        label="Asignar Rol / Grupo"
    )