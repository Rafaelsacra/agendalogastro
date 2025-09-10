from django.urls import path
from . import views

urlpatterns = [
    path('calendario/', views.calendario, name='calendario'),
    path('eventos/', views.eventos_json, name='eventos_json'),
    path('verificar-atualizacoes/', views.verificar_atualizacoes, name='verificar_atualizacoes'),
    path('controle-chegada/', views.controle_chegada, name='controle_chegada'),
    path('registrar-chegada/<int:agendamento_id>/', views.registrar_chegada, name='registrar_chegada'),
    path('api/registrar-chegada/<int:agendamento_id>/', views.registrar_chegada_ajax, name='registrar_chegada_ajax'),
] 