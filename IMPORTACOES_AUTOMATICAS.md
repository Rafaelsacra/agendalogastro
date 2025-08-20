# Importações Automáticas - Sistema de Agendamento

## Visão Geral

O sistema está configurado para importar automaticamente agendamentos do Google Sheets a cada 5 minutos usando Celery Beat.

## Configuração Atual

- **Frequência**: A cada 5 minutos
- **Task**: `agenda.tasks.importar_agendamentos_task`
- **Fonte**: Google Sheets (ID: 1Jocq3vX6YDoJ0NJ4UAYWkePfu1txB7hflH8gIxcQf0k)
- **Aba**: AGENDA

## Como Iniciar as Importações Automáticas

### Opção 1: Script Batch (Windows)
```bash
start_celery_beat.bat
```

### Opção 2: Script PowerShell
```powershell
.\start_celery_beat.ps1
```

### Opção 3: Comando Manual
```bash
python manage.py celery beat --loglevel=info
```

## Como Funciona

1. **Celery Beat** executa a cada 5 minutos
2. **Task** `importar_agendamentos_task` é executada
3. **Comando** `importar_agendamentos` é chamado
4. **Google Sheets** é consultado para novos dados
5. **Banco de dados** é atualizado com os agendamentos

## Monitoramento

### Logs
Os logs são exibidos no console e incluem:
- Início da importação
- Número de agendamentos processados
- Erros encontrados
- Conclusão da importação

### Status das Tasks
Para verificar o status das tasks:
```python
python manage.py shell -c "from core.celery import app; print('Beat Schedule:', app.conf.beat_schedule)"
```

## Solução de Problemas

### Task não está sendo executada
1. Verifique se o Celery Beat está rodando
2. Confirme se a task está registrada
3. Verifique os logs de erro

### Erro de conexão com Google Sheets
1. Verifique se o arquivo `credentials.json` existe
2. Confirme se as permissões estão corretas
3. Verifique se o ID da planilha está correto

### Importação não está funcionando
1. Execute a task manualmente para testar
2. Verifique os logs de erro
3. Confirme se o banco de dados está acessível

## Configuração Avançada

### Alterar Frequência
Edite `core/settings.py`:
```python
CELERY_BEAT_SCHEDULE = {
    'importar-agendamentos-a-cada-5-minutos': {
        'task': 'agenda.tasks.importar_agendamentos_task',
        'schedule': crontab(minute='*/5'),  # A cada 5 minutos
    },
}
```

### Adicionar Novas Tasks
1. Crie a task em `agenda/tasks.py`
2. Adicione ao `CELERY_BEAT_SCHEDULE`
3. Reinicie o Celery Beat

## Arquivos Importantes

- `core/settings.py` - Configuração do Celery
- `core/celery.py` - Configuração da aplicação Celery
- `agenda/tasks.py` - Tasks do Celery
- `agenda/management/commands/importar_agendamentos.py` - Comando de importação

## Requisitos

- Python 3.8+
- Django 5.1+
- Celery
- gspread
- google-auth
