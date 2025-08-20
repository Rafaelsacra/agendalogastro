from django.urls import path
from . import views

urlpatterns = [
    path('calendario/', views.calendario, name='calendario'),
    path('eventos/', views.eventos_json, name='eventos_json'),
    path('verificar-atualizacoes/', views.verificar_atualizacoes, name='verificar_atualizacoes'),
] 