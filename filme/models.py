from django.db import models
from django.utils import timezone  # será usado para salvar a data de criação do filme
from django.contrib.auth.models import AbstractUser  # importar usuário padrão do django
# Create your models here.

# (armazenar_banco_dados, mostrar_usuario)
LISTA_CATEGORIAS = (
    ("analises", "Análises"),
    ("programacao", "Programação"),
    ("apresentacao", "Apresentação"),
    ("outros", "Outros")
)

# criar o filme
class Filme(models.Model):  # criar nova tabela no banco de dados (sempre que fizer isso executar: python manage.py makemigrations e em seguida python manage.py migrate)
    def __str__(self):  # aparecer o nome do título no print da classe
        return self.titulo

    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to="thumb_filmes")  # fazer pip install pillow para mexer com imagens
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
    # .now sem parenteses pq se não os horários seriam sempre os do momento em que o usuário está assistindo o filme
    data_criacao = models.DateTimeField(default=timezone.now)
    # para aparecer no adm: em admin.py importar essa classe

# criar os episódios
class Episodio(models.Model):
    # criar chave estrangeira para conectar com a tabela Filme -> .Manytomanyfields() permite que varios episodios criem relações com varios filmes
    filme = models.ForeignKey("Filme", related_name="episodios", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self):  # aparecer o nome do título no print da classe
        return self.titulo

'''
se já souber logo no inicio que o usuario será diferente, já criar essa classe para o django já iniciar com a tabela
de usuarios correta.
caso contrario, duas opções:
1. deletar o banco de dados atual e todos os arquivos em migrations menos o __init__.py (mas perde todos os usuários e filmes já cadastrados)
    1.1. rodar: python manage.py makemigrations (recriar banco de dados)
    1.2. python manage.py migrate
    1.3. python manage.py createsuperuser (para recriar usuario do admin)
2. Ou comentar a linha AUTH_USER_MODEL em setttings e rodar os comandos:
    2.1. python manage.py migrate auth zero
    2.2. descomentar AUTH_USER_MODEL e rodar: python manage.py migrate auth
'''
# criar o usuário (poderia ser em um app próprio, mas como o site do projeto gira entorno dos filmes, optou-se por criar dentro de Filmes
class Usuario(AbstractUser):  # django já tem um usuario, pode-se usar o padrão dele ou acrescentar informações como vai ser o caso aqui
    filmes_vistos = models.ManyToManyField("Filme")  # filmes podem ter sido assistidos por varios usuarios e usuarios podem ter visto varios filmes

