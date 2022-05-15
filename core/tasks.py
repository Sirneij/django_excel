import requests
from celery import shared_task
from io import BytesIO

from core.models import Coins
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Protection
from decouple import config


@shared_task
def get_coins_data_from_coingecko_and_store()->None:
    BASE_URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=ngn&order=market_cap_desc&per_page=250&page=1&sparkline=false'

    coin_data = requests.get(BASE_URL).json()

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
def export_data_to_excel(user_email:str)->None:
    excelfile = BytesIO()
    workbook = Workbook()
    workbook.remove(workbook.active)
    worksheet = workbook.create_sheet(title='Latest Cryptocurrency Coins Data', index=1)
    workbook.security.workbookPassword = config('PASSWORD', default='12345data')
    workbook.security.lockStructure = config('PROTECT', default=True, cast=bool)
    workbook.security.revisionsPassword = config('PASSWORD', default='12345data')
    worksheet.protection.sheet = config('PROTECT', default=True, cast=bool)
    worksheet.protection.formatCells = config('PROTECT', default=False, cast=bool)

    worksheet.sheet_properties.tabColor = '1072BA'
    worksheet.freeze_panes = 'I2'

    coin_queryset = Coins.objects.all().order_by('-rank')
    columns = ['Logo', 'Name', 'Symbol', 'Rank', 'Current price', 'Price change', 'Market cap', 'Total supply']
    row_num = 1

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.font = Font(bold=True)
    # Iterate through all news
    for index, new in enumerate(coin_queryset, 1):
        row_num += 1

        # Define the data for each cell in the row
        row = [
            index,
            str(new.id),
            new.title,
            new.story_type,
            new.author,
            new.created_by,
            str(new.time),
            new.text,
            new.story_url,
        ]

        # Assign the data for each cell of the row
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
            cell.protection = Protection(locked=True)

    workbook.save(excelfile)