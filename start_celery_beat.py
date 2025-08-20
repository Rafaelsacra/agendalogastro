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

from celery.bin.celery import main as celery_main

if __name__ == '__main__':
    print("Iniciando Celery Beat para importações automáticas...")
    print("Configuração:")
    print("- Importação a cada 5 minutos")
    print("- Task: agenda.tasks.importar_agendamentos_task")
    print("\nPressione Ctrl+C para parar")
    
    try:
        # Inicia o Celery Beat
        sys.argv = ['celery', 'beat', '--loglevel=info']
        celery_main()
    except KeyboardInterrupt:
        print("\nCelery Beat parado pelo usuário")
    except Exception as e:
        print(f"Erro ao iniciar Celery Beat: {e}")
        print("Tentando método alternativo...")
        
        try:
            # Método alternativo usando o app diretamente
            from core.celery import app
            print("Iniciando Celery Beat usando app diretamente...")
            app.start(['beat', '--loglevel=info'])
        except Exception as e2:
            print(f"Erro no método alternativo: {e2}")
