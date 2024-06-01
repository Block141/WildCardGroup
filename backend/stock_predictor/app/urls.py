from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict_view, name='predict'),
    path('get_historical_data/', views.get_historical_data, name='get_historical_data'),
    path('get_weekly_data/', views.get_weekly_data, name='get_weekly_data'),
    path('get_monthly_data/', views.get_monthly_data, name='get_monthly_data'),
    path('news/', views.get_stock_news, name='get_stock_news'),

]


