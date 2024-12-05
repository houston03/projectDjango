from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DepositRequest
from rest_framework.parsers import JSONParser
import datetime
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP


@api_view(['POST'])
def calculate_deposit(request):
    try:
        json_data = JSONParser().parse(request)

        date_str = json_data.get('date')
        periods = json_data.get('periods')
        amount = json_data.get('amount')
        rate = json_data.get('rate')

        if not date_str:
            raise ValueError("Дата не указана")
        input_date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()

        if not isinstance(periods, int) or periods <= 0:
            raise ValueError("Неверное количество периодов")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Неверная сумма вклада")
        if not isinstance(rate, (int, float)) or rate < 0:
            raise ValueError("Неверная процентная ставка")

        amount = Decimal(str(amount))
        rate = Decimal(str(rate))
        results = []
        current_date = input_date
        total_amount = Decimal(amount)  # Initialize total_amount

        for i in range(periods):
            interest = (amount * rate / Decimal(100) / Decimal(12))
            total_amount += interest  # Accumulate without rounding
            amount += interest
            rounded_amount = amount.quantize(Decimal('0.02'), ROUND_HALF_UP)  # Round only for display
            results.append(f"{current_date.strftime('%d.%m.%Y')}:{rounded_amount}")
            current_date += timedelta(days=30)

        # Round only at the end
        final_amount = total_amount.quantize(Decimal('0.02'), ROUND_HALF_UP)

        deposit_request = DepositRequest(date=input_date, periods=periods, amount=final_amount, rate=rate,
                                         results='\n'.join(results))
        deposit_request.save()
        return Response({'results': results}, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({'error': f'Неверный формат данных: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Внутренняя ошибка: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.shortcuts import render

def index(request):  #Fixed typo here
    return render(request, 'index.html', {'title': 'Main'})