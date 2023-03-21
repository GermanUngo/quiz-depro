from django.shortcuts import render, redirect
from django.utils.timezone import now

from quiz.base.forms import AlunoForm
from quiz.base.models import Pergunta, Aluno, Resposta


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


PONTUACAO_MAXIMA = 1000


def perguntas(requisicao, indice):
    try:
        aluno_id = requisicao.session['aluno_id']
    except KeyError:
        return redirect('/')
    else:
        try:
            pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
        except IndexError:
            return redirect('/classificacao')
        else:
            contexto = {'indice_da_questao': indice, 'pergunta': pergunta}
            if requisicao.method == 'POST':
                resposta_indice = int(requisicao.POST['resposta_indice'])
                if resposta_indice == pergunta.aleternativa_correta:
                    # Armazenar os dados da resposta
                    try:
                        data_da_primeira_resposta = Resposta.objects.filter(pergunta=pergunta).order_by('respondida_em')[0].respondida_em
                    except IndexError:
                        Resposta(aluno_id=aluno_id, pergunta=pergunta, pontos=PONTUACAO_MAXIMA).save()
                    else:
                        diferenca = now() - data_da_primeira_resposta
                        diferenca_em_segundos = int(diferenca.total_seconds())
                        pontos = max(PONTUACAO_MAXIMA - diferenca_em_segundos, 10)
                        Resposta(aluno_id=aluno_id, pergunta=pergunta, pontos=pontos).save()
                    return redirect(f'/perguntas/{indice + 1}')
                contexto['resposta_indice'] = resposta_indice
            return render(requisicao, 'base/game.html', context=contexto)


def clasificacao(requisicao):
    try:
        aluno_id = requisicao.session['aluno_id']
    except KeyError:
        return redirect('/')
    else:
        return render(requisicao, 'base/clasificacao.html')
