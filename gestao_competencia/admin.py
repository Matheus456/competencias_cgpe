from django.contrib import admin
from .models import *

class NameId(admin.ModelAdmin):
    search_fields = ['id', 'nome']

admin.site.register(Area, NameId)
admin.site.register(Colaborador, NameId)
admin.site.register(SoftSkill, NameId)
admin.site.register(HardSkill, NameId)
admin.site.register(ColaboradorHardSkill)
admin.site.register(ColaboradorSoftSkill)
admin.site.register(Startup, NameId)
admin.site.register(SubArea, NameId)
admin.site.register(Escala)
