from datetime import datetime
from io import BytesIO
from typing import Any, Optional

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
    response = requests.get(settings.GOOGLE_API_SERVICE_KEY_URL)
    with open('core/djangoexcel.json', 'wb') as file:
        file.write(response.content)
    service_account_file = 'core/djangoexcel.json'
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=settings.GOOGLE_API_SCOPE
    )
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    sheet_metadata_values = sheet.get(spreadsheetId=settings.SPREADSHEET_ID).execute()
    csheets = sheet_metadata_values.get('sheets', '')
    datetime_format = '%a %b %d %Y %Hh%Mm'
    if csheets and len(csheets) > 1:
        for csheet in csheets:
            sheet_title = csheet.get('properties', {}).get('title', '')
            date_segment_of_the_title = ' '.join(sheet_title.split(' ')[0:5]).strip()
            parsed_datetime: Optional[Any] = None
            try:
                parsed_datetime = datetime.strptime(date_segment_of_the_title, datetime_format)
            except ValueError as err:
                print(err)
            now = timezone.now().strftime(datetime_format)
            if (
                parsed_datetime
                and (datetime.strptime(now, datetime_format) - parsed_datetime).seconds
                > settings.SPREADSHEET_TAB_EXPIRY
            ):
                sheet_id = csheet.get('properties', {}).get('sheetId', 0)
                batch_update_request_body = {'requests': [{'deleteSheet': {'sheetId': sheet_id}}]}
                sheet.batchUpdate(spreadsheetId=settings.SPREADSHEET_ID, body=batch_update_request_body).execute()

    coin_queryset = Coins.objects.all().order_by('rank')
    coin_data_list: list[Any] = [
        [
            'Name',
            'Symbol',
            'Rank',
            'Current price',
            'Price change',
            'Market cap',
            'Total supply',
        ]
    ]
    for coin in coin_queryset:
        coin_data_list.append(
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

    new_sheet_title = f'{timezone.now().strftime(datetime_format)} Coin data'
    batch_update_request_body = {
        'requests': [
            {
                'addSheet': {
                    'properties': {
                        'title': new_sheet_title,
                        'tabColor': {'red': 0.968627451, 'green': 0.576470588, 'blue': 0.101960784},
                        'gridProperties': {'rowCount': len(coin_data_list), 'columnCount': 7},
                    }
                }
            }
        ]
    }
    sheet.batchUpdate(spreadsheetId=settings.SPREADSHEET_ID, body=batch_update_request_body).execute()
    sheet.values().append(
        spreadsheetId=settings.SPREADSHEET_ID,
        range=f"'{new_sheet_title}'!A1:G1",
        valueInputOption='USER_ENTERED',
        body={'values': coin_data_list},
    ).execute()
