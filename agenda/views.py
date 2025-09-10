from datetime import date, timedelta, datetime
from .models import Agendamento
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json

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
        # Define cor baseada no status
        if a.compareceu:
            if a.status_pontualidade == 'Pontual':
                cor = '#28a745'  # Verde
            elif a.status_pontualidade == 'Atrasado':
                cor = '#dc3545'  # Vermelho
            elif a.status_pontualidade == 'Adiantado':
                cor = '#ffc107'  # Amarelo
            else:
                cor = cores[idx % len(cores)]
        else:
            cor = cores[idx % len(cores)]
            
        eventos.append({
            'title': a.fornecedor,
            'start': f"{a.data}T{a.horario_agendado}",
            'color': cor,
            'extendedProps': {
                'fornecedor': a.fornecedor,
                'status_pontualidade': a.status_pontualidade_display,
                'compareceu': a.compareceu,
                'hora_entrada_real': a.hora_entrada_real.strftime('%H:%M') if a.hora_entrada_real else None,
                'observacoes': a.observacoes or ''
            }
        })
    return render(request, 'agenda/calendario.html', {'eventos': eventos, 'hoje': hoje})

def eventos_json(request):
    agendamentos = Agendamento.objects.all()
    cores = ['#F26522', '#0054A6', '#757778']  # Laranja, Azul, Cinza Médio
    eventos = []
    for idx, a in enumerate(agendamentos):
        # Define cor baseada no status
        if a.compareceu:
            if a.status_pontualidade == 'Pontual':
                cor = '#28a745'  # Verde
            elif a.status_pontualidade == 'Atrasado':
                cor = '#dc3545'  # Vermelho
            elif a.status_pontualidade == 'Adiantado':
                cor = '#ffc107'  # Amarelo
            else:
                cor = cores[idx % len(cores)]
        else:
            cor = cores[idx % len(cores)]
            
        eventos.append({
            'title': a.fornecedor,
            'start': f"{a.data}T{a.horario_agendado}",
            'color': cor,
            'extendedProps': {
                'fornecedor': a.fornecedor,
                'status_pontualidade': a.status_pontualidade_display,
                'compareceu': a.compareceu,
                'hora_entrada_real': a.hora_entrada_real.strftime('%H:%M') if a.hora_entrada_real else None,
                'observacoes': a.observacoes or ''
            }
        })
    return JsonResponse(eventos, safe=False)

def verificar_atualizacoes(request):
    """View para verificar se houve atualizações recentes"""
    from django.core.cache import cache
    from django.http import JsonResponse
    
    ultima_importacao = cache.get('ultima_importacao')
    total_agendamentos = Agendamento.objects.count()
    
    return JsonResponse({
        'ultima_importacao': ultima_importacao,
        'total_agendamentos': total_agendamentos,
        'timestamp': datetime.now().isoformat()
    })

def controle_chegada(request):
    """View para portaria/recebimento controlar chegada dos fornecedores"""
    hoje = date.today()
    
    # Agendamentos de hoje que ainda não compareceram
    agendamentos_hoje = Agendamento.objects.filter(
        data=hoje
    ).order_by('horario_agendado')
    
    # Agendamentos já processados hoje
    agendamentos_processados = agendamentos_hoje.filter(compareceu=True)
    
    # Agendamentos pendentes
    agendamentos_pendentes = agendamentos_hoje.filter(compareceu=False)
    
    context = {
        'agendamentos_hoje': agendamentos_hoje,
        'agendamentos_processados': agendamentos_processados,
        'agendamentos_pendentes': agendamentos_pendentes,
        'hoje': hoje,
    }
    
    return render(request, 'agenda/controle_chegada.html', context)

def registrar_chegada(request, agendamento_id):
    """View para registrar a chegada de um fornecedor"""
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    
    if request.method == 'POST':
        compareceu = request.POST.get('compareceu') == 'on'
        hora_entrada_str = request.POST.get('hora_entrada_real')
        observacoes = request.POST.get('observacoes', '')
        
        agendamento.compareceu = compareceu
        agendamento.observacoes = observacoes
        
        if compareceu and hora_entrada_str:
            # Combina a data do agendamento com a hora fornecida
            try:
                hora_entrada = datetime.strptime(hora_entrada_str, '%H:%M').time()
                data_hora_entrada = timezone.make_aware(
                    datetime.combine(agendamento.data, hora_entrada)
                )
                agendamento.hora_entrada_real = data_hora_entrada
            except ValueError:
                messages.error(request, 'Formato de hora inválido. Use HH:MM')
                return redirect('controle_chegada')
        else:
            agendamento.hora_entrada_real = None
            
        agendamento.save()
        
        if compareceu:
            messages.success(request, f'Chegada registrada para {agendamento.fornecedor} - {agendamento.status_pontualidade_display}')
        else:
            messages.info(request, f'Registrado que {agendamento.fornecedor} não compareceu')
            
        return redirect('controle_chegada')
    
    return render(request, 'agenda/registrar_chegada.html', {'agendamento': agendamento})

@csrf_exempt
def registrar_chegada_ajax(request, agendamento_id):
    """API para registrar chegada via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        
        compareceu = data.get('compareceu', False)
        hora_entrada_str = data.get('hora_entrada_real', '')
        observacoes = data.get('observacoes', '')
        
        agendamento.compareceu = compareceu
        agendamento.observacoes = observacoes
        
        if compareceu and hora_entrada_str:
            try:
                hora_entrada = datetime.strptime(hora_entrada_str, '%H:%M').time()
                data_hora_entrada = timezone.make_aware(
                    datetime.combine(agendamento.data, hora_entrada)
                )
                agendamento.hora_entrada_real = data_hora_entrada
            except ValueError:
                return JsonResponse({'error': 'Formato de hora inválido'}, status=400)
        else:
            agendamento.hora_entrada_real = None
            
        agendamento.save()
        
        return JsonResponse({
            'success': True,
            'status_pontualidade': agendamento.status_pontualidade_display,
            'compareceu': agendamento.compareceu
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
