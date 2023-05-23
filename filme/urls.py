'''
sempre construir tres coisas nas urls:
1. url (link onde a página vai aparecer
2. uma view (o que vai acontecer quando o usuário entrar nesse link
3. template (parte visual do que será exibido)
'''
from django.urls import path, reverse_lazy
from .views import Homepage, Homefilmes, Detalhesfilme, Pesquisafilme, Editarperfil, Criarconta
from django.contrib.auth import views as auth_view  # django já tem view de login pronta. dar nome diferente, pois já tem var com esse nome.


# definir o nome do aplicativo
app_name = "filme"


# se for Function based view, passar função sem parêntesis no final, se for Class Based View passar com parêntesis
urlpatterns = [
    path("", Homepage.as_view(), name="homepage"),
    path("filmes/", Homefilmes.as_view(), name="homefilmes"),
    path("filmes/<int:pk>", Detalhesfilme.as_view(), name="detalhesfilme"),
    path("pesquisa/", Pesquisafilme.as_view(), name="pesquisafilme"),
    path("login/", auth_view.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_view.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("editarperfil/<int:pk>", Editarperfil.as_view(), name="editarperfil"),
    path("criarconta/", Criarconta.as_view(), name="criarconta"),
    path("mudarsenha/", auth_view.PasswordChangeView.as_view(template_name="editarperfil.html", success_url=reverse_lazy("filme:homefilmes")), name="mudarsenha")
]
# LoginView já repassa para o HTML, uma variavel form -> django já vem linkado com bootstrap para edição visual de forms (fazer: pip install django-crispy-forms)
