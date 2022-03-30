from django.urls import path
from . import views

urlpatterns = [
    path('', views.encontrar_usuario, name='encontrar_usuario'),
    path('<str:id>/formulario_competencias', views.formulario_competencias, name='formulario_competencias'),
    path('<str:id>/avaliar_competencias', views.avaliar_compentecias, name='avaliar_compentecias'),
    path('dashboard/startup', views.dashboard_startup, name='dashboard_startup'),
]