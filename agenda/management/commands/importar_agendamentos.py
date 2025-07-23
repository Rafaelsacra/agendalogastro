import gspread
from django.core.management.base import BaseCommand
from core import settings
from agenda.models import Agendamento
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configurações
CREDENTIALS_PATH = 'core/credentials.json'
SPREADSHEET_ID = '1Jocq3vX6YDoJ0NJ4UAYWkePfu1txB7hflH8gIxcQf0k'
SHEET_NAME = 'AGENDA'  # Nome exato da aba

class Command(BaseCommand):
    help = 'Importa agendamentos do Google Sheets para o banco de dados'

    def handle(self, *args, **options):
        # Limpa todos os agendamentos antes de importar
        Agendamento.objects.all().delete()
        # Autenticação
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scopes)
        gc = gspread.authorize(creds)
        
        # Abrir planilha e aba
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(SHEET_NAME)
        
        # Ler todos os registros
        rows = worksheet.get_all_records(expected_headers=["FORNECEDOR", "DATA", "HORÁRIO AGENDADO"])
        count = 0
        for row in rows:
            try:
                row_filtrado = {
                    'FORNECEDOR': str(row.get('FORNECEDOR', '')).strip(),
                    'DATA': str(row.get('DATA', '')).strip(),
                    'HORÁRIO AGENDADO': str(row.get('HORÁRIO AGENDADO', '')).strip()
                }

                fornecedor = row_filtrado['FORNECEDOR']
                data_str = row_filtrado['DATA']
                horario_str = row_filtrado['HORÁRIO AGENDADO']

                # Pula linhas sem fornecedor, data ou horário
                if not fornecedor or not data_str or not horario_str:
                    continue

                # Tenta converter a data
                try:
                    data = datetime.strptime(data_str, '%d/%m/%Y').date()
                except Exception:
                    continue  # pula se a data for inválida

                # Tenta converter o horário
                try:
                    horario = datetime.strptime(horario_str, '%H:%M').time()
                except Exception:
                    continue  # pula se o horário for inválido

                agendamento, created = Agendamento.objects.update_or_create(
                    fornecedor=fornecedor,
                    data=data,
                    horario_agendado=horario,
                    defaults={
                        'quantidade_volumes': 0,
                    }
                )
                count += 1
            except Exception as e:
                self.stderr.write(f'Erro ao importar linha: {row_filtrado} - {e}')
        self.stdout.write(f'Importação concluída. {count} agendamentos processados.') 