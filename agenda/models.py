from django.db import models
from django.utils import timezone

class Agendamento(models.Model):
    fornecedor = models.CharField(max_length=255)
    data_agendada = models.DateField()
    hora_agendada = models.TimeField()
    
    # Novos campos para controle de pontualidade
    compareceu = models.BooleanField(default=False, verbose_name="Fornecedor compareceu?")
    hora_entrada_real = models.DateTimeField(null=True, blank=True, verbose_name="Hora de entrada real")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações adicionais")

    @property
    def status_pontualidade(self):
        """Calcula o status de pontualidade automaticamente"""
        if not self.compareceu or not self.hora_entrada_real:
            return "Não compareceu"
        
        # Combina data e hora agendada em datetime
        hora_prevista = timezone.make_aware(
            timezone.datetime.combine(self.data_agendada, self.hora_agendada)
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
        return f"{self.fornecedor} - {self.data_agendada} {self.hora_agendada}"

class AgendamentoRepresentante(models.Model):
    nome_representante = models.CharField(max_length=255, verbose_name="Nome do Representante")
    fornecedor_marca = models.CharField(max_length=255, verbose_name="Fornecedor/Marca")
    data_agendada = models.DateField(verbose_name="Data da Visita")
    hora_agendada = models.TimeField(verbose_name="Horário da Visita")
    comprador_responsavel = models.CharField(max_length=255, verbose_name="Comprador Responsável")
    
    # Campos para controle de pontualidade (iguais ao Agendamento)
    compareceu = models.BooleanField(default=False, verbose_name="Representante compareceu?")
    hora_entrada_real = models.DateTimeField(null=True, blank=True, verbose_name="Hora de entrada real")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações adicionais")

    @property
    def status_pontualidade(self):
        """Calcula o status de pontualidade automaticamente"""
        if not self.compareceu or not self.hora_entrada_real:
            return "Não compareceu"
        
        # Combina data e hora agendada em datetime
        hora_prevista = timezone.make_aware(
            timezone.datetime.combine(self.data_agendada, self.hora_agendada)
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
        return f"{self.nome_representante} - {self.fornecedor_marca} - {self.data_agendada} {self.hora_agendada}"

class ChegadaDiaria(models.Model):
    data = models.DateField(default=timezone.now)
    total_agendamentos = models.PositiveIntegerField(default=0)
    total_chegados = models.PositiveIntegerField(default=0)
    total_pendentes = models.PositiveIntegerField(default=0)
    total_pontuais = models.PositiveIntegerField(default=0)
    total_atrasados = models.PositiveIntegerField(default=0)
    total_adiantados = models.PositiveIntegerField(default=0)
    
    # Campos para representantes
    total_representantes = models.PositiveIntegerField(default=0)
    total_representantes_chegados = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Chegadas de {self.data}"