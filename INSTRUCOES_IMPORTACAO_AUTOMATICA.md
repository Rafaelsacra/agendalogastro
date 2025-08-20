# 🚀 Sistema de Importação Automática de Agendamentos

## ✨ Funcionalidades Implementadas

### 🔄 Importação Automática
- **Frequência**: A cada 1 minuto (configurável)
- **Comando**: Executa automaticamente `python manage.py importar_agendamentos`
- **Logs**: Registra todas as operações no console

### 📅 Calendário Auto-Atualizável
- **Atualização**: Eventos são atualizados automaticamente a cada minuto
- **Status em Tempo Real**: Mostra informações sobre importações e total de agendamentos
- **Notificações**: Alerta visual quando novos agendamentos são importados

## 🛠️ Como Usar

### 1. Iniciar o Django
```bash
python manage.py runserver
```

### 2. Iniciar o Celery Worker (em um terminal separado)
```bash
celery -A core worker --loglevel=info
```

### 3. Iniciar o Celery Beat (em outro terminal separado)
```bash
python start_celery_beat_auto.py
```

### 4. Acessar o Calendário
Abra no navegador: http://localhost:8000/agenda/calendario/

## 📊 Barra de Status

O calendário agora inclui uma barra de status que mostra:
- **Status**: Estado da conexão com o sistema
- **Total de Agendamentos**: Número atual de agendamentos no banco
- **Última Atualização**: Timestamp da última importação automática
- **Auto-refresh**: Indica que o sistema está ativo

## 🔔 Notificações

- **Verde**: Novos agendamentos foram importados
- **Automática**: Aparece por 5 segundos e desaparece
- **Tempo Real**: Detecta mudanças automaticamente

## ⚙️ Configurações

### Alterar Frequência de Importação
Edite `core/settings.py`:
```python
CELERY_BEAT_SCHEDULE = {
    'importar-agendamentos-a-cada-minuto': {
        'task': 'agenda.tasks.importar_agendamentos_task',
        'schedule': crontab(minute='*/2'),  # A cada 2 minutos
    },
}
```

### Logs Detalhados
Para ver logs mais detalhados, altere em `core/settings.py`:
```python
'level': 'DEBUG',  # Em vez de 'INFO'
```

## 🚨 Solução de Problemas

### Celery não inicia
1. Verifique se o Django está rodando
2. Certifique-se de que todas as dependências estão instaladas
3. Verifique se o banco de dados está acessível

### Importação não funciona
1. Verifique os logs do Celery Worker
2. Teste o comando manualmente: `python manage.py importar_agendamentos`
3. Verifique se o arquivo de dados está no local correto

### Calendário não atualiza
1. Verifique se o Celery Beat está rodando
2. Abra o console do navegador para ver erros JavaScript
3. Verifique se a URL `/verificar-atualizacoes/` está funcionando

## 📁 Arquivos Modificados

- `core/settings.py` - Configurações do Celery e cache
- `agenda/tasks.py` - Task de importação com cache
- `agenda/views.py` - Nova view para verificar atualizações
- `agenda/urls.py` - Nova URL para verificar atualizações
- `agenda/templates/agenda/calendario.html` - Interface melhorada
- `start_celery_beat_auto.py` - Script de inicialização automática

## 🎯 Próximos Passos

1. **Monitoramento**: Adicionar dashboard de estatísticas
2. **Alertas**: Notificações por email quando houver erros
3. **Backup**: Sistema de backup automático dos agendamentos
4. **Relatórios**: Geração automática de relatórios diários

---

**Sistema configurado e funcionando! 🎉**
A importação automática está ativa e o calendário se atualiza a cada minuto.
