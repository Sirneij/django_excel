from django.urls import path

from core import views

app_name: str = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('extract-data-to-excel/', views.extract_and_send_coin_data_via_email, name='extract_data'),
]
