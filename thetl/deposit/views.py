from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DepositRequest
from rest_framework.parsers import JSONParser
import json
import datetime
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
import traceback

@api_view(['POST'])
def calculate_deposit(request):
    try:
        json_data = JSONParser().parse(request)

        date_str = json_data.get('date')
        periods = json_data.get('periods')
        amount = json_data.get('amount')
        rate = json_data.get('rate')

        # Валидация (аналогично вашему коду)



        input_date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()

        results = []
        current_date = input_date
        for i in range(periods):
            interest = amount * rate / 100 / 12
            amount += interest
            amount = Decimal(amount).quantize(Decimal('0.02'), ROUND_HALF_UP)
            results.append(f"{current_date.strftime('%d.%m.%Y')}:{amount}")
            current_date += timedelta(days=30)

        # Создаем объект DepositRequest и сохраняем
        deposit_request = DepositRequest(date=input_date, periods=periods, amount=amount, rate=rate, results='\n'.join(results))
        deposit_request.save()
        return Response({'results': results}, status=status.HTTP_201_CREATED)  # Возвращаем 201


    except ValueError as e:
        return Response({'error': f'Неверный формат данных: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Внутренняя ошибка: {e}', 'details': traceback.format_exc()},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Добавлена детальная информация

from django.shortcuts import render

def index(requests):
    return render(requests, 'index.html', {'title' : 'Main'})
