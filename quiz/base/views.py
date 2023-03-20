from django.shortcuts import render, redirect

# Create your views here.
from quiz.base.forms import AlunoForm
from quiz.base.models import Pergunta


def home(requisicao):
    if requisicao.method == 'POST':
        formulario = AlunoForm(requisicao.POST)
        if formulario.is_valid():
            aluno = formulario.save()
            return redirect('/perguntas/1')
    return render(requisicao, 'base/home.html')


def perguntas(requisicao, indice):
    pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
    contexto = {'indice_da_questao': indice, 'pergunta': pergunta}
    return render(requisicao, 'base/game.html', context=contexto)


def clasificacao(requisicao):
    return render(requisicao, 'base/clasificacao.html')
