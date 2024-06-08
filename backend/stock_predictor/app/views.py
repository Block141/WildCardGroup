from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf
from datetime import datetime, timedelta
import json
import requests
from stock_predictor.predict import run_model

def get_historical_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y") 
    return hist

def get_weekly_data(symbol):
    if symbol.method == 'GET':
        symbol = symbol.GET.get('symbol')
        if not symbol:
            return JsonResponse({'error': 'No symbol provided'}, status=400)
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            hist = yf.download(symbol, start=start_date, end=end_date, interval='1d')
            last_seven_days_data = hist.tail(7)
            return JsonResponse({'historical_data': json.loads(last_seven_days_data.to_json(orient='records'))})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_monthly_data(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol')
        if not symbol:
            return JsonResponse({'error': 'No symbol provided'}, status=400)
        try:
            hist = yf.download(symbol, period="1y", interval='1mo')
            # Add the date column to the DataFrame
            hist['Date'] = hist.index.strftime('%Y-%m-%d')
            # Convert historical data to JSON and return
            return JsonResponse({'historical_data': json.loads(hist.to_json(orient='records'))})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def index(request):
    return render(request, 'index.html')

# def predict_view(request):
#     if request.method == 'GET':
#         symbol = request.GET.get('symbol')
#         historical_data = get_historical_data(symbol)
#         result = run_model(historical_data)  # Run the model and get the result dictionary

#         return render(request, 'index.html', {'result': result, 'symbol': symbol})
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

def predict_view(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol')
        if not symbol:
            return JsonResponse({'error': 'No symbol provided'}, status=400)
        try:
            historical_data = get_historical_data(symbol)
            result = run_model(historical_data)  # Run the model and get the result dictionary
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_stock_news(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol')
        if not symbol:
            return JsonResponse({'error': 'No ticker provided'}, status=400)
        try:
            response = requests.get(f'https://api.tickertick.com/feed?q=z:{symbol}&n=5')
            response.raise_for_status()
            news = response.json()
            return JsonResponse(news)
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)