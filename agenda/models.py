from django.db import models

# Create your models here.

class Agendamento(models.Model):
    fornecedor = models.CharField(max_length=100)
    data = models.DateField()
    horario_agendado = models.TimeField()
    quantidade_volumes = models.IntegerField()
    nota_fiscal = models.CharField(max_length=50, blank=True, null=True)
    status_entrega = models.CharField(max_length=50, blank=True, null=True)
    # Outros campos podem ser adicionados conforme necessário

    def __str__(self):
        return f"{self.fornecedor} - {self.data} {self.horario_agendado}"
