@echo off
echo Iniciando Celery Beat para importacoes automaticas...
echo.
echo Configuracao:
echo - Importacao a cada 5 minutos
echo - Task: agenda.tasks.importar_agendamentos_task
echo.
echo Pressione Ctrl+C para parar
echo.

python manage.py celery beat --loglevel=info

pause
