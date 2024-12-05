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
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Check for 201 Created status code
        self.assertEqual(len(response.json()['results']), 3)  # Check the number of results

        #Check if DepositRequest object is saved in the db
        self.assertEqual(DepositRequest.objects.count(), 1)
        deposit = DepositRequest.objects.first()
        self.assertEqual(deposit.date, date(2024,1,1))
        self.assertEqual(deposit.periods, 3)
        self.assertEqual(deposit.amount, Decimal('10252')) #You'll want to calculate this precisely


    def test_invalid_date_format(self):
        data = {
            "date": "01-01-2024",  # Invalid date format
            "periods": 3,
            "amount": 10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Check for 400 Bad Request
        self.assertIn('error', response.json()) # Check that error message is returned


    def test_invalid_periods(self):
        data = {
            "date": "01.01.2024",
            "periods": -1,  #Invalid periods value
            "amount": 10000,
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Check for 400 Bad Request
        self.assertIn('error', response.json()) # Check that error message is returned

    def test_invalid_amount(self):
        data = {
            "date": "01.01.2024",
            "periods": 3,
            "amount": -10000,  #Invalid amount value
            "rate": 10
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Check for 400 Bad Request
        self.assertIn('error', response.json()) # Check that error message is returned

    def test_invalid_rate(self):
        data = {
            "date": "01.01.2024",
            "periods": 3,
            "amount": 10000,
            "rate": -10,  #Invalid rate value
        }
        response = self.client.post(reverse('calculate_deposit'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Check for 400 Bad Request
        self.assertIn('error', response.json())