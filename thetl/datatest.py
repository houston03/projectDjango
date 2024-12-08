import requests
import json

# (venv) PS C:\Users\Stend\PycharmProjects\aProject\thetl\deposit> python datatest.py
# Скрипт для сохранения результата в Постгрес и теста
url = 'http://127.0.0.1:8000/calculate/'
data = {
            "date": "01.01.2024",
            "periods": 3,
            "amount": 10000,
            "rate": 10
        }
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.raise_for_status()

    print(response.json())

except requests.exceptions.RequestException as e:
    print(f"Ошибка при отправке запроса: {e}")
except json.JSONDecodeError as e:
    print(f"Ошибка декодирования ответа: {e}")