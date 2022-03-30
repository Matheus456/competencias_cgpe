from ast import Sub
from django.shortcuts import render, redirect
from django.db.models import Count, Avg
from numpy import array
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

def dashboard_startup(request):
    startups = Startup.objects.all()
    startup_selected = startups.get(id=request.GET['id'])
    colaboradores = Colaborador.objects.filter(startup = startup_selected).order_by('area')

    areas = colaboradores.values_list('area', flat=True).distinct()
    soft_skills = colaboradores.values_list('soft_skills', flat=True).distinct()
    hard_skills = colaboradores.values_list('hard_skills', flat=True).distinct()


    sub_areas = colaboradores.values_list('hard_skills__subarea', flat=True).distinct()
    sub_areas_avg = ColaboradorHardSkill.objects.filter(hard_skill__in=hard_skills).values_list('hard_skill__subarea').annotate(dcount=Avg('score_hard'))

    array_bubble = []
    
    for index, sub_area_avg in enumerate(sub_areas_avg):
        try:
            nome = SubArea.objects.get(id=sub_area_avg[0]).nome
            if nome:
                hash_bubble = {"nome": nome, "id": sub_area_avg[0], "groupid": index, "size": sub_area_avg[1]}
                array_bubble.append(hash_bubble)
        except SubArea.DoesNotExist:
          pass

    sub_areas_objects = SubArea.objects.filter(id__in = sub_areas)

    print("TESTE")
    print(array_bubble)
    print("TESTE")


    return render(request, 'dashboard/filtro_startup.html',
        {
            'startups': startups,
            'startup_selected': startup_selected,
            'colaboradores': colaboradores,
            'areas': areas,
            'soft_skills': soft_skills,
            'hard_skills': hard_skills,
            'array_bubble': array_bubble,
        }
    )

def _atualiza_skills(request, tipo, classe, campo, id_colaorador):
    skills = request.GET.getlist(tipo)
    skills_a = {a: request.GET[tipo + "-{}".format(a)] for a in skills}
    for key in skills_a:
        colaborador = classe.objects.filter(**{tipo: key}, colaborador=id_colaorador)
        colaborador.update(**{campo: skills_a[key]})
