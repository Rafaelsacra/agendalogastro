from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Agendamento, AgendamentoRepresentante, ChegadaDiaria
from django.http import JsonResponse
from datetime import timedelta, date, datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

# Calendário
def calendario(request):
    return render(request, "agenda/calendario.html")

# Eventos JSON para o FullCalendar
def eventos_json(request):
    data = []
    
    # Agendamentos de mercadoria
    agendamentos = Agendamento.objects.exclude(data_agendada__week_day__in=[1,7])  # Django: 1=Domingo, 7=Sábado
    for e in agendamentos:
        # Define cor baseada no status de pontualidade
        if e.compareceu:
            if e.status_pontualidade == 'Pontual':
                cor = '#28a745'  # Verde
            elif e.status_pontualidade == 'Atrasado':
                cor = '#dc3545'  # Vermelho
            elif e.status_pontualidade == 'Adiantado':
                cor = '#ffc107'  # Amarelo
            else:
                cor = '#6c757d'  # Cinza
        else:
            cor = '#6c757d'  # Cinza para não compareceu
            
        data.append({
            "title": f"📦 {e.fornecedor}",
            "start": f"{e.data_agendada}T{e.hora_agendada}",
            "end": f"{e.data_agendada}T{e.hora_agendada}",
            "color": cor,
            "extendedProps": {
                'tipo': 'mercadoria',
                'fornecedor': e.fornecedor,
                'status_pontualidade': e.status_pontualidade_display,
                'compareceu': e.compareceu,
                'hora_entrada_real': e.hora_entrada_real.strftime('%H:%M') if e.hora_entrada_real else None,
                'observacoes': e.observacoes or ''
            }
        })
    
    # Agendamentos de representantes
    representantes = AgendamentoRepresentante.objects.exclude(data_agendada__week_day__in=[1,7])
    for r in representantes:
        # Define cor baseada no status de pontualidade (cores diferentes para representantes)
        if r.compareceu:
            if r.status_pontualidade == 'Pontual':
                cor = '#17a2b8'  # Azul claro
            elif r.status_pontualidade == 'Atrasado':
                cor = '#e83e8c'  # Rosa
            elif r.status_pontualidade == 'Adiantado':
                cor = '#fd7e14'  # Laranja
            else:
                cor = '#6c757d'  # Cinza
        else:
            cor = '#6c757d'  # Cinza para não compareceu
            
        data.append({
            "title": f"👤 {r.nome_representante} - {r.fornecedor_marca}",
            "start": f"{r.data_agendada}T{r.hora_agendada}",
            "end": f"{r.data_agendada}T{r.hora_agendada}",
            "color": cor,
            "extendedProps": {
                'tipo': 'representante',
                'nome_representante': r.nome_representante,
                'fornecedor_marca': r.fornecedor_marca,
                'comprador_responsavel': r.comprador_responsavel,
                'status_pontualidade': r.status_pontualidade_display,
                'compareceu': r.compareceu,
                'hora_entrada_real': r.hora_entrada_real.strftime('%H:%M') if r.hora_entrada_real else None,
                'observacoes': r.observacoes or ''
            }
        })
    
    return JsonResponse(data, safe=False)

# Controle de chegada
def controle_chegada(request):
    dia_param = request.GET.get("dia")
    if dia_param:
        dia_atual = date.fromisoformat(dia_param)
    else:
        dia_atual = date.today()

    agendamentos = Agendamento.objects.filter(data_agendada=dia_atual).order_by('hora_agendada')
    representantes = AgendamentoRepresentante.objects.filter(data_agendada=dia_atual).order_by('hora_agendada')

    # Atualiza registro diário com estatísticas de pontualidade
    total_agendamentos = agendamentos.count()
    total_representantes = representantes.count()
    total_geral = total_agendamentos + total_representantes
    
    chegados_agendamentos = agendamentos.filter(compareceu=True).count()
    chegados_representantes = representantes.filter(compareceu=True).count()
    total_chegados = chegados_agendamentos + chegados_representantes
    
    pendentes_agendamentos = total_agendamentos - chegados_agendamentos
    pendentes_representantes = total_representantes - chegados_representantes
    total_pendentes = pendentes_agendamentos + pendentes_representantes
    
    # Estatísticas de pontualidade para agendamentos
    pontuais_agendamentos = 0
    atrasados_agendamentos = 0
    adiantados_agendamentos = 0
    
    for agendamento in agendamentos.filter(compareceu=True, hora_entrada_real__isnull=False):
        if agendamento.status_pontualidade == 'Pontual':
            pontuais_agendamentos += 1
        elif agendamento.status_pontualidade == 'Atrasado':
            atrasados_agendamentos += 1
        elif agendamento.status_pontualidade == 'Adiantado':
            adiantados_agendamentos += 1
    
    # Estatísticas de pontualidade para representantes
    pontuais_representantes = 0
    atrasados_representantes = 0
    adiantados_representantes = 0
    
    for representante in representantes.filter(compareceu=True, hora_entrada_real__isnull=False):
        if representante.status_pontualidade == 'Pontual':
            pontuais_representantes += 1
        elif representante.status_pontualidade == 'Atrasado':
            atrasados_representantes += 1
        elif representante.status_pontualidade == 'Adiantado':
            adiantados_representantes += 1
    
    total_pontuais = pontuais_agendamentos + pontuais_representantes
    total_atrasados = atrasados_agendamentos + atrasados_representantes
    total_adiantados = adiantados_agendamentos + adiantados_representantes
    
    ChegadaDiaria.objects.update_or_create(
        data=dia_atual,
        defaults={
            "total_agendamentos": total_agendamentos,
            "total_chegados": chegados_agendamentos,
            "total_pendentes": pendentes_agendamentos,
            "total_pontuais": pontuais_agendamentos,
            "total_atrasados": atrasados_agendamentos,
            "total_adiantados": adiantados_agendamentos,
            "total_representantes": total_representantes,
            "total_representantes_chegados": chegados_representantes
        }
    )

    dia_anterior = dia_atual - timedelta(days=1)
    dia_seguinte = dia_atual + timedelta(days=1)

    return render(request, "agenda/controle_chegada.html", {
        "agendamentos": agendamentos,
        "representantes": representantes,
        "dia_atual": dia_atual,
        "dia_anterior": dia_anterior,
        "dia_seguinte": dia_seguinte,
        "total_agendamentos": total_agendamentos,
        "total_representantes": total_representantes,
        "total_geral": total_geral,
        "total_chegados": total_chegados,
        "total_pendentes": total_pendentes,
        "total_pontuais": total_pontuais,
        "total_atrasados": total_atrasados,
        "total_adiantados": total_adiantados
    })

