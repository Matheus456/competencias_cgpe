# Generated by Django 4.0 on 2022-03-30 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=70)),
                ('email', models.CharField(max_length=70)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.area')),
            ],
        ),
        migrations.CreateModel(
            name='Escala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legenda_1', models.CharField(blank=True, max_length=35)),
                ('legenda_2', models.CharField(blank=True, max_length=35)),
                ('legenda_3', models.CharField(blank=True, max_length=35)),
                ('legenda_4', models.CharField(blank=True, max_length=35)),
                ('legenda_5', models.CharField(blank=True, max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Startup',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='SubArea',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=70)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.area')),
            ],
        ),
        migrations.CreateModel(
            name='SoftSkill',
            fields=[
                ('nome', models.CharField(max_length=70)),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.area')),
                ('escala', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.escala')),
            ],
        ),
        migrations.CreateModel(
            name='HardSkill',
            fields=[
                ('nome', models.CharField(max_length=70)),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.area')),
                ('escala', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.escala')),
                ('subarea', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.subarea')),
            ],
        ),
        migrations.CreateModel(
            name='ColaboradorSoftSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_soft', models.IntegerField(null=True)),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_competencia.colaborador')),
                ('soft_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_competencia.softskill')),
            ],
        ),
        migrations.CreateModel(
            name='ColaboradorHardSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_hard', models.IntegerField(null=True)),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_competencia.colaborador')),
                ('hard_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_competencia.hardskill')),
            ],
        ),
        migrations.AddField(
            model_name='colaborador',
            name='hard_skills',
            field=models.ManyToManyField(through='gestao_competencia.ColaboradorHardSkill', to='gestao_competencia.HardSkill'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='soft_skills',
            field=models.ManyToManyField(through='gestao_competencia.ColaboradorSoftSkill', to='gestao_competencia.SoftSkill'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='startup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.startup'),
        ),
    ]
