from django.conf import settings
from django.db import models
from django.utils import timezone


class Area(models.Model):
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    nome = models.TextField()
    
    def __str__(self):
        return self.nome

class SubArea(models.Model):
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    nome = models.TextField()
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.nome


class SoftSkill(models.Model):
    nome = models.TextField()
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    id =  models.CharField(primary_key=True, max_length=255, unique=True)

    def __str__(self):
        return self.nome

class HardSkill(models.Model):
    nome = models.TextField()
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    subarea = models.ForeignKey(SubArea, null=True, on_delete=models.SET_NULL)
    id =  models.CharField(primary_key=True, max_length=255, unique=True)

    def __str__(self):
        return self.nome

class Startup(models.Model):
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    nome = models.TextField()

class Colaborador(models.Model):
    id =  models.CharField(primary_key=True, max_length=255, unique=True)
    nome = models.TextField()
    email = models.TextField()
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    startup = models.ForeignKey(Startup, null=True, on_delete=models.SET_NULL)
    hard_skills = models.ManyToManyField(HardSkill, through='ColaboradorHardSkill')
    soft_skills = models.ManyToManyField(SoftSkill, through='ColaboradorSoftSkill')

    def __str__(self):
        return self.nome

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