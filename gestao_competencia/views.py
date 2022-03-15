from django.shortcuts import render, redirect
from .models import *

def encontrar_usuario(request):
    email = request.GET.get('email')
    if email is None:
        return render(request, 'gestao_competencia/encontrar_usuario.html', {})
    else:
        try:
            colaborador = Colaborador.objects.get(email=email)
            return redirect('formulario_competencias', id=colaborador.id)
        except Colaborador.DoesNotExist: 
            return render(request, 'gestao_competencia/encontrar_usuario.html', 
                            {'mensagem': 'Não existe colaborador com esse email'})

def formulario_competencias(request, id):
    colaborador = Colaborador.objects.get(id=id)
    colaborador_soft = ColaboradorSoftSkill.objects.filter(colaborador=colaborador)
    colaborador_hard = ColaboradorHardSkill.objects.filter(colaborador=colaborador)
    return render(request, 'gestao_competencia/form_competencias.html', {'colaborador': colaborador,'colaborador_softs': colaborador_soft, 'colaborador_hards': colaborador_hard})

def avaliar_compentecias(request, id):
    soft_skills = request.GET.getlist('soft_skill')
    a_soft_skills = {a: request.GET['soft_skill-{}'.format(a)] for a in soft_skills}
    for key in a_soft_skills:
        colaborador_soft = ColaboradorSoftSkill.objects.filter(soft_skill=key, colaborador=id)
        colaborador_soft.update(score_soft=a_soft_skills[key])
    
    hard_skills = request.GET.getlist('hard_skill')
    a_hard_skills = {a: request.GET['hard_skill-{}'.format(a)] for a in hard_skills}
    for key in a_hard_skills:
        colaborador_soft = ColaboradorHardSkill.objects.filter(hard_skill=key, colaborador=id)
        colaborador_soft.update(score_hard=a_hard_skills[key])

    return render(request, 'gestao_competencia/agradecimento.html', {})

