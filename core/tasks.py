from io import BytesIO
from typing import Any

import requests
from celery import shared_task
from decouple import config
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Protection

from core.models import Coins
from core.templatetags.custom_tags import currency


@shared_task
def get_coins_data_from_coingecko_and_store() -> None:
    """Fetch data from coingecko api and store."""
    base_url = 'https://api.coingecko.com/api/v3/coins/'
    market_currency_order = 'markets?vs_currency=ngn&order=market_cap_desc&'
    per_page = 'per_page=250&page=1&sparkline=false'
    final_url = f'{base_url}{market_currency_order}{per_page}'

    coin_data = requests.get(final_url).json()

    for data in coin_data:
        coin, _ = Coins.objects.get_or_create(name=data['name'], symbol=data['symbol'])
        coin.image_url = data['image']
        coin.current_price = data['current_price']
        coin.price_change_within_24_hours = data['price_change_24h']
        coin.rank = data['market_cap_rank']
        coin.market_cap = data['market_cap']
        coin.total_supply = data['total_supply']
        coin.save()


@shared_task
def export_data_to_excel(user_email: str) -> None:
    """Send extracted model data and save in excel and send to email."""
    excelfile = BytesIO()
    workbook = Workbook()
    workbook.remove(workbook.active)
    worksheet = workbook.create_sheet(title='Latest Cryptocurrency Coins', index=1)
    workbook.security.workbookPassword = config('PASSWORD', default='12345data')
    workbook.security.lockStructure = config('PROTECT', default=True, cast=bool)
    workbook.security.revisionsPassword = config('PASSWORD', default='12345data')
    worksheet.protection.sheet = config('PROTECT', default=True, cast=bool)
    worksheet.protection.formatCells = config('PROTECT', default=False, cast=bool)

    worksheet.sheet_properties.tabColor = '1072BA'
    worksheet.freeze_panes = 'I2'

    coin_queryset = Coins.objects.all().order_by('rank')
    columns = ['Name', 'Symbol', 'Rank', 'Current price', 'Price change', 'Market cap', 'Total supply']
    row_num = 1

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.font = Font(bold=True)
    # Iterate through all coins
    for _, coin in enumerate(coin_queryset, 1):
        row_num += 1

        # Define the data for each cell in the row
        row = [
            coin.name,
            f'{coin.symbol}'.upper(),
            coin.rank,
            currency(coin.current_price),
            currency(coin.price_change_within_24_hours),
            currency(coin.market_cap),
            coin.total_supply,
        ]

        # Assign the data for each cell of the row
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
            cell.protection = Protection(locked=True)
    workbook.save(excelfile)
    now = timezone.now()
    message = EmailMessage(
        f'Coin data as of {now.date().isoformat()}',
        f'Generated at: {now.isoformat()}',
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
    message.attach('latest-coin-list.xlsx', excelfile.getvalue(), 'application/vnd.ms-excel')
    message.send()


@shared_task
def populate_googlesheet_with_coins_data() -> None:
    """Populate Googlesheet with the coin data from the database."""
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = config('SPREADSHEET_ID', default='1AFNyUKcqgwO-CCXRubcIALOC74yfV716Q5q57Ojjicc')

    url = config('SERVICE_KEY_PATH')
    response = requests.get(url)
    with open('core/djangoexcel.json', 'wb') as file:
        file.write(response.content)

    service_account_file = 'core/djangoexcel.json'
    creds = None
    creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    coin_queryset = Coins.objects.all().order_by('rank')
    data: list[Any] = []
    for coin in coin_queryset:
        data.append(
            [
                coin.name,
                f'{coin.symbol}'.upper(),
                coin.rank,
                str(currency(coin.current_price)),
                str(currency(coin.price_change_within_24_hours)),
                str(currency(coin.market_cap)),
                str(coin.total_supply),
            ]
        )
    sheet.values().clear(spreadsheetId=spreadsheet_id, range='Coins!A2:G').execute()
    sheet.values().append(
        spreadsheetId=spreadsheet_id, range='Coins!A2:G2', valueInputOption='USER_ENTERED', body={'values': data}
    ).execute()
