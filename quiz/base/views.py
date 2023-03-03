from django.shortcuts import render

# Create your views here.


def home(requisicao):
    return render(requisicao, 'base/home.html')


def perguntas(requisicao, indice):
    contexto = {'indice_da_questao':indice}
    return render(requisicao, 'base/game.html', context=contexto)


def clasificacao(requisicao):
    return render(requisicao, 'base/clasificacao.html')
