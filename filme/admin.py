from django.contrib import admin
from .models import Filme, Episodio, Usuario  # . simboliza que o arquivo importado está no mesmo arquivo desse
from django.contrib.auth.admin import UserAdmin


# aparecer campo personalizado no admin sobre filmes_vistos (cada tupla é uma sessão (div) no admin)
campos = list(UserAdmin.fieldsets)
campos.append(
    ("Histórico", {"fields": ("filmes_vistos",)})
)
UserAdmin.fieldsets = tuple(campos)

# Register your models here.
admin.site.register(Filme)  # registrar classe filme no espaço do admin
admin.site.register(Episodio)  # registrar classe episodio no espaço do admin
admin.site.register(Usuario, UserAdmin)  # reconhecer usuario criado em models como usuario padrao