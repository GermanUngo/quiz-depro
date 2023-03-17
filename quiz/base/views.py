from django.shortcuts import render

# Create your views here.
from quiz.base.models import Pergunta


def home(requisicao):
    return render(requisicao, 'base/home.html')


def perguntas(requisicao, indice):
    pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
    contexto = {'indice_da_questao': indice, 'pergunta': pergunta}
    return render(requisicao, 'base/game.html', context=contexto)


def clasificacao(requisicao):
    return render(requisicao, 'base/clasificacao.html')
