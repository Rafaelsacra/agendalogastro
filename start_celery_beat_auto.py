#!/usr/bin/env python
"""
Script para iniciar o Celery Beat automaticamente
Executa a importação de agendamentos a cada 1 minuto
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

from celery import Celery
from core.celery import app

if __name__ == '__main__':
    print("🚀 Iniciando Celery Beat para importação automática de agendamentos...")
    print("📅 Importação será executada a cada 1 minuto")
    print("🌐 Acesse http://localhost:8000/agenda/calendario/ para ver o calendário")
    print("⏰ Pressione Ctrl+C para parar")
    print("-" * 60)
    
    try:
        # Inicia o Celery Beat
        app.start(['beat', '--loglevel=info'])
    except KeyboardInterrupt:
        print("\n🛑 Celery Beat parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar Celery Beat: {e}")
        sys.exit(1)
