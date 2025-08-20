#!/usr/bin/env python
"""
Script para testar se a task do Celery está funcionando
"""

import os
import sys
import django
from pathlib import Path

# Adiciona o diretório do projeto ao Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from agenda.tasks import importar_agendamentos_task
from agenda.models import Agendamento

def testar_task():
    print("🧪 TESTANDO TASK DE IMPORTAÇÃO AUTOMÁTICA")
    print("=" * 60)
    
    # Conta agendamentos antes
    total_antes = Agendamento.objects.count()
    print(f"📊 Total de agendamentos ANTES do teste: {total_antes}")
    
    try:
        # Executa a task diretamente
        print("\n🔄 Executando task...")
        resultado = importar_agendamentos_task.delay()
        
        # Aguarda o resultado
        resultado_final = resultado.get(timeout=60)
        print(f"\n✅ Task executada com sucesso!")
        print(f"📋 Resultado: {resultado_final}")
        
        # Conta agendamentos depois
        total_depois = Agendamento.objects.count()
        print(f"📊 Total de agendamentos DEPOIS do teste: {total_depois}")
        print(f"🆕 Variação: {total_depois - total_antes:+d}")
        
    except Exception as e:
        print(f"\n❌ Erro ao executar task: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    testar_task()
