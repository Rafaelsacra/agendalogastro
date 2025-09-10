from django.db import models
from django.utils import timezone

# Create your models here.

class Agendamento(models.Model):
    fornecedor = models.CharField(max_length=100)
    data = models.DateField()
    horario_agendado = models.TimeField()
    quantidade_volumes = models.IntegerField()
    nota_fiscal = models.CharField(max_length=50, blank=True, null=True)
    status_entrega = models.CharField(max_length=50, blank=True, null=True)
    
    # Novos campos para controle de pontualidade
    compareceu = models.BooleanField(default=False, verbose_name="Fornecedor compareceu?")
    hora_entrada_real = models.DateTimeField(null=True, blank=True, verbose_name="Hora de entrada real")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações adicionais")
    
    # Outros campos podem ser adicionados conforme necessário

    @property
    def status_pontualidade(self):
        """Calcula o status de pontualidade automaticamente"""
        if not self.compareceu or not self.hora_entrada_real:
            return "Não compareceu"
        
        # Combina data e hora agendada em datetime
        hora_prevista = timezone.make_aware(
            timezone.datetime.combine(self.data, self.horario_agendado)
        )
        
        # Calcula diferença em minutos
        diferenca_minutos = (self.hora_entrada_real - hora_prevista).total_seconds() / 60
        
        if abs(diferenca_minutos) <= 5:  # Tolerância de 5 minutos
            return "Pontual"
        elif diferenca_minutos > 5:
            return "Atrasado"
        else:
            return "Adiantado"

    @property
    def status_pontualidade_display(self):
        """Retorna o status com ícones para exibição"""
        status = self.status_pontualidade
        if status == "Pontual":
            return "✅ Pontual"
        elif status == "Atrasado":
            return "⏰ Atrasado"
        elif status == "Adiantado":
            return "⏰ Adiantado"
        else:
            return "❌ Não compareceu"

    def __str__(self):
        return f"{self.fornecedor} - {self.data} {self.horario_agendado}"
