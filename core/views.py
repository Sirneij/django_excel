import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from core.models import Coins
from core.tasks import export_data_to_excel


def index(request: HttpRequest) -> HttpResponse:
    coins = Coins.objects.all().order_by('rank')
    context: dict[str, str] = {
        'coin_data': coins,
    }
    return render(request, 'coin_data.html', context)


def extract_and_send_coin_data_via_email(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        request_data = json.loads(request.body)
        email = request_data['userEmail']
        export_data_to_excel.delay(email)
        return JsonResponse({'message': 'Coins data successfully extracted 💃!'}, status=200)
    else:
        return JsonResponse({'message': 'Coins data failed to be extracted 😔!'}, status=500)
