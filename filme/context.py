'''
esse arquivo pega variáveis personalizadas para repassar ao views, que passarão a ser globais
'''

from .models import Filme

# adicionar em settings.py na parte de templates -> context_processors
def lista_filmes_recentes(request):

    # botar um - na frente ordena em ordem decrescente
    lista_filmes = Filme.objects.all().order_by("-data_criacao")[0:8]
    if lista_filmes:
        filme_destaque = lista_filmes[0]
    else:
        filme_destaque = None
    return {"lista_filmes_recentes": lista_filmes, "filme_destaque": filme_destaque}  # sempre retornar um dicionário de um item só


def lista_filmes_emalta(request):
    lista_filmes = Filme.objects.all().order_by("-visualizacoes")[0:8]
    return {"lista_filmes_emalta": lista_filmes}
