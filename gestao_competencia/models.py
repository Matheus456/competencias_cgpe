from django.conf import settings
from django.db import models
from django.utils import timezone


class Area(models.Model):
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    nome = models.CharField(max_length=70)
    
    def __str__(self):
        return f"{self.nome} - {self.id}"

class SubArea(models.Model):
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    nome = models.CharField(max_length=70)
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.nome} - {self.id}"

class Escala(models.Model):
    legenda_1 = models.CharField(max_length=35, blank=True) 
    legenda_2 = models.CharField(max_length=35, blank=True) 
    legenda_3 = models.CharField(max_length=35, blank=True) 
    legenda_4 = models.CharField(max_length=35, blank=True) 
    legenda_5 = models.CharField(max_length=35, blank=True) 

    def __str__(self):
        return f"{self.legenda_1} | {self.legenda_2} | {self.legenda_3} | {self.legenda_4} | {self.legenda_5}"

class SoftSkill(models.Model):
    nome = models.CharField(max_length=70)
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    escala = models.ForeignKey(Escala, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nome

class HardSkill(models.Model):
    nome = models.CharField(max_length=70)
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    subarea = models.ForeignKey(SubArea, null=True, on_delete=models.SET_NULL)
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    escala = models.ForeignKey(Escala, null=True, on_delete=models.SET_NULL)
    

    def __str__(self):
        return f"{self.nome} - {self.id} - {self.area.nome}"

class Startup(models.Model):
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    nome = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.nome} - {self.id}"

class Colaborador(models.Model):
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    nome = models.CharField(max_length=70)
    email = models.CharField(max_length=70)
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    startup = models.ForeignKey(Startup, null=True, on_delete=models.SET_NULL)
    hard_skills = models.ManyToManyField(HardSkill, through='ColaboradorHardSkill')
    soft_skills = models.ManyToManyField(SoftSkill, through='ColaboradorSoftSkill')

    def __str__(self):
        return f"{self.nome} - {self.id}"

class ColaboradorHardSkill(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    hard_skill = models.ForeignKey(HardSkill, on_delete=models.CASCADE)
    score_hard = models.IntegerField(null=True)

    def __str__(self):
        return self.colaborador.nome + ' - ' + self.hard_skill.nome

class ColaboradorSoftSkill(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    soft_skill = models.ForeignKey(SoftSkill, on_delete=models.CASCADE)
    score_soft = models.IntegerField(null=True)

    def __str__(self):
        return self.colaborador.nome + ' - ' + self.soft_skill.nome