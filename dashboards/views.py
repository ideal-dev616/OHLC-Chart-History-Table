from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
import json
from datetime import datetime, timedelta
from django.conf import settings


def home(request):
  return render(request, 'home.html')

@login_required
def backtesting(request):
  file_path = settings.STATIC_ROOT + "stock.txt"   #full path to text.
  f = open(file_path , 'r')
  stocks = f.read().split("\n")
  f.close()

  url = "http://697da36f3f68.ngrok.io/history"
  
  today = datetime.now()
  dt_today = today.strftime("%Y-%m-%d %H:%M:00")
  fromDate = datetime.now() - timedelta(10)
  dt_from = fromDate.strftime("%Y-%m-%d %H:%M:00")

  payload = {
    "start_date": str(dt_from),
    "end_date": str(dt_today),
    "symbol": "AAIT",
    "bartype": "1min"
  }
  headers = {
    'Content-Type': 'application/json'
  }

  print(payload)

  response = requests.post(url, headers=headers, data=json.dumps(payload))
  print(response)
  return render(request, 'backtesting.html', {'json_chart': json.dumps(response.json()), 'json_table': response.json(), 'stocks': stocks})

def getUpdatedOHLC(request):
  # request should be ajax and method should be POST.
  if request.method == "POST":
    barType = request.POST.get('barType')
    stockType = request.POST.get('stockType')
    startDateTime = request.POST.get('startDateTime') + ":00"
    endDateTime = request.POST.get('endDateTime') + ":00"

    url = "http://697da36f3f68.ngrok.io/history"
    payload = {
      "start_date": str(startDateTime),
      "end_date": str(endDateTime),
      "symbol": str(stockType),
      "bartype": str(barType)
    }
    headers = {
      'Content-Type': 'application/json'
    }

    print(payload)
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.json())
    return JsonResponse({'json_table': response.json()}, status=200)
  return JsonResponse({"error": ""}, status=400)