# Registrar chegada - formulário
def registrar_chegada(request, agendamento_id):
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
                    datetime.combine(agendamento.data_agendada, hora_entrada)
                )
                agendamento.hora_entrada_real = data_hora_entrada
            except ValueError:
                messages.error(request, 'Formato de hora inválido. Use HH:MM')
                return redirect('agenda:controle_chegada')
        else:
            agendamento.hora_entrada_real = None
            
        agendamento.save()
        
        if compareceu:
            messages.success(request, f'Chegada registrada para {agendamento.fornecedor} - {agendamento.status_pontualidade_display}')
        else:
            messages.info(request, f'Registrado que {agendamento.fornecedor} não compareceu')
            
        return redirect('agenda:controle_chegada')
    
    return render(request, 'agenda/registrar_chegada.html', {'agendamento': agendamento})

# Criar agendamento de representante
@csrf_exempt
def criar_agendamento_representante(request):
    """API para criar agendamento de representante via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        agendamento = AgendamentoRepresentante.objects.create(
            nome_representante=data.get('nome_representante'),
            fornecedor_marca=data.get('fornecedor_marca'),
            data_agendada=data.get('data_agendada'),
            hora_agendada=data.get('hora_agendada'),
            comprador_responsavel=data.get('comprador_responsavel'),
            observacoes=data.get('observacoes', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Agendamento de representante criado com sucesso!',
            'agendamento_id': agendamento.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Registrar chegada de representante
def registrar_chegada_representante(request, representante_id):
    representante = get_object_or_404(AgendamentoRepresentante, id=representante_id)
    
    if request.method == 'POST':
        compareceu = request.POST.get('compareceu') == 'on'
        hora_entrada_str = request.POST.get('hora_entrada_real')
        observacoes = request.POST.get('observacoes', '')
        
        representante.compareceu = compareceu
        representante.observacoes = observacoes
        
        if compareceu and hora_entrada_str:
            try:
                hora_entrada = datetime.strptime(hora_entrada_str, '%H:%M').time()
                data_hora_entrada = timezone.make_aware(
                    datetime.combine(representante.data_agendada, hora_entrada)
                )
                representante.hora_entrada_real = data_hora_entrada
            except ValueError:
                messages.error(request, 'Formato de hora inválido. Use HH:MM')
                return redirect('agenda:controle_chegada')
        else:
            representante.hora_entrada_real = None
            
        representante.save()
        
        if compareceu:
            messages.success(request, f'Chegada registrada para {representante.nome_representante} - {representante.status_pontualidade_display}')
        else:
            messages.info(request, f'Registrado que {representante.nome_representante} não compareceu')
            
        return redirect('agenda:controle_chegada')
    
    return render(request, 'agenda/registrar_chegada_representante.html', {'representante': representante})

# Verificar atualizações
def verificar_atualizacoes(request):
    """View para verificar se houve atualizações recentes"""
    total_agendamentos = Agendamento.objects.count()
    total_representantes = AgendamentoRepresentante.objects.count()
    
    return JsonResponse({
        'total_agendamentos': total_agendamentos,
        'total_representantes': total_representantes,
        'total_geral': total_agendamentos + total_representantes,
        'timestamp': timezone.now().isoformat()
    })