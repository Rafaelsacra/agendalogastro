#!/usr/bin/env python
"""
Script para iniciar o Celery Beat para importações automáticas
"""
import os
import sys
import django
from pathlib import Path

# Adiciona o diretório do projeto ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core.celery import app

if __name__ == '__main__':
    print("Iniciando Celery Beat para importações automáticas...")
    print("Configuração atual:")
    print(f"- Broker: {app.conf.broker_url}")
    print(f"- Result Backend: {app.conf.result_backend}")
    print(f"- Beat Schedule: {app.conf.beat_schedule}")
    print("\nPressione Ctrl+C para parar")
    
    try:
        # Inicia o Celery Beat
        app.start(['beat', '--loglevel=info'])
    except KeyboardInterrupt:
        print("\nCelery Beat parado pelo usuário")
    except Exception as e:
        print(f"Erro ao iniciar Celery Beat: {e}")
