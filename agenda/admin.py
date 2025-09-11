from django.contrib import admin
from .models import Agendamento, AgendamentoRepresentante, ChegadaDiaria

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = [
        'fornecedor', 
        'data_agendada', 
        'hora_agendada',
        'compareceu',
        'hora_entrada_real',
        'status_pontualidade_display',
        'observacoes'
    ]
    
    list_filter = [
        'data_agendada',
        'compareceu',
        'hora_agendada'
    ]
    
    search_fields = ['fornecedor', 'observacoes']
    
    readonly_fields = ['status_pontualidade_display']
    
    fieldsets = (
        ('Informações do Agendamento', {
            'fields': ('fornecedor', 'data_agendada', 'hora_agendada')
        }),
        ('Controle de Chegada', {
            'fields': ('compareceu', 'hora_entrada_real', 'observacoes', 'status_pontualidade_display'),
            'description': 'Preenchido pela Portaria/Recebimento quando o fornecedor chega'
        }),
    )
    
    def status_pontualidade_display(self, obj):
        return obj.status_pontualidade_display
    status_pontualidade_display.short_description = 'Status de Pontualidade'

@admin.register(ChegadaDiaria)
class ChegadaDiariaAdmin(admin.ModelAdmin):
    list_display = [
        'data',
        'total_agendamentos',
        'total_chegados',
        'total_pendentes',
        'total_pontuais',
        'total_atrasados',
        'total_adiantados'
    ]
    
    list_filter = [
        'data'
    ]
    
    readonly_fields = [
        'total_agendamentos', 
        'total_chegados', 
        'total_pendentes',
        'total_pontuais',
        'total_atrasados',
        'total_adiantados'
    ]
    
    def has_add_permission(self, request):
        return False  # Gerado automaticamente

@admin.register(AgendamentoRepresentante)
class AgendamentoRepresentanteAdmin(admin.ModelAdmin):
    list_display = [
        'nome_representante', 
        'fornecedor_marca',
        'data_agendada', 
        'hora_agendada',
        'comprador_responsavel',
        'compareceu',
        'hora_entrada_real',
        'status_pontualidade_display'
    ]
    
    list_filter = [
        'data_agendada',
        'compareceu',
        'hora_agendada',
        'comprador_responsavel'
    ]
    
    search_fields = ['nome_representante', 'fornecedor_marca', 'comprador_responsavel', 'observacoes']
    
    readonly_fields = ['status_pontualidade_display']
    
    fieldsets = (
        ('Informações da Visita', {
            'fields': ('nome_representante', 'fornecedor_marca', 'data_agendada', 'hora_agendada', 'comprador_responsavel')
        }),
        ('Controle de Chegada', {
            'fields': ('compareceu', 'hora_entrada_real', 'observacoes', 'status_pontualidade_display'),
            'description': 'Preenchido pela Portaria/Recebimento quando o representante chega'
        }),
    )
    
    def status_pontualidade_display(self, obj):
        return obj.status_pontualidade_display
    status_pontualidade_display.short_description = 'Status de Pontualidade'