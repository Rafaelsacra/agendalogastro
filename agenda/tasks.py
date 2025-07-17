from celery import shared_task
from django.core.management import call_command

@shared_task
def importar_agendamentos_task():
    call_command('importar_agendamentos') 