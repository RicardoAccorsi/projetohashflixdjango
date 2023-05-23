from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "filme"

    # para criar admin após o deploy
    '''def ready(self):

        from .models import Usuario
        import os

        email_admin = os.getenv("EMAIL_ADMIN")
        senha_admin = os.getenv("SENHA_ADMIN")

        usuarios = Usuario.objects.filter(email=email_admin)

        if not usuarios:
            Usuario.objects.create_superuser(username="admin", email=email_admin, password=senha_admin, is_active=True, is_staff=True)'''