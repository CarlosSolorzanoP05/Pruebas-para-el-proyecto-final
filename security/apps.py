from django.apps import AppConfig


class SecurityConfig(AppConfig):
    name = 'security'
<<<<<<< HEAD

    def ready(self):
        # Registra las señales (post_save de User -> Profile + rol
        # "Usuario" por defecto). Ver security/signals.py.
        import security.signals  # noqa: F401
=======
>>>>>>> 72f4066fa5748c0921f8bba8fa79ee453233c999
