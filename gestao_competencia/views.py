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
    colaborador_hard = ColaboradorHardSkill.objects.raw('''
        SELECT * FROM gestao_competencia_colaboradorhardskill as colaborador_hs
            INNER JOIN gestao_competencia_hardskill as hs
                ON colaborador_hs.hard_skill_id=hs.id
            INNER JOIN gestao_competencia_subarea as subarea
                ON hs.subarea_id=subarea.id
            WHERE colaborador_id = %s
            ORDER BY subarea.nome
        ''', [colaborador.id])

    return render(request, 'gestao_competencia/form_competencias.html', {
        'colaborador': colaborador,
        'colaborador_softs': colaborador_soft,
        'colaborador_hards': colaborador_hard,
    })

def avaliar_compentecias(request, id):
    _atualiza_skills(request, 'soft_skill', ColaboradorSoftSkill, 'score_soft', id)
    _atualiza_skills(request, 'hard_skill', ColaboradorHardSkill, 'score_hard', id)
    return render(request, 'gestao_competencia/agradecimento.html', {})

def _atualiza_skills(request, tipo, classe, campo, id_colaorador):
    skills = request.GET.getlist(tipo)
    skills_a = {a: request.GET[tipo + "-{}".format(a)] for a in skills}
    for key in skills_a:
        colaborador = classe.objects.filter(**{tipo: key}, colaborador=id_colaorador)
        colaborador.update(**{campo: skills_a[key]})
