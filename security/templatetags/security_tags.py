from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Filtro para verificar en los templates HTML si un usuario pertenece a un grupo.
    Uso en el HTML: {% if request.user|has_group:"Administrador" %}
    """
    if user.is_superuser:
        return True
    return user.groups.filter(name=group_name).exists()