from ast import Sub
from django.shortcuts import render, redirect
from django.db.models import Count, Avg, Case, When
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

    sub_areas_avg = ColaboradorHardSkill.objects.filter(hard_skill__in=hard_skills).values_list('hard_skill__subarea').annotate(dcount=Avg('score_hard'))

    array_bubble = []
    
    for index, sub_area_avg in enumerate(sub_areas_avg):
        try:
            nome = SubArea.objects.get(id=sub_area_avg[0]).nome
            if nome:
                hash_bubble = {"nome": nome, "id": sub_area_avg[0], "groupid": index, "size": round(sub_area_avg[1], 2)}
                array_bubble.append(hash_bubble)
        except SubArea.DoesNotExist:
          pass

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

def dashboard_competencias(request):
    hard_skills = HardSkill.objects.all()
    hard_skill_selected = hard_skills.get(id=request.GET['id'])
    colaborador_hard_skill = ColaboradorHardSkill.objects.filter(hard_skill_id = hard_skill_selected, colaborador__startup__isnull=False).order_by('score_hard')
    colaboradores_ids = colaborador_hard_skill.values('colaborador_id')

    scores_avg = colaborador_hard_skill.values_list('colaborador__startup').annotate(dcount=Avg('score_hard'))
    preserved = Case(*[When(pk=pk['colaborador_id'], then=pos) for pos, pk in enumerate(colaboradores_ids)])
    print(preserved)
    colaboradores = Colaborador.objects.filter(id__in = colaboradores_ids).order_by(preserved)

    areas = colaboradores.values_list('area', flat=True).distinct()
    startups = colaboradores.values_list('startup', flat=True).distinct()
    hard_skill_score = 0
    array_bubble = []
    if colaboradores.count() > 0:
        hard_skill_score = round(colaborador_hard_skill.aggregate(Avg('score_hard'))['score_hard__avg'], 2)

        array_bubble = []
        
        for index, score_avg in enumerate(scores_avg):
            try:
                nome = Startup.objects.get(id=score_avg[0]).nome
                if nome:
                    hash_bubble = {"nome": nome, "id": score_avg[0], "groupid": index, "size": round(score_avg[1], 2)}
                    array_bubble.append(hash_bubble)
            except SubArea.DoesNotExist:
                pass

    return render(request, 'dashboard/filtro_competencia.html',
        {
            'hard_skills': hard_skills,
            'hard_skill_score': hard_skill_score,
            'hard_skill_selected': hard_skill_selected,
            'colaborador_hard_skill': colaborador_hard_skill,
            'colaboradores': colaboradores,
            'areas': areas,
            'startups': startups,
            'array_bubble': array_bubble,
        }
    )

def _atualiza_skills(request, tipo, classe, campo, id_colaorador):
    skills = request.GET.getlist(tipo)
    skills_a = {a: request.GET[tipo + "-{}".format(a)] for a in skills}
    for key in skills_a:
        colaborador = classe.objects.filter(**{tipo: key}, colaborador=id_colaorador)
        colaborador.update(**{campo: skills_a[key]})
