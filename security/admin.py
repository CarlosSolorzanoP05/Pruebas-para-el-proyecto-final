from django.contrib import admin
<<<<<<< HEAD
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'cedula', 'saldo_efectivo', 'saldo_tarjeta', 'dinero', 'rango']
    search_fields = ['user__username', 'user__email', 'cedula']
=======
>>>>>>> 72f4066fa5748c0921f8bba8fa79ee453233c999

# Register your models here.
