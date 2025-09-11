from django.urls import path
from . import views

app_name = "agenda"

urlpatterns = [
    path("calendario/", views.calendario, name="calendario"),
    path("controle-chegada/", views.controle_chegada, name="controle_chegada"),
    path("eventos-json/", views.eventos_json, name="eventos_json"),
    path("registrar-chegada/<int:agendamento_id>/", views.registrar_chegada, name="registrar_chegada"),
    path("registrar-chegada-representante/<int:representante_id>/", views.registrar_chegada_representante, name="registrar_chegada_representante"),
    path("criar-agendamento-representante/", views.criar_agendamento_representante, name="criar_agendamento_representante"),
    path("verificar-atualizacoes/", views.verificar_atualizacoes, name="verificar_atualizacoes"),
]