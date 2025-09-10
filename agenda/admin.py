from django.contrib import admin
from .models import Agendamento

# Register your models here.

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = [
        'fornecedor', 
        'data', 
        'horario_agendado', 
        'compareceu', 
        'hora_entrada_real',
        'status_pontualidade_display',
        'quantidade_volumes'
    ]
    
    list_filter = [
        'data',
        'compareceu',
        'horario_agendado'
    ]
    
    search_fields = ['fornecedor', 'nota_fiscal']
    
    readonly_fields = ['status_pontualidade_display']
    
    fieldsets = (
        ('Informações do Agendamento', {
            'fields': ('fornecedor', 'data', 'horario_agendado', 'quantidade_volumes', 'nota_fiscal', 'status_entrega')
        }),
        ('Controle de Chegada', {
            'fields': ('compareceu', 'hora_entrada_real', 'observacoes', 'status_pontualidade_display'),
            'description': 'Preenchido pela Portaria/Recebimento quando o fornecedor chega'
        }),
    )
    
    def status_pontualidade_display(self, obj):
        return obj.status_pontualidade_display
    status_pontualidade_display.short_description = 'Status de Pontualidade'
