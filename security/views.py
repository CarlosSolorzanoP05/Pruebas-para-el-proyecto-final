from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.contrib import messages
from shared.mixins import GroupRequiredMixin  # Importamos el mixin que creamos en shared/
from .forms import UserRegistrationForm, UserRoleForm,GroupCreateForm
class UserCreateView(GroupRequiredMixin, CreateView):
    """Vista para que el Admin registre nuevos trabajadores"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'security/user_form.html'
    success_url = reverse_lazy('user_list')
    group_required = ['Administrador']  # Solo el Admin puede crear usuarios

    def form_valid(self, form):
        # Guardamos el usuario cifrando la contraseña automáticamente
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, f"Usuario {user.username} creado con éxito.")
        return super().form_valid(form)


class UserListView(GroupRequiredMixin, ListView):
    """Vista para listar todos los usuarios y ver qué rol tienen actualmente"""
    model = User
    template_name = 'security/user_list.html'
    context_object_name = 'users'
    group_required = ['Administrador']  # Solo accesible por el Administrador


class UserRoleUpdateView(GroupRequiredMixin, FormView):
    """Vista para asignarle o cambiarle el Grupo/Rol a un usuario de forma dinámica"""
    form_class = UserRoleForm
    template_name = 'security/role_form.html'
    success_url = reverse_lazy('user_list')
    group_required = ['Administrador']  # Protegido a nivel de servidor

    def form_valid(self, form):
        user = form.cleaned_data['user']
        group = form.cleaned_data['group']

        # Limpiamos los grupos anteriores para que no tenga múltiples roles conflictivos
        user.groups.clear()
        # Asignamos el nuevo rol/grupo
        user.add_to_class('groups', group) if hasattr(user, 'add_to_class') else user.groups.add(group)
        
        messages.success(self.request, f"Se asignó el rol '{group.name}' al usuario {user.username} correctamente.")
        return super().form_valid(form)
class GroupCreateView(GroupRequiredMixin, CreateView):
    """Vista exclusiva para que el Admin cree nuevos roles desde la interfaz web"""
    model = Group
    form_class = GroupCreateForm
    template_name = 'security/group_form.html'
    success_url = reverse_lazy('user_list') # Redirige a la lista de usuarios al terminar
    group_required = ['Administrador'] # Protección estricta a nivel de servidor

    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f"El nuevo rol '{group.name}' fue creado exitosamente en el sistema.")
        return super().form_valid(form)