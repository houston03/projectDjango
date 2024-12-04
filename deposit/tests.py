from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_UP
from .models import DepositRequest
import json
import datetime

class CalculateDepositTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_request(self):
        data = {
            "date": "01.01.2024",
            "periods": 3,
            "amount": 10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Проверяем статус ответа
        self.assertIn('results', response.json())     # Проверяем наличие результатов
        results = response.json()['results']
        self.assertEqual(len(results), 3)            # Проверяем количество результатов
        # Добавьте сюда более точные проверки результатов расчета, например:
        # self.assertEqual(results[0], "01.01.2024:10020.83") # Пример, рассчитайте значения заранее
        self.assertEqual(DepositRequest.objects.count(), 1) # Проверяем, что запись создана


    def test_invalid_date_format(self):
        data = {
            "date": "01-01-2024",  # Неверный формат даты
            "periods": 3,
            "amount": 10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Проверяем статус ответа
        self.assertIn('error', response.json())     # Проверяем наличие сообщения об ошибке
        self.assertTrue('Неверный формат данных' in response.json()['error']) # Проверяем текст ошибки


    def test_invalid_periods(self):
        data = {
            "date": "01.01.2024",
            "periods": -1,      # Неверное количество периодов
            "amount": 10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        # Добавьте проверку содержимого ошибки


    def test_invalid_amount(self):
        data = {
            "date": "01.01.2024",
            "periods": 3,
            "amount": -1000,    # Неверная сумма
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        # Добавьте проверку содержимого ошибки


    def test_invalid_rate(self):
        data = {
            "date": "01.01.2024",
            "periods": 3,
            "amount": 10000,
            "rate": -5        # Неверная процентная ставка
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        # Добавьте проверку содержимого ошибки


    def test_missing_fields(self):
        data = {
            "periods": 3,
            "amount": 10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        # Добавьте проверку содержимого ошибки

    def test_decimal_rounding(self):
        data = {
            "date": "01.01.2024",
            "periods": 1,
            "amount": 10000,
            "rate": 10.01
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        # Проверьте округление.  Рассчитайте ожидаемое значение вручную.
        expected_amount = Decimal('10083.75').quantize(Decimal('0.02'), ROUND_HALF_UP)
        self.assertEqual(Decimal(response.json()['results'][0].split(':')[1]), expected_amount)