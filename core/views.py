from django.shortcuts import render

from core.models import Coins


def index(request):
    coins = Coins.objects.all().order_by('rank')
    context: dict[str, str] = {
        'coin_data': coins,
    }
    return render(request, 'coin_data.html', context)
