# Generated by Django 3.2.9 on 2021-12-04 16:26

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
                ('nome', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('nome', models.TextField()),
                ('email', models.TextField()),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.area')),
            ],
        ),
        migrations.CreateModel(
            name='SoftSkill',
            fields=[
                ('nome', models.TextField()),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.area')),
            ],
        ),
        migrations.CreateModel(
            name='HardSkill',
            fields=[
                ('nome', models.TextField()),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestao_competencia.area')),
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
    ]
