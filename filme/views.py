from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin  # para tornar login necessario em algumas páginas
from .forms import Criarcontaform, Formhome


# classes tendem a já ter mais coisas prontas pelo django, com functions fica mais a cargo do usuário de elaborar toda a lógica

# Create your views here. Exemplo de Function based view
'''def homepage(request):  # request informa o tipo de requisição sendo feito no site  (function based views: FBV)
    return render(request, "homepage.html")'''

class Homepage(FormView):  # FormView sempre precisa de um success url
    template_name = "homepage.html"
    form_class = Formhome

    def get_success_url(self):
        email = self.request.POST.get("email")  # pegar email preenchido no campo
        usuarios = Usuario.objects.filter(email=email)  # pegar usuarios com esse email no banco de dados

        if usuarios:  # se tiver, redireciona para email
            return reverse("filme:login")
        else:  # se n, redireciona para criar conta
            return reverse("filme:criarconta")


    # mudar dinamicamente para qual pagina o botao na logo redireciona
    def get(self, request, *args, **kwargs):  # espera um redirecionamento/carregamento de página
        if request.user.is_authenticated:  # refireciona para homefilmes
            return redirect("filme:homefilmes")  # ("app_name:nome_classe")
        else:  # redireciona para a homepage
            return super().get(request, *args, **kwargs)

# exemplo de Function based views
'''def homefilmes(request):  # 3 parametro é um contexto à página
    context = {}
    lista_filmes = Filme.objects.all()
    context["lista_filmes"] = lista_filmes
    return render(request, "homefilmes.html", context)'''

# vai repassar uma lista de itens
class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"

    # essa linha ja faz tudo que as 15 a 17 fazem, mas retorna com o nome object_list
    model = Filme


# essa view vai criar várias páginas, uma para cada item da base de dados
class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"

    # essa linha retorna apenas um item da base de dados, com o nome object
    model = Filme


    # mudar função get para contabilizar visualizações
    def get(self, request, *args, **kwargs):

        # descobrir qual filme está acessando
        filme = self.get_object()

        # somar 1 nas visualizacoes desse filme
        filme.visualizacoes += 1

        # salvar alterações no banco de dados
        filme.save()

        # adicionar filme a filmes_vistos do usuario
        usuario = request.user  # pegar usuario atual
        usuario.filmes_vistos.add(filme)  # add a filmes_vistos

        # pode deixar tanto em branco dentro do super(), como super(DetailView, self), dá no mesmo
        return super().get(request, *args, **kwargs)  # redireciona o usuário para o link final


    def get_context_data(self, **kwargs):

        # pegar tudo o que a função já faz automaticamente
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        # criar lista com filmes com a mesma categoria
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados
        return context  # variável local


class Pesquisafilme(ListView):  # listview por padrão retorna um object_list (lista de itens do modelo)
    template_name = "pesquisa.html"
    model = Filme

    # função pronta para pegar query da url
    def get_queryset(self):

        # quando o usuário fizer uma requisicao do tipo GET, pegar parametro "query" da requisicao feita
        termo_pesquisa = self.request.GET.get("query")

        # se tiver um termo de pesquisa, o usuario passou um query
        if termo_pesquisa:

            # editar object_list padrão (parametro__icontains pega os termos que tem tal valor em seu parametro
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
        # o usuario chegou no link de pesquisa digitando manualmente, não retornar nada
        else:
            return None


# classe para editar perfil
class Editarperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"

    # modelo a ser editato
    model = Usuario

    # campos que poderão ser editados
    fields = ["first_name", "last_name", "email"]

    # impedir que o usuário tente mudar o perfil que não seja o dele
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.id != self.kwargs['pk']:
                return self.redirect_to_own_profile()
        else:
            return HttpResponseRedirect(reverse('filme:login'))
        return super().dispatch(request, *args, **kwargs)

    def redirect_to_own_profile(self):
        own_profile_url = reverse('filme:editar-perfil', kwargs={'pk': self.request.user.id})
        return HttpResponseRedirect(own_profile_url)

    # link para redirecionar em caso de sucesso
    def get_success_url(self):
        return reverse("filme:homefilmes")


class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = Criarcontaform

    # salvar novo usuario no banco de dados
    def form_valid(self, form):
        form.save()

        # retornar forms válido
        return super().form_valid(form)

    # informar para onde o formulario vai redirecionar caso tenha sido preenchido com sucesso
    def get_success_url(self):  # espera um link como resposta
        return reverse("filme:login")