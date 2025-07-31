from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def importar_agendamentos_task(self):
    try:
        logger.info("Iniciando importação de agendamentos...")
        call_command('importar_agendamentos')
        logger.info("Importação de agendamentos concluída com sucesso.")
        return "Importação concluída com sucesso"
    except Exception as e:
        logger.error(f"Erro durante importação de agendamentos: {str(e)}")
        # Re-raise the exception so Celery can handle it
        raise 