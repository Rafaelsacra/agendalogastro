# Script PowerShell para iniciar Celery Beat
Write-Host "Iniciando Celery Beat para importacoes automaticas..." -ForegroundColor Green
Write-Host ""
Write-Host "Configuracao:" -ForegroundColor Yellow
Write-Host "- Importacao a cada 5 minutos" -ForegroundColor White
Write-Host "- Task: agenda.tasks.importar_agendamentos_task" -ForegroundColor White
Write-Host ""
Write-Host "Pressione Ctrl+C para parar" -ForegroundColor Red
Write-Host ""

try {
    python manage.py celery beat --loglevel=info
}
catch {
    Write-Host "Erro ao executar Celery Beat: $_" -ForegroundColor Red
}

Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
