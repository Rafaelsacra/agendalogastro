from datetime import date, timedelta
from .models import Agendamento
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def calendario_semanal(request):
    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    agendamentos = Agendamento.objects.filter(data__range=[inicio_semana, fim_semana])
    eventos = [
        {
            'title': a.fornecedor,
            'start': f"{a.data}T{a.horario_agendado}",
        }
        for a in agendamentos
    ]
    return render(request, 'agenda/calendario.html', {'eventos': eventos})

def calendario(request):
    hoje = date.today()
    agendamentos = Agendamento.objects.all()
    cores = ['#F26522', '#0054A6', '#757778']  # Laranja, Azul, Cinza Médio
    eventos = []
    for idx, a in enumerate(agendamentos):
        eventos.append({
            'title': a.fornecedor,
            'start': f"{a.data}T{a.horario_agendado}",
            'color': cores[idx % len(cores)],
            'extendedProps': {
                'fornecedor': a.fornecedor
            }
        })
    return render(request, 'agenda/calendario.html', {'eventos': eventos, 'hoje': hoje})

def eventos_json(request):
    agendamentos = Agendamento.objects.all()
    cores = ['#F26522', '#0054A6', '#757778']  # Laranja, Azul, Cinza Médio
    eventos = []
    for idx, a in enumerate(agendamentos):
        eventos.append({
            'title': a.fornecedor,
            'start': f"{a.data}T{a.horario_agendado}",
            'color': cores[idx % len(cores)],
            'extendedProps': {
                'fornecedor': a.fornecedor
            }
        })
    return JsonResponse(eventos, safe=False)
