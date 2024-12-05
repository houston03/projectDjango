from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
import json
from .models import DepositRequest
from datetime import date

# (venv) PS C:\Users\Stend\PycharmProjects\aProject\thetl> python manage.py test deposit

class CalculateDepositViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_input(self):
        data = {
            "date": "01.01.2024",
            "periods": 3,
            "amount": 10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')  # Отправляется POST-запрос
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()['results']), 3)
        self.assertEqual(DepositRequest.objects.count(), 1)  # Проверяется, что в базе данных создалась одна запись
        deposit = DepositRequest.objects.first()  # Получение созданной записи из базы данных
        self.assertEqual(deposit.date, date(2024,1,1))
        self.assertEqual(deposit.periods, 3)
        self.assertEqual(deposit.amount, Decimal('10252'))

# Тесты на ошибки, должны вернуть статус код 400 и сообщение об ошибке

    def test_invalid_date_format(self):
        data = {
            "date": "01-01-2024",
            "periods": 3,
            "amount": 10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


    def test_invalid_periods(self):
        data = {
            "date": "01.01.2024",
            "periods": -1,
            "amount": 10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_invalid_amount(self):
        data = {
            "date": "01.01.2024",
            "periods": 3,
            "amount": -10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_invalid_rate(self):
        data = {
            "date": "01.01.2024",
            "periods": 3,
            "amount": 10000,
            "rate": -10,
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())