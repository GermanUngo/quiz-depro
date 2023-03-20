from django.shortcuts import render, redirect

# Create your views here.
from quiz.base.forms import AlunoForm
from quiz.base.models import Pergunta, Aluno


def home(requisicao):
    if requisicao.method == 'POST':
        #Usuario já existe
        email = requisicao.POST['email']
        try:
            aluno = Aluno.objects.get(email=email)
        except Aluno.DoesNotExist:

            #Usuário não existe
            formulario = AlunoForm(requisicao.POST)
            if formulario.is_valid():
                aluno = formulario.save()
                requisicao.session['aluno_id'] = aluno.id
                return redirect('/perguntas/1')
            else:
                contexto = {'formulario': formulario}
                return render(requisicao, 'base/home.html', contexto)
        else:
            requisicao.session['aluno_id'] = aluno.id
            return redirect('/perguntas/1')

    return render(requisicao, 'base/home.html')


def perguntas(requisicao, indice):
    pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
    contexto = {'indice_da_questao': indice, 'pergunta': pergunta}
    return render(requisicao, 'base/game.html', context=contexto)


def clasificacao(requisicao):
    return render(requisicao, 'base/clasificacao.html')
