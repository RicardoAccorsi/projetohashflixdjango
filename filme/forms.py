'''
criar forms personalizados
'''
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms

# form da homepage
class Formhome(forms.Form):  # forms.Form é o formulário padrão do django
    email = forms.EmailField(label=False)  # retirar legenda do campo com label=False

# form de criar conta
class Criarcontaform(UserCreationForm):

    # acrescentar campo de email na hora de criar conta (por padrão, o django tem username, senha e conf senha
    email = forms.EmailField(required=True)

    # passar modelo de usuario que o site está utilizando
    class Meta:
        model = Usuario

        # editar campos que aparecerão no forms
        fields = ("username", "email", "password1", "password2")