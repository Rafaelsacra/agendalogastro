from celery import shared_task
from django.core.management import call_command
from django.core.cache import cache
from .models import Agendamento
import logging
from datetime import datetime
import sys

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def importar_agendamentos_task(self):
    try:
        # Captura o total de agendamentos ANTES da importação
        total_antes = Agendamento.objects.count()
        
        print("=" * 60)
        print(f"🔄 INICIANDO IMPORTAÇÃO AUTOMÁTICA - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📊 Total de agendamentos ANTES: {total_antes}")
        print("=" * 60)
        
        logger.info(f"Iniciando importação automática de agendamentos - Total antes: {total_antes}")
        
        # Executa o comando de importação
        call_command('importar_agendamentos')
        
        # Captura o total de agendamentos DEPOIS da importação
        total_depois = Agendamento.objects.count()
        novos_agendamentos = total_depois - total_antes
        
        # Armazena timestamp da última importação para o frontend
        cache.set('ultima_importacao', datetime.now().isoformat(), timeout=300)
        
        print("=" * 60)
        print(f"✅ IMPORTAÇÃO CONCLUÍDA - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📊 Total de agendamentos DEPOIS: {total_depois}")
        print(f"🆕 Novos agendamentos: {novos_agendamentos}")
        print(f"📈 Variação: {novos_agendamentos:+d}")
        print("=" * 60)
        
        logger.info(f"Importação automática concluída - Total: {total_depois}, Novos: {novos_agendamentos}")
        
        return {
            "status": "sucesso",
            "total_antes": total_antes,
            "total_depois": total_depois,
            "novos_agendamentos": novos_agendamentos,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print("=" * 60)
        print(f"❌ ERRO NA IMPORTAÇÃO - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Erro: {str(e)}")
        print("=" * 60)
        
        logger.error(f"Erro durante importação automática: {str(e)}")
        # Re-raise the exception so Celery can handle it
        raise 